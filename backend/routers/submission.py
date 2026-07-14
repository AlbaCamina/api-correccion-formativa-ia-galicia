import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from backend.models.user import Profesor
from backend.services.auth_service import get_current_profesor

router = APIRouter(
    prefix="/api/v1/submissions",
    tags=["submissions"],
)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".heic", ".pdf"}
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    current_profesor: Profesor = Depends(get_current_profesor)
):
    """
    Endpoint para subir imágenes o archivos PDF de exámenes.
    - Valida formato (JPG, PNG, HEIC, PDF).
    - Valida tamaño máximo de 25 MB.
    - Guarda localmente con un nombre UUID único en la carpeta /uploads.
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nombre de archivo inválido."
        )

    filename = file.filename
    _, ext = os.path.splitext(filename.lower())
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Formato de archivo '{ext}' no soportado. Formatos admitidos: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        )

    # Determinar el tamaño del archivo moviendo el cursor del archivo subyacente
    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell()
    file.file.seek(0)  # Resetear cursor al inicio

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El archivo excede el límite máximo de 25 MB (Tamaño subido: {file_size / (1024 * 1024):.2f} MB)."
        )

    # Crear directorio local si no existe
    uploads_dir = "uploads"
    os.makedirs(uploads_dir, exist_ok=True)

    # Generar nombre único con UUID para evitar colisiones
    saved_filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(uploads_dir, saved_filename)

    try:
        with open(file_path, "wb") as f:
            while chunk := await file.read(1024 * 1024):  # Chunked read de 1MB
                f.write(chunk)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fallo al escribir el archivo en disco: {str(e)}"
        )

    return {
        "original_filename": filename,
        "saved_filename": saved_filename,
        "url": f"/uploads/{saved_filename}"
    }
