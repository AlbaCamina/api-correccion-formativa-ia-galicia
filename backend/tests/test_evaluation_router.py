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

    def test_evaluate_endpoint_invalid_pydantic_payload(self):
        """Valida que enviar un payload malformado lanza HTTP 422 con formato {error, detail}."""
        # Enviamos un campo incorrecto para forzar error de validación de FastAPI / Pydantic
        payload = {
            "student_answer_incorrect_field": "Hola",
            "rubric": "Rúbrica"
        }
        response = self.client.post("/api/v1/evaluate", json=payload)
        self.assertEqual(response.status_code, 422)
        data = response.json()
        self.assertEqual(data["error"], "Error de validación")
        self.assertIn("detail", data)

    def test_startup_validation_missing_key(self):
        """Valida que startup_validation aborta si falta la key correspondiente en la configuración."""
        import asyncio
        from backend.main import startup_validation
        
        # Guardar valores originales
        orig_provider = os.environ.get("LLM_PROVIDER")
        orig_openai_key = os.environ.get("OPENAI_API_KEY")
        
        try:
            # Forzar OpenAI sin clave
            os.environ["LLM_PROVIDER"] = "openai"
            os.environ["OPENAI_API_KEY"] = "tu_api_key_de_openai_aqui"
            with self.assertRaises(RuntimeError):
                asyncio.run(startup_validation())
                
            # Forzar Groq sin clave
            os.environ["LLM_PROVIDER"] = "groq"
            os.environ["GROQ_API_KEY"] = "tu_api_key_de_groq_aqui"
            with self.assertRaises(RuntimeError):
                asyncio.run(startup_validation())
                
            # Forzar proveedor inválido
            os.environ["LLM_PROVIDER"] = "invalid_llm"
            with self.assertRaises(RuntimeError):
                asyncio.run(startup_validation())
                
        finally:
            # Restaurar
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
