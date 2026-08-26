import os
import logging
from fastapi import FastAPI, Request, HTTPException
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from backend.routers import evaluation_router, auth_router, marco_router, rubrica_router, submission_router

# Configurar logging principal del servidor con marcas de tiempo (v0.1-005)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("backend.main")

# Cargar variables de entorno desde el archivo .env (v0.1-006)
load_dotenv()

async def startup_validation():
    """
    Valida en el arranque que las variables de entorno requeridas según el proveedor estén presentes.
    Si faltan, el servidor aborta el inicio del proceso.
    """
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    model = os.getenv("LLM_MODEL")

    logger.info("Validando configuración de variables de entorno al inicio...")
    logger.info(f"Proveedor configurado: {provider.upper()} | Modelo por defecto: {model}")

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "tu_api_key_de_openai_aqui":
            error_msg = "La variable OPENAI_API_KEY no está configurada o contiene el marcador por defecto."
            logger.critical(error_msg)
            raise RuntimeError(error_msg)
    elif provider == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or api_key == "tu_api_key_de_groq_aqui":
            error_msg = "La variable GROQ_API_KEY no está configurada o contiene el marcador por defecto."
            logger.critical(error_msg)
            raise RuntimeError(error_msg)
    elif provider == "mock":
        logger.info("El servidor arranca en modo SIMULACIÓN (MOCK). No se requieren claves API reales.")
    else:
        error_msg = f"El proveedor LLM_PROVIDER='{provider}' no está soportado."
        logger.critical(error_msg)
        raise RuntimeError(error_msg)

    secret_key = os.getenv("SECRET_KEY", "super-secret-key-galicia-2026-hitl-ninja")
    if secret_key == "super-secret-key-galicia-2026-hitl-ninja":
        error_msg = "La variable SECRET_KEY contiene el valor por defecto inseguro. Configura una clave secreta real en .env antes de desplegar."
        logger.critical(error_msg)
        raise RuntimeError(error_msg)

    logger.info("¡Validación de variables de entorno exitosa! El servidor está listo.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_validation()
    yield


app = FastAPI(
    title="API de Corrección Formativa con IA - Galicia",
    description="Backend oficial para el sistema de corrección formativa adaptada al Decreto 157/2022 de la Xunta de Galicia.",
    version="0.4.0",
    lifespan=lifespan,
)

# Registro de enrutadores
app.include_router(evaluation_router)
app.include_router(auth_router)
app.include_router(marco_router)
app.include_router(rubrica_router)
app.include_router(submission_router)

# Asegurar existencia del directorio y servir archivos de /uploads (simulando S3)
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")



# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# ==========================================
# GESTIÓN DE EXCEPCIONES Y FORMATO DE ERRORES (v0.1-005)
# ==========================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Handler para excepciones HTTP controladas.
    """
    logger.error(f"Error HTTP {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Error de solicitud" if exc.status_code < 500 else "Error interno del servidor",
            "detail": exc.detail
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handler para errores de validación de datos de entrada de Pydantic (HTTP 422).
    """
    logger.error(f"Error de validación de datos (422): {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "Error de validación",
            "detail": str(exc.errors())
        }
    )

@app.exception_handler(Exception)
async def universal_exception_handler(request: Request, exc: Exception):
    """
    Handler universal para capturar cualquier error no controlado y devolver HTTP 500.
    """
    logger.error(f"Excepción no controlada detectada: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Error interno del servidor",
            "detail": str(exc)
        }
    )

@app.get("/health")
async def health_check():
    """
    Endpoint de salud del backend para verificar el correcto funcionamiento del servidor.
    """
    return {
        "status": "ok",
        "version": "0.4.0",
        "service": "api-correccion-formativa-ia-galicia"
    }
