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

        self.submission = Submission(
            id="test-submission-uuid-001",
            profesor_id=1,
            rubrica_id=1,
            estado="REVIEW",
            estado_feed_forward="PENDIENTE",
        )
        self.db.add(self.submission)

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

    def test_evaluate_endpoint_success(self):
        """Valida que POST /api/v1/evaluate guarda la entrega y devuelve la evaluación formativa mockeada (v0.2)."""
        payload = {
            "student_answer": "El prisionero sale a la luz exterior y ve el sol...",
            "rubrica_id": 1,
            "etapa": "BACH",
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
        self.assertIsNone(resultado["calificacion_cualitativa"])
        self.assertEqual(resultado["calificacion_numerica"], 8.0)
        self.assertEqual(len(resultado["visualMarkers"]), 1)
        self.assertEqual(resultado["visualMarkers"][0]["type"], "error_excluido")
        self.assertIn("siguiente_paso_accionable", resultado)
        self.assertIn("qualitativeAnalysis", resultado)
        self.assertEqual(resultado["confidence_score"], 0.92)

    def test_evaluate_endpoint_validation_error(self):
        """Valida que enviar datos vacíos o sin rúbrica lanza error 400 o 404."""
        # 1. student_answer vacío -> 400
        payload = {
            "student_answer": "",
            "rubrica_id": 1,
            "etapa": "BACH"
        }
        response = self.client.post("/api/v1/evaluate", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("La respuesta del estudiante no puede estar vacía", response.json()["detail"])

        # 2. rubrica_id inexistente o de otro docente -> 404
        payload = {
            "student_answer": "Respuesta correcta",
            "rubrica_id": 999,
            "etapa": "BACH"
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

    def test_evaluate_endpoint_missing_etapa_validation_error(self):
        """Valida que omitir la etapa lanza error 422 (breaking change D-041)."""
        payload = {
            "student_answer": "Respuesta normal",
            "rubrica_id": 1
        }
        response = self.client.post("/api/v1/evaluate", json=payload)
        self.assertEqual(response.status_code, 422)
        self.assertIn("etapa", str(response.json()["detail"]))

    def test_evaluate_endpoint_cross_check_etapa_error(self):
        """Valida que si hay marco_id y la etapa del request difiere de la del marco, lanza 400 (D-041)."""
        payload = {
            "student_answer": "Respuesta",
            "rubrica_id": 1,
            "etapa": "ESO",  # Incompatible: el marco 1 tiene etapa='BACH'
            "marco_id": 1
        }
        response = self.client.post("/api/v1/evaluate", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("La etapa declarada 'ESO' no coincide con la etapa del marco normativo 'BACH'", response.json()["detail"])

    def test_startup_validation_missing_key(self):
        """Valida que startup_validation aborta si falta la key correspondiente en la configuración."""
        import asyncio
        from backend.main import startup_validation

        orig_provider = os.environ.get("LLM_PROVIDER")
        orig_openai_key = os.environ.get("OPENAI_API_KEY")
        orig_groq_key = os.environ.get("GROQ_API_KEY")

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
            if orig_groq_key:
                os.environ["GROQ_API_KEY"] = orig_groq_key
            else:
                os.environ.pop("GROQ_API_KEY", None)

    def test_startup_validation_default_secret_key(self):
        """Valida que startup_validation aborta si SECRET_KEY contiene el valor por defecto inseguro."""
        import asyncio
        from backend.main import startup_validation

        orig_secret = os.environ.get("SECRET_KEY")
        orig_provider = os.environ.get("LLM_PROVIDER")

        try:
            os.environ["LLM_PROVIDER"] = "mock"
            os.environ["SECRET_KEY"] = "super-secret-key-galicia-2026-hitl-ninja"
            with self.assertRaises(RuntimeError):
                asyncio.run(startup_validation())
        finally:
            if orig_secret:
                os.environ["SECRET_KEY"] = orig_secret
            else:
                os.environ.pop("SECRET_KEY", None)
            if orig_provider:
                os.environ["LLM_PROVIDER"] = orig_provider
            else:
                os.environ.pop("LLM_PROVIDER", None)

    # ==========================================
    # TESTS DE ENDPOINTS FEED FORWARD (D-026)
    # ==========================================

    def test_feed_forward_pendiente_a_realizado(self):
        """Transición válida: PENDIENTE -> REALIZADO_ALUMNO devuelve 200 y actualiza el estado."""
        response = self.client.patch("/api/v1/submissions/test-submission-uuid-001/feed-forward/realizado")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["estado_feed_forward"], "REALIZADO_ALUMNO")

    def test_feed_forward_realizado_a_verificado(self):
        """Transición válida: REALIZADO_ALUMNO -> VERIFICADO_EN_PRUEBA_SIGUIENTE devuelve 200."""
        self.client.patch("/api/v1/submissions/test-submission-uuid-001/feed-forward/realizado")
        response = self.client.patch(
            "/api/v1/submissions/test-submission-uuid-001/feed-forward/verificado",
            json={"ia_propuso_verificacion": True, "evaluation_id": 1},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["estado_feed_forward"], "VERIFICADO_EN_PRUEBA_SIGUIENTE")

    def test_feed_forward_salto_invalido_pendiente_a_verificado(self):
        """Transición inválida: PENDIENTE -> VERIFICADO_EN_PRUEBA_SIGUIENTE devuelve 409."""
        response = self.client.patch("/api/v1/submissions/test-submission-uuid-001/feed-forward/verificado")
        self.assertEqual(response.status_code, 409)

    def test_feed_forward_404_submission_inexistente(self):
        """Devuelve 404 si la submission no existe."""
        response = self.client.patch("/api/v1/submissions/no-existe/feed-forward/realizado")
        self.assertEqual(response.status_code, 404)

    def test_feed_forward_unauthorized(self):
        """Devuelve 403 si un profesor distinto al dueño intenta modificar el feed-forward."""
        profesor2 = Profesor(id=2, email="otradocente@edu.xunta.gal", nombre="María", hashed_password="hashed_mock")
        self.db.add(profesor2)
        self.db.commit()

        # Sobrescribir localmente la dependencia
        def override_get_current_profesor2():
            return profesor2

        app.dependency_overrides[get_current_profesor] = override_get_current_profesor2

        try:
            # Intentar marcar realizado
            response1 = self.client.patch("/api/v1/submissions/test-submission-uuid-001/feed-forward/realizado")
            self.assertEqual(response1.status_code, 403)

            # Intentar verificar
            response2 = self.client.patch(
                "/api/v1/submissions/test-submission-uuid-001/feed-forward/verificado",
                json={"ia_propuso_verificacion": True, "evaluation_id": 1}
            )
            self.assertEqual(response2.status_code, 403)
        finally:
            # Restaurar
            app.dependency_overrides[get_current_profesor] = lambda: self.profesor

    def test_feed_forward_changelog_persistido(self):
        """Verifica que la transición persiste una entrada en ChangeLog con actor y datos correctos."""
        self.client.patch("/api/v1/submissions/test-submission-uuid-001/feed-forward/realizado")

        log = (
            self.db.query(ChangeLog)
            .filter(
                ChangeLog.submission_id == "test-submission-uuid-001",
                ChangeLog.accion == "FEED_FORWARD_REALIZADO",
            )
            .first()
        )
        self.assertIsNotNone(log)
        self.assertEqual(log.actor, "PROFESOR_ID_1")
        self.assertEqual(log.datos_anteriores["estado_feed_forward"], "PENDIENTE")
        self.assertEqual(log.datos_nuevos["estado_feed_forward"], "REALIZADO_ALUMNO")
        self.assertIsNone(log.audit_metadata)

    def test_feed_forward_verificado_metadata_ia(self):
        """Verifica que audit_metadata registra la señal de IA sin hacerla actora de la transición."""
        self.client.patch("/api/v1/submissions/test-submission-uuid-001/feed-forward/realizado")
        self.client.patch(
            "/api/v1/submissions/test-submission-uuid-001/feed-forward/verificado",
            json={"ia_propuso_verificacion": True, "evaluation_id": 99},
        )

        log = (
            self.db.query(ChangeLog)
            .filter(
                ChangeLog.submission_id == "test-submission-uuid-001",
                ChangeLog.accion == "FEED_FORWARD_VERIFICADO",
            )
            .first()
        )
        self.assertIsNotNone(log)
        self.assertEqual(log.actor, "PROFESOR_ID_1")
        self.assertTrue(log.audit_metadata["ia_propuso_verificacion"])
        self.assertEqual(log.audit_metadata["evaluation_id"], 99)

    def test_approve_submission_success(self):
        """Aprobación exitosa: transiciona a GRADED, actualiza la evaluacion y crea el ChangeLog."""
        evaluacion = Evaluacion(
            submission_id="test-submission-uuid-001",
            resultado_ia={"calificacion_numerica": 8.0},
            aprobado_por_profesor=False
        )
        self.db.add(evaluacion)
        self.db.commit()

        payload = {"nota_final": 9.0}
        response = self.client.patch("/api/v1/submissions/test-submission-uuid-001/approve", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["estado"], "GRADED")

        # Verificar base de datos
        db_sub = self.db.query(Submission).filter(Submission.id == "test-submission-uuid-001").first()
        self.assertEqual(db_sub.estado, "GRADED")

        db_eval = self.db.query(Evaluacion).filter(Evaluacion.submission_id == "test-submission-uuid-001").first()
        self.assertTrue(db_eval.aprobado_por_profesor)
        self.assertEqual(db_eval.nota_final, 9.0)

        db_log = (
            self.db.query(ChangeLog)
            .filter(
                ChangeLog.submission_id == "test-submission-uuid-001",
                ChangeLog.accion == "EVALUACION_APROBADA"
            )
            .first()
        )
        self.assertIsNotNone(db_log)
        self.assertEqual(db_log.actor, "PROFESOR_ID_1")
        self.assertEqual(db_log.audit_metadata["actor_id"], 1)
        self.assertEqual(db_log.audit_metadata["actor_tipo"], "profesor")

    def test_approve_submission_invalid_state(self):
        """Intento de aprobación cuando el estado no es REVIEW devuelve 409."""
        sub = self.db.query(Submission).filter(Submission.id == "test-submission-uuid-001").first()
        sub.estado = "PENDING"
        self.db.commit()

        response = self.client.patch("/api/v1/submissions/test-submission-uuid-001/approve")
        self.assertEqual(response.status_code, 409)

    def test_approve_submission_unauthorized(self):
        """Intento de aprobación por parte de un profesor no propietario devuelve 403."""
        profesor2 = Profesor(id=2, email="otradocente@edu.xunta.gal", nombre="María", hashed_password="hashed_mock")
        self.db.add(profesor2)
        self.db.commit()

        # Sobrescribir localmente la dependencia
        def override_get_current_profesor2():
            return profesor2

        app.dependency_overrides[get_current_profesor] = override_get_current_profesor2

        try:
            response = self.client.patch("/api/v1/submissions/test-submission-uuid-001/approve")
            self.assertEqual(response.status_code, 403)
        finally:
            # Restaurar
            app.dependency_overrides[get_current_profesor] = lambda: self.profesor

    def test_listar_submissions_owner_only(self):
        """Devuelve solo las entregas del profesor autenticado."""
        # Submission ajena (profesor 2)
        sub_ajena = Submission(
            id="test-submission-uuid-ajena",
            profesor_id=2,
            rubrica_id=1,
            estado="REVIEW",
        )
        self.db.add(sub_ajena)
        self.db.commit()

        response = self.client.get("/api/v1/submissions")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Debe contener solo la del profesor 1
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], "test-submission-uuid-001")

    def test_listar_submissions_filter_estado(self):
        """Devuelve las entregas del profesor autenticado filtradas opcionalmente por estado."""
        # Crear otra submission del profesor 1 pero en estado GRADED
        sub_graded = Submission(
            id="test-submission-uuid-graded",
            profesor_id=1,
            rubrica_id=1,
            estado="GRADED",
        )
        self.db.add(sub_graded)
        self.db.commit()

        # 1. Filtrar por REVIEW
        response = self.client.get("/api/v1/submissions?estado=REVIEW")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], "test-submission-uuid-001")

        # 2. Filtrar por GRADED
        response = self.client.get("/api/v1/submissions?estado=GRADED")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], "test-submission-uuid-graded")

    def test_obtener_evaluacion_success(self):
        """Obtiene la evaluación de una entrega propia de forma exitosa."""
        resultado_mock = {
            "etapa": "BACH",
            "transcription": "Test",
            "rubricBreakdown": [
                {
                    "criterio_codigo": "FILO-B2.3",
                    "competencias_clave": ["CCL", "CC"],
                    "category": "Cat",
                    "score": 8.0,
                    "maxScore": 10.0,
                    "peso": 100.0,
                    "nivel_logro": 4,
                    "reasoning": "Reason"
                }
            ],
            "visualMarkers": [],
            "qualitativeAnalysis": {
                "strengths": ["Strength"],
                "improvementNeeds": {
                    "immediate": ["Immediate"],
                    "mediumLongTerm": ["Medium"]
                },
                "teacherSummary": "Summary"
            },
            "calificacion_numerica": 8.0,
            "calificacion_cualitativa": None,
            "siguiente_paso_accionable": "Siguiente paso",
            "confidence_score": 0.9
        }
        evaluacion = Evaluacion(
            submission_id="test-submission-uuid-001",
            resultado_ia=resultado_mock,
            aprobado_por_profesor=False
        )
        self.db.add(evaluacion)
        self.db.commit()

        response = self.client.get("/api/v1/evaluaciones/test-submission-uuid-001")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["submission_id"], "test-submission-uuid-001")
        self.assertFalse(data["aprobado_por_profesor"])

    def test_obtener_evaluacion_unauthorized(self):
        """Devuelve 403 si un profesor intenta acceder a la evaluación de una entrega ajena."""
        profesor2 = Profesor(id=2, email="otradocente@edu.xunta.gal", nombre="María", hashed_password="hashed_mock")
        self.db.add(profesor2)
        self.db.commit()

        # Sobrescribir localmente la dependencia
        def override_get_current_profesor2():
            return profesor2

        app.dependency_overrides[get_current_profesor] = override_get_current_profesor2

        try:
            response = self.client.get("/api/v1/evaluaciones/test-submission-uuid-001")
            self.assertEqual(response.status_code, 403)
        finally:
            # Restaurar
            app.dependency_overrides[get_current_profesor] = lambda: self.profesor


if __name__ == "__main__":
    unittest.main()
