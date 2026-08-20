import os
import unittest
import io
import json
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from PIL import Image

from backend.main import app
from backend.models.database import Base, get_db
from backend.models.user import Profesor
from backend.models.rubrica import RubricaDocente
from backend.models.marco import MarcoEvaluacion
from backend.models.submission import Submission, Evaluacion, ChangeLog
from backend.services.auth_service import get_current_profesor

# Configuración de base de datos SQLite en memoria para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class TestSubmissionRouter(unittest.TestCase):
    def setUp(self):
        # Configurar LLM_PROVIDER=mock para los tests
        self.original_provider = os.getenv("LLM_PROVIDER")
        os.environ["LLM_PROVIDER"] = "mock"

        # Crear esquema de base de datos relacional
        Base.metadata.create_all(bind=engine)
        self.db = TestingSessionLocal()

        # Insertar datos de prueba
        self.profesor = Profesor(id=1, email="profesor@edu.xunta.es", nombre="Alba Camiña", hashed_password="hashed_mock")
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

        self.marco = MarcoEvaluacion(
            id=1,
            nombre="Decreto 156/2022",
            asignatura="Filosofía",
            curso="1 BACH",
            etapa="BACH",
            rubrica_completa={}
        )
        self.db.add(self.marco)
        
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

        # Clean up mock uploads
        if os.path.exists("uploads"):
            for f in os.listdir("uploads"):
                if f.endswith(".png") or f.endswith(".pdf") or f.endswith(".txt"):
                    try:
                        os.remove(os.path.join("uploads", f))
                    except OSError:
                        pass

    def test_upload_image_success(self):
        """Valida que subir una imagen PNG válida guarda el archivo y retorna 201."""
        file_content = b"fake-png-binary-content"
        file_name = "test_examen.png"
        
        response = self.client.post(
            "/api/v1/submissions/upload",
            files={"file": (file_name, file_content, "image/png")}
        )
        
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["original_filename"], file_name)
        self.assertTrue(data["saved_filename"].endswith(".png"))
        self.assertTrue(data["url"].startswith("/uploads/"))
        
        # Verificar que el archivo realmente se guardó localmente
        saved_path = os.path.join("uploads", data["saved_filename"])
        self.assertTrue(os.path.exists(saved_path))
        with open(saved_path, "rb") as f:
            self.assertEqual(f.read(), file_content)

    def test_upload_pdf_success(self):
        """Valida que subir un archivo PDF válido guarda el archivo y retorna 201."""
        file_content = b"%PDF-1.4 fake pdf content"
        file_name = "test_examen.pdf"
        
        response = self.client.post(
            "/api/v1/submissions/upload",
            files={"file": (file_name, file_content, "application/pdf")}
        )
        
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["original_filename"], file_name)
        self.assertTrue(data["saved_filename"].endswith(".pdf"))

    def test_upload_invalid_extension(self):
        """Valida que subir un archivo con extensión no permitida (.txt) retorna 400."""
        file_content = b"fake text content"
        file_name = "cheat_sheet.txt"
        
        response = self.client.post(
            "/api/v1/submissions/upload",
            files={"file": (file_name, file_content, "text/plain")}
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("no soportado", response.json()["detail"])

    def test_upload_oversized_file(self):
        """Valida que subir un archivo que excede 25 MB retorna 400."""
        oversized_content = b"0" * (26 * 1024 * 1024)
        file_name = "huge_scan.png"
        
        response = self.client.post(
            "/api/v1/submissions/upload",
            files={"file": (file_name, oversized_content, "image/png")}
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("excede el límite máximo de 25 MB", response.json()["detail"])

    def test_serve_uploaded_file(self):
        """Valida que se puede descargar el archivo subido mediante la ruta de estáticos /uploads/."""
        file_content = b"fake-pdf-content"
        file_name = "doc.pdf"
        
        # 1. Subir
        upload_resp = self.client.post(
            "/api/v1/submissions/upload",
            files={"file": (file_name, file_content, "application/pdf")}
        )
        self.assertEqual(upload_resp.status_code, 201)
        url = upload_resp.json()["url"]
        
        # 2. Descargar/Servir
        serve_resp = self.client.get(url)
        self.assertEqual(serve_resp.status_code, 200)
        self.assertEqual(serve_resp.content, file_content)

    def test_upload_and_evaluate_success_image(self):
        """Valida el flujo exitoso de subida, transcripción y evaluación de una imagen recortada."""
        # Generar una imagen recortada válida en memoria (proporciones correctas: ratio <= 1.2)
        img = Image.new("RGB", (100, 100), color="white")
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format="PNG")
        img_bytes = img_byte_arr.getvalue()

        # Enviar petición POST
        response = self.client.post(
            "/api/v1/submissions/upload-and-evaluate",
            files={"file": ("cropped_examen.png", img_bytes, "image/png")},
            data={
                "rubrica_id": 1,
                "marco_id": 1,
                "etapa": "BACH",
                "modo_evaluacion": "COMBINADO",
                "question": "¿Qué simboliza el sol?",
                "alumno_id": "ALU-99",
                "adaptaciones_alumno": json.dumps({"excluir_ortografia": True})
            }
        )

        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["submission_id"], data["submission_id"])
        self.assertFalse(data["aprobado_por_profesor"])
        
        # Verificar la transcripción en el contrato de resultado de la IA
        resultado_ia = data["resultado_ia"]
        self.assertIn("transcription", resultado_ia)
        # Como es modo mock de vision_service, devolverá el texto del mock
        self.assertIn("Examen de Filosofía", resultado_ia["transcription"])

        # Verificar persistencia en base de datos
        sub_db = self.db.query(Submission).filter(Submission.alumno_id == "ALU-99").first()
        self.assertIsNotNone(sub_db)
        self.assertEqual(sub_db.estado, "REVIEW")
        
        # Verificar registro de ChangeLog
        log = self.db.query(ChangeLog).filter(ChangeLog.submission_id == sub_db.id).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.accion, "IA_EVALUATION")
        self.assertEqual(log.actor, "IA")
        self.assertTrue(log.audit_metadata["url_archivo"].startswith("/uploads/"))

    def test_upload_and_evaluate_fail_uncropped_image(self):
        """Valida que subir una imagen no recortada (ratio > 1.2) sea rechazado con HTTP 400."""
        # Generar una imagen no recortada (ratio alto/ancho = 1.5 > 1.2)
        img = Image.new("RGB", (100, 150), color="white")
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format="PNG")
        img_bytes = img_byte_arr.getvalue()

        response = self.client.post(
            "/api/v1/submissions/upload-and-evaluate",
            files={"file": ("uncropped.png", img_bytes, "image/png")},
            data={
                "rubrica_id": 1,
                "etapa": "BACH",
                "modo_evaluacion": "COMBINADO"
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("La imagen parece no estar recortada", response.json()["detail"])

    def test_upload_and_evaluate_success_pdf(self):
        """Valida que la subida de un PDF no aplique la regla de proporciones de imagen."""
        file_content = b"%PDF-1.4 fake pdf content"
        
        response = self.client.post(
            "/api/v1/submissions/upload-and-evaluate",
            files={"file": ("examen.pdf", file_content, "application/pdf")},
            data={
                "rubrica_id": 1,
                "etapa": "BACH",
                "modo_evaluacion": "COMBINADO"
            }
        )

        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn("transcription", data["resultado_ia"])

    def test_upload_and_evaluate_invalid_adaptaciones(self):
        """Valida que pasar un JSON corrupto de adaptaciones retorne HTTP 400."""
        img = Image.new("RGB", (100, 100), color="white")
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format="PNG")
        img_bytes = img_byte_arr.getvalue()

        response = self.client.post(
            "/api/v1/submissions/upload-and-evaluate",
            files={"file": ("cropped.png", img_bytes, "image/png")},
            data={
                "rubrica_id": 1,
                "etapa": "BACH",
                "adaptaciones_alumno": "esto-no-es-json"
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("debe ser un JSON válido", response.json()["detail"])


if __name__ == "__main__":
    unittest.main()
