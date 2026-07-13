from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from backend.routers import evaluation_router

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = FastAPI(
    title="API de Corrección Formativa con IA - Galicia",
    description="Backend oficial para el sistema de corrección formativa adaptada al Decreto 157/2022 de la Xunta de Galicia.",
    version="0.1-001",
)

app.include_router(evaluation_router)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configurable en producción según la URL de la PWA
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """
    Endpoint de salud del backend para verificar el correcto funcionamiento del servidor.
    """
    return {
        "status": "ok",
        "version": "0.1-001",
        "service": "api-correccion-formativa-ia-galicia"
    }
