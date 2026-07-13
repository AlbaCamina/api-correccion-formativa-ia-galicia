import os
import unittest
from fastapi.testclient import TestClient
from backend.main import app

class TestEvaluationRouter(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        # Configurar LLM_PROVIDER=mock para tests unitarios/integración
        self.original_provider = os.getenv("LLM_PROVIDER")
        os.environ["LLM_PROVIDER"] = "mock"

    def tearDown(self):
        if self.original_provider:
            os.environ["LLM_PROVIDER"] = self.original_provider
        else:
            os.environ.pop("LLM_PROVIDER", None)

    def test_evaluate_endpoint_success(self):
        """Valida que POST /api/v1/evaluate devuelve correctamente la evaluación formativa mockeada."""
        payload = {
            "student_answer": "El prisionero sale a la luz exterior y ve el sol...",
            "rubric": "Precisión conceptual (0-5 pts).",
            "question": "¿Qué simboliza la salida del prisionero?"
        }
        response = self.client.post("/api/v1/evaluate", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Validaciones de estructura del contrato
        self.assertIn("transcription", data)
        self.assertEqual(data["calificacion_cualitativa"], "NT")
        self.assertEqual(data["visualMarkers"], [])
        self.assertIn("siguiente_paso_accionable", data)
        self.assertIn("qualitativeAnalysis", data)
        self.assertEqual(data["confidence_score"], 0.92)

    def test_evaluate_endpoint_validation_error(self):
        """Valida que enviar datos vacíos lanza error 400."""
        # 1. student_answer vacío
        payload = {
            "student_answer": "",
            "rubric": "Criterios básicos"
        }
        response = self.client.post("/api/v1/evaluate", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("La respuesta del estudiante no puede estar vacía", response.json()["detail"])

        # 2. rubric vacía
        payload = {
            "student_answer": "Respuesta correcta",
            "rubric": "   "
        }
        response = self.client.post("/api/v1/evaluate", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("La rúbrica o criterios de evaluación no pueden estar vacíos", response.json()["detail"])

if __name__ == "__main__":
    unittest.main()
