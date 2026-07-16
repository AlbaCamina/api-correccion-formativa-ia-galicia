import os
import uuid
from fastapi import APIRouter, Body, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session

from backend.models.database import get_db
from backend.models.submission import (
    ChangeLog,
    FeedForwardVerificadoRequest,
    Submission,
    SubmissionResponse,
)
from backend.models.user import Profesor
from backend.services.auth_service import get_current_profesor

router = APIRouter(
    prefix="/api/v1/submissions",
    tags=["submissions"],
)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".heic", ".pdf"}
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB

# Transiciones válidas de estado_feed_forward (D-026)
FEED_FORWARD_TRANSITIONS: dict[str, str] = {
    "PENDIENTE": "REALIZADO_ALUMNO",
    "REALIZADO_ALUMNO": "VERIFICADO_EN_PRUEBA_SIGUIENTE",
}


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


@router.patch("/{submission_id}/feed-forward/realizado", response_model=SubmissionResponse)
def marcar_feed_forward_realizado(
    submission_id: str,
    db: Session = Depends(get_db),
    current_profesor: Profesor = Depends(get_current_profesor),
):
    """
    Marca el Siguiente Paso Accionable como realizado por el alumno (proxy docente).
    Transición válida: PENDIENTE -> REALIZADO_ALUMNO.
    Registra la transición en ChangeLog con actor humano explícito (ADR D-026, D-002).
    """
    sub = db.query(Submission).filter(Submission.id == submission_id).first()
    if not sub:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entrega no encontrada.")
    if sub.profesor_id != current_profesor.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso sobre esta entrega.")

    estado_destino = FEED_FORWARD_TRANSITIONS.get(sub.estado_feed_forward)
    if estado_destino != "REALIZADO_ALUMNO":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Transición no permitida desde el estado actual '{sub.estado_feed_forward}'.",
        )

    estado_anterior = sub.estado_feed_forward
    sub.estado_feed_forward = "REALIZADO_ALUMNO"

    log = ChangeLog(
        submission_id=sub.id,
        accion="FEED_FORWARD_REALIZADO",
        actor=f"PROFESOR_ID_{current_profesor.id}",
        datos_anteriores={"estado_feed_forward": estado_anterior},
        datos_nuevos={"estado_feed_forward": sub.estado_feed_forward},
        audit_metadata=None,
    )
    db.add(log)
    db.commit()
    db.refresh(sub)
    return sub


@router.patch("/{submission_id}/feed-forward/verificado", response_model=SubmissionResponse)
def confirmar_feed_forward_verificado(
    submission_id: str,
    body: FeedForwardVerificadoRequest = Body(default=None),
    db: Session = Depends(get_db),
    current_profesor: Profesor = Depends(get_current_profesor),
):
    """
    Confirma que la mejora del Feed Forward fue verificada en la siguiente prueba.
    Transición válida: REALIZADO_ALUMNO -> VERIFICADO_EN_PRUEBA_SIGUIENTE.
    El LLM puede haber propuesto la verificación, pero solo el profesor puede confirmarla.
    La señal de IA se traza en metadata, nunca como actor (ADR D-026, D-002, AI Act).
    """
    sub = db.query(Submission).filter(Submission.id == submission_id).first()
    if not sub:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entrega no encontrada.")
    if sub.profesor_id != current_profesor.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso sobre esta entrega.")

    estado_destino = FEED_FORWARD_TRANSITIONS.get(sub.estado_feed_forward)
    if estado_destino != "VERIFICADO_EN_PRUEBA_SIGUIENTE":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Transición no permitida desde el estado actual '{sub.estado_feed_forward}'.",
        )

    body = body or FeedForwardVerificadoRequest()
    estado_anterior = sub.estado_feed_forward
    sub.estado_feed_forward = "VERIFICADO_EN_PRUEBA_SIGUIENTE"

    log = ChangeLog(
        submission_id=sub.id,
        accion="FEED_FORWARD_VERIFICADO",
        actor=f"PROFESOR_ID_{current_profesor.id}",
        datos_anteriores={"estado_feed_forward": estado_anterior},
        datos_nuevos={"estado_feed_forward": sub.estado_feed_forward},
        audit_metadata={
            "ia_propuso_verificacion": body.ia_propuso_verificacion,
            "evaluation_id": body.evaluation_id,
        },
    )
    db.add(log)
    db.commit()
    db.refresh(sub)
    return sub
