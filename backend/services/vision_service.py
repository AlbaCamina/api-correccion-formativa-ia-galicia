import base64
import os
import logging
from openai import OpenAI

logger = logging.getLogger("backend.services.vision_service")
logger.setLevel(logging.INFO)

if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(ch)

def get_vision_client() -> OpenAI:
    """
    Retorna el cliente de OpenAI configurado adecuadamente.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "tu_api_key_de_openai_aqui":
        raise ValueError("Falta configurar OPENAI_API_KEY en las variables de entorno.")
    return OpenAI(api_key=api_key)

async def transcribir_imagen(imagen_bytes: bytes, mime_type: str = "image/jpeg") -> str:
    """
    Transcribe el contenido de un examen manuscrito a partir de sus bytes usando OpenAI Vision (gpt-4o-mini).
    Soporta modo MOCK para pruebas y CI/CD sin dependencia de red.
    Si hay tramos ilegibles, los marcará con [ILEGIBLE].
    """
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    model_name = os.getenv("LLM_MODEL", "gpt-4o-mini")

    if provider == "mock":
        logger.info("Modo MOCK activado en vision_service. Retornando transcripción simulada.")
        return (
            "Examen de Filosofía (Mito de la Caverna)\n"
            "Pregunta: Explica el significado del sol y la luz en el mito.\n"
            "Respuesta: El sol representa la Idea de Bien, que es la causa de todo lo recto y bello. "
            "La luz nos permite ver las ideas. El esfuerzo para salir es difícil y requiere un gran esfuerzo."
        )

    client = get_vision_client()
    base64_image = base64.b64encode(imagen_bytes).decode('utf-8')
    data_url = f"data:{mime_type};base64,{base64_image}"

    prompt = (
        "Eres un transcriptor experto en caligrafía manuscrita escolar. "
        "Tu única tarea es transcribir de forma extremadamente fiel y exacta todo el texto manuscrito "
        "que aparece en esta imagen del examen. "
        "Reglas estrictas:\n"
        "1. No añadas introducciones, explicaciones, preámbulos ni comentarios. Devuelve SOLO el texto transcrito.\n"
        "2. Respeta los saltos de párrafo del alumno si los hay.\n"
        "3. Si hay palabras, tachones o tramos enteros que son completamente ilegibles, reemplázalos exactamente por la palabra '[ILEGIBLE]'.\n"
        "4. Mantén los errores ortográficos y la puntuación original del estudiante (no los corrijas)."
    )

    try:
        logger.info(f"Enviando imagen a OpenAI Vision usando el modelo {model_name}...")
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": data_url
                            }
                        }
                    ]
                }
            ],
            temperature=0.0,  # Queremos transcripción determinista y fiel
        )
        transcription = response.choices[0].message.content
        if not transcription:
            raise ValueError("OpenAI Vision retornó una transcripción vacía.")
            
        logger.info("Transcripción completada con éxito.")
        return transcription.strip()

    except Exception as e:
        logger.error(f"Fallo al transcribir la imagen con OpenAI Vision: {e}")
        raise RuntimeError(f"Error en el servicio de transcripción de imagen: {e}")
