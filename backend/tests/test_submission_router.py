import os
import unittest
import io
from fastapi.testclient import TestClient
from backend.main import app
from backend.services.auth_service import get_current_profesor

class MockProfesor:
    id = 1
    email = "profesor@edu.xunta.es"
    nombre = "Alba Camiña"

class TestSubmissionRouter(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        # Override the auth dependency to bypass JWT checking
        app.dependency_overrides[get_current_profesor] = lambda: MockProfesor()
        
    def tearDown(self):
        # Clean up overrides
        app.dependency_overrides.clear()
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
        # 26 MB of dummy data
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

if __name__ == "__main__":
    unittest.main()
