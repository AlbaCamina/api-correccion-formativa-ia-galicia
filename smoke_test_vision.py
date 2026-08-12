import asyncio
import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno ANTES de importar los servicios
load_dotenv()

# Sobrescribir siempre con el modelo Vision independientemente de lo que haya en .env
os.environ["LLM_PROVIDER"] = "groq"
import base64
import httpx

async def run_vision_smoke_test():
    print("--- INICIANDO SMOKE TEST MULTIMODAL (v0.3) ---")
    # Forzar el modelo Vision independientemente de lo que haya en .env
    os.environ["LLM_PROVIDER"] = "openai"
    os.environ["LLM_MODEL"] = "gpt-4o-mini"
    
    print(f"Proveedor configurado: {os.environ.get('LLM_PROVIDER').upper()}")
    print(f"Modelo configurado: {os.environ.get('LLM_MODEL')}")
    
    # URL de imagen de prueba (reemplazamos Wikimedia por dummyimage para evitar error 429)
    image_url = "https://dummyimage.com/600x400/000/fff&text=Examen+de+prueba+para+IA"
    
    print("[!] Descargando imagen localmente para enviar en Base64 (evita 403 de Wikimedia)...")
    async with httpx.AsyncClient(follow_redirects=True) as client:
        # Simulamos un navegador para evitar bloqueos
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = await client.get(image_url, headers=headers)
        response.raise_for_status()
        base64_img = base64.b64encode(response.content).decode("utf-8")
        image_payload = f"data:image/jpeg;base64,{base64_img}"

    
    rubrica_test = """
    Criterios de Evaluación (ESO):
    - CRIT-1: Transcripción precisa del contenido manuscrito. (Peso: 50%)
    - CRIT-2: Identificación correcta de elementos visuales (trazos, correcciones). (Peso: 50%)
    """
    
    print(f"\n[!] Enviando imagen en Base64 a OpenAI (gpt-4o-mini)...")
    print("[!] Esperando respuesta (puede tardar unos segundos)...")
    
    try:
        from backend.services.llm_client import evaluate_answer
        resultado = await evaluate_answer(
            student_answer="",
            rubric=rubrica_test,
            question="Describe el contenido de la imagen de la forma más fiel posible y evalúalo.",
            etapa="ESO",
            image_url=image_payload
        )
        
        print("\n✅ ¡ÉXITO! JSON Pydantic devuelto correctamente.\n")
        
        print("=== TRANSCRIPCIÓN ===")
        print(resultado.transcription)
        print("\n=== CALIFICACIÓN ===")
        print(f"Nota: {resultado.calificacion_numerica} ({resultado.calificacion_cualitativa})")
        
        print("\n=== VISUAL MARKERS ===")
        if resultado.visualMarkers:
            for marker in resultado.visualMarkers:
                print(f"  📍 [X:{marker.x}%, Y:{marker.y}%] TIPO: {marker.type}")
                print(f"     Comentario: {marker.comment}")
        else:
            print("  ⚠️ No se generaron marcadores visuales (el array está vacío).")
            
        print("\n=== JSON COMPLETO ===")
        print(resultado.model_dump_json(indent=2))
            
    except Exception as e:
        print(f"\n❌ Error durante el test: {e}")

if __name__ == "__main__":
    if sys.platform == 'win32':
        # Evita errores de EventLoop en Windows con asyncio
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_vision_smoke_test())
