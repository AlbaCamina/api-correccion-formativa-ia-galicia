import os
import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from backend.main import app
from backend.models.database import Base, get_db
from backend.models.user import Profesor
from backend.models.rubrica import RubricaDocente
from backend.models.marco import MarcoEvaluacion
from backend.models.submission import Submission, Evaluacion, ChangeLog
from backend.services.auth_service import get_current_profesor

# Configuración de base de datos en memoria SQLite para tests unitarios/integración aislados
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class TestEvaluationRouter(unittest.TestCase):
    def setUp(self):
        # Configurar LLM_PROVIDER=mock para tests unitarios/integración
        self.original_provider = os.getenv("LLM_PROVIDER")
        os.environ["LLM_PROVIDER"] = "mock"

        # Crear esquema de base de datos relacional en la memoria SQLite
        Base.metadata.create_all(bind=engine)
        self.db = TestingSessionLocal()

        # Insertar profesor y rúbrica de prueba en BBDD de test
        self.profesor = Profesor(id=1, email="alba@edu.xunta.gal", nombre="Alba Camiña", hashed_password="hashed_mock")
        self.db.add(self.profesor)

        self.rubrica = RubricaDocente(
            id=1,
            profesor_id=1,
            nombre="Precisión conceptual platónica",
            criterios=[
                {
                    "id": "C1",
                    "nombre": "Precisión conceptual",
                    "descripcion": "Evalúa el simbolismo de la caverna de Platón y su precisión.",
                    "peso": 100.0
                }
            ]
        )
        self.db.add(self.rubrica)
        self.db.commit()

        # Sobrescribir dependencias en FastAPI
        def override_get_db():
            try:
                yield self.db
            finally:
                pass

        def override_get_current_profesor():
            return self.profesor

        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_current_profesor] = override_get_current_profesor
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()
        self.db.close()
        Base.metadata.drop_all(bind=engine)
        if self.original_provider:
            os.environ["LLM_PROVIDER"] = self.original_provider
        else:
            os.environ.pop("LLM_PROVIDER", None)

    def test_evaluate_endpoint_success(self):
        """Valida que POST /api/v1/evaluate guarda la entrega y devuelve la evaluación formativa mockeada (v0.2)."""
        payload = {
            "student_answer": "El prisionero sale a la luz exterior y ve el sol...",
            "rubrica_id": 1,
            "question": "¿Qué simboliza la salida del prisionero?"
        }
        response = self.client.post("/api/v1/evaluate", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.json()

        # Validaciones de estructura de EvaluacionResponse (v0.2)
        self.assertIn("id", data)
        self.assertIn("submission_id", data)
        self.assertIn("resultado_ia", data)

        resultado = data["resultado_ia"]
        self.assertIn("transcription", resultado)
        self.assertEqual(resultado["calificacion_cualitativa"], "NT")
        self.assertEqual(len(resultado["visualMarkers"]), 1)
        self.assertEqual(resultado["visualMarkers"][0]["type"], "error_excluido")
        self.assertIn("siguiente_paso_accionable", resultado)
        self.assertIn("qualitativeAnalysis", resultado)
        self.assertEqual(resultado["confidence_score"], 0.92)

    def test_evaluate_endpoint_validation_error(self):
        """Valida que enviar datos vacíos o sin rúbrica lanza error 400 o 422."""
        # 1. student_answer vacío -> 400
        payload = {
            "student_answer": "",
            "rubrica_id": 1
        }
        response = self.client.post("/api/v1/evaluate", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("La respuesta del estudiante no puede estar vacía", response.json()["detail"])

        # 2. rubrica_id inexistente o de otro docente -> 404
        payload = {
            "student_answer": "Respuesta correcta",
            "rubrica_id": 999
        }
        response = self.client.post("/api/v1/evaluate", json=payload)
        self.assertEqual(response.status_code, 404)
        self.assertIn("La rúbrica especificada no existe", response.json()["detail"])

    def test_evaluate_endpoint_invalid_pydantic_payload(self):
        """Valida que enviar un payload malformado lanza HTTP 422 con formato {error, detail}."""
        payload = {
            "student_answer_incorrect_field": "Hola",
            "rubrica_id": "no-es-un-entero"
        }
        response = self.client.post("/api/v1/evaluate", json=payload)
        self.assertEqual(response.status_code, 422)
        data = response.json()
        self.assertIn("detail", data)

    def test_startup_validation_missing_key(self):
        """Valida que startup_validation aborta si falta la key correspondiente en la configuración."""
        import asyncio
        from backend.main import startup_validation

        orig_provider = os.environ.get("LLM_PROVIDER")
        orig_openai_key = os.environ.get("OPENAI_API_KEY")

        try:
            os.environ["LLM_PROVIDER"] = "openai"
            os.environ["OPENAI_API_KEY"] = "tu_api_key_de_openai_aqui"
            with self.assertRaises(RuntimeError):
                asyncio.run(startup_validation())

            os.environ["LLM_PROVIDER"] = "groq"
            os.environ["GROQ_API_KEY"] = "tu_api_key_de_groq_aqui"
            with self.assertRaises(RuntimeError):
                asyncio.run(startup_validation())

            os.environ["LLM_PROVIDER"] = "invalid_llm"
            with self.assertRaises(RuntimeError):
                asyncio.run(startup_validation())

        finally:
            if orig_provider:
                os.environ["LLM_PROVIDER"] = orig_provider
            else:
                os.environ.pop("LLM_PROVIDER", None)
            if orig_openai_key:
                os.environ["OPENAI_API_KEY"] = orig_openai_key
            else:
                os.environ.pop("OPENAI_API_KEY", None)


if __name__ == "__main__":
    unittest.main()
