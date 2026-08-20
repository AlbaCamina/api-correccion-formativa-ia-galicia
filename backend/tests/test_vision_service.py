import unittest
from unittest.mock import patch, MagicMock
import os

from backend.services.vision_service import transcribir_imagen

class TestVisionService(unittest.IsolatedAsyncioTestCase):
    
    @patch.dict(os.environ, {"LLM_PROVIDER": "mock"})
    async def test_transcribir_imagen_mock(self):
        """Valida que en modo mock retorne la transcripción simulada."""
        result = await transcribir_imagen(b"fake_image_bytes")
        self.assertIn("Examen de Filosofía", result)
        self.assertIn("La luz nos permite ver las ideas", result)

    @patch.dict(os.environ, {"LLM_PROVIDER": "openai", "OPENAI_API_KEY": "fake_key_12345"})
    @patch("backend.services.vision_service.get_vision_client")
    async def test_transcribir_imagen_openai_success(self, mock_get_client):
        """Valida que en modo openai llame al cliente de OpenAI correctamente y devuelva la transcripción."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_message.content = "Transcripción real de prueba"
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        
        mock_client.chat.completions.create.return_value = mock_response

        result = await transcribir_imagen(b"fake_image_bytes")

        self.assertEqual(result, "Transcripción real de prueba")
        mock_client.chat.completions.create.assert_called_once()
        
        # Verificar los argumentos de la llamada
        args, kwargs = mock_client.chat.completions.create.call_args
        self.assertEqual(kwargs["model"], "gpt-4o-mini")
        self.assertEqual(kwargs["temperature"], 0.0)
        messages = kwargs["messages"]
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]["role"], "user")
        self.assertTrue(any(item["type"] == "image_url" for item in messages[0]["content"]))

    @patch.dict(os.environ, {"LLM_PROVIDER": "openai", "OPENAI_API_KEY": "fake_key_12345"})
    @patch("backend.services.vision_service.get_vision_client")
    async def test_transcribir_imagen_openai_error(self, mock_get_client):
        """Valida que si OpenAI falla, se capture la excepción y lance RuntimeError."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("OpenAI API Down")

        with self.assertRaises(RuntimeError) as context:
            await transcribir_imagen(b"fake_image_bytes")
            
        self.assertIn("Error en el servicio de transcripción de imagen", str(context.exception))

if __name__ == "__main__":
    unittest.main()
