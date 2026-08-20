import os
import uuid
import json
import io
from fastapi import APIRouter, Body, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from PIL import Image

from typing import Optional, List, Literal
from pydantic import BaseModel, Field
from backend.models.database import get_db
from backend.models.submission import (
    ChangeLog,
    FeedForwardVerificadoRequest,
    Submission,
    SubmissionResponse,
    Evaluacion,
    EvaluacionResponse,
)
from backend.models.user import Profesor
from backend.models.marco import MarcoEvaluacion, Etapa
from backend.models.rubrica import RubricaDocente
from backend.services.auth_service import get_current_profesor
from backend.services.storage_service import storage_service
from backend.services.vision_service import transcribir_imagen
from backend.services.llm_client import evaluate_answer

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

    try:
        url = await storage_service.upload_file(file, ext)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    return {
        "original_filename": filename,
        "saved_filename": os.path.basename(url),
        "url": url
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


class ApproveRequest(BaseModel):
    nota_final: Optional[float] = Field(None, description="Nota final opcional asignada por el docente.")


@router.patch("/{submission_id}/approve", response_model=SubmissionResponse)
def aprobar_submission(
    submission_id: str,
    body: Optional[ApproveRequest] = None,
    db: Session = Depends(get_db),
    current_profesor: Profesor = Depends(get_current_profesor),
):
    """
    Aprueba la evaluación de una entrega (Human-in-the-Loop).
    Transiciona el estado de la entrega de REVIEW a GRADED.
    Registra en ChangeLog la acción EVALUACION_APROBADA con el actor docente.
    """
    sub = db.query(Submission).filter(Submission.id == submission_id).first()
    if not sub:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entrega no encontrada.")
    if sub.profesor_id != current_profesor.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso sobre esta entrega.")

    if sub.estado != "REVIEW":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"La entrega debe estar en estado 'REVIEW' para ser aprobada. Estado actual: '{sub.estado}'.",
        )

    estado_anterior = sub.estado
    sub.estado = "GRADED"

    # Buscar la evaluación correspondiente para marcarla como aprobada
    evaluacion = db.query(Evaluacion).filter(Evaluacion.submission_id == sub.id).order_by(Evaluacion.id.desc()).first()
    if evaluacion:
        evaluacion.aprobado_por_profesor = True
        if body and body.nota_final is not None:
            evaluacion.nota_final = body.nota_final
        elif evaluacion.nota_final is None:
            # Si no se provee nota_final e intentamos usar la de la IA
            evaluacion.nota_final = evaluacion.resultado_ia.get("calificacion_numerica")

    log = ChangeLog(
        submission_id=sub.id,
        accion="EVALUACION_APROBADA",
        actor=f"PROFESOR_ID_{current_profesor.id}",
        datos_anteriores={"estado": estado_anterior},
        datos_nuevos={"estado": sub.estado},
        audit_metadata={
            "actor_id": current_profesor.id,
            "actor_tipo": "profesor"
        },
    )
    db.add(log)
    db.commit()
    db.refresh(sub)
    return sub


@router.get("", response_model=List[SubmissionResponse])
def listar_submissions(
    estado: Optional[str] = None,
    db: Session = Depends(get_db),
    current_profesor: Profesor = Depends(get_current_profesor),
):
    """
    Lista las entregas que pertenecen al profesor autenticado.
    Soporta filtro opcional por estado en base de datos.
    """
    query = db.query(Submission).filter(Submission.profesor_id == current_profesor.id)
    if estado:
        query = query.filter(Submission.estado == estado)
    return query.all()


def validar_recorte_cabecera(file_bytes: bytes, filename: str):
    _, ext = os.path.splitext(filename.lower())
    if ext in {".pdf"}:
        return  # No se valida en PDF
    
    try:
        image = Image.open(io.BytesIO(file_bytes))
        width, height = image.size
        # El ratio estándar A4 es 1.414. Si se recortó el 20%, el ratio resultante es <= 1.13.
        # Definimos un límite de 1.20 para la validación (Privacy by Design).
        ratio = height / width
        if ratio > 1.20:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La imagen parece no estar recortada. El alto de la imagen excede el 80% de la proporción esperada (Privacy by Design)."
            )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al procesar la imagen para validar sus proporciones."
        )


@router.post("/upload-and-evaluate", response_model=EvaluacionResponse, status_code=status.HTTP_201_CREATED)
async def upload_and_evaluate(
    file: UploadFile = File(...),
    rubrica_id: int = Form(...),
    marco_id: Optional[int] = Form(None),
    etapa: Etapa = Form(...),
    modo_evaluacion: Optional[Literal["COMBINADO", "AUDITORIA_CURRICULAR"]] = Form("COMBINADO"),
    question: Optional[str] = Form(None),
    alumno_id: Optional[str] = Form(None),
    adaptaciones_alumno: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_profesor: Profesor = Depends(get_current_profesor)
):
    """
    Pipeline unificado de corrección multimodal:
    1. Valida el formato del archivo y su tamaño (máx 25MB).
    2. Valida las proporciones de la imagen (exige recorte en el cliente / Privacy by Design).
    3. Guarda la imagen localmente/nube de forma segura.
    4. Envía la imagen al servicio de transcripción (vision_service).
    5. Crea la Submission en la base de datos (estado ANALYZING).
    6. Invoca al LLM (llm_client.evaluate_answer) para la evaluación.
    7. Registra la Evaluacion y el ChangeLog en la base de datos (estado REVIEW).
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

    # Leer los bytes del archivo
    file_bytes = await file.read()
    await file.seek(0)  # Resetear cursor del archivo para storage_service

    # Validar tamaño
    file_size = len(file_bytes)
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El archivo excede el límite máximo de 25 MB (Tamaño subido: {file_size / (1024 * 1024):.2f} MB)."
        )

    # Validar proporciones (recorte de cabecera en cliente)
    validar_recorte_cabecera(file_bytes, filename)

    # Parsear adaptaciones curriculares si vienen como string JSON
    adaptaciones = None
    if adaptaciones_alumno:
        try:
            adaptaciones = json.loads(adaptaciones_alumno)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El campo adaptaciones_alumno debe ser un JSON válido."
            )

    # 1. Recuperar y verificar la rúbrica
    rubrica = db.query(RubricaDocente).filter(
        RubricaDocente.id == rubrica_id,
        RubricaDocente.profesor_id == current_profesor.id
    ).first()
    if not rubrica:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La rúbrica especificada no existe o no tienes autorización para usarla."
        )

    # 2. Recuperar el marco si aplica
    marco = None
    if marco_id is not None:
        marco = db.query(MarcoEvaluacion).filter(
            MarcoEvaluacion.id == marco_id,
            MarcoEvaluacion.estado_activo == True
        ).first()
        if not marco:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El marco de evaluación legislativo especificado no existe o no está activo."
            )
        if marco.etapa != etapa.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"La etapa declarada '{etapa.value}' no coincide con la etapa del marco normativo '{marco.etapa}'."
            )

    # 3. Guardar el archivo en el storage service
    try:
        url = await storage_service.upload_file(file, ext)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al almacenar el archivo: {str(e)}"
        )

    # 4. Transcribir la imagen
    try:
        transcription = await transcribir_imagen(file_bytes)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error durante la transcripción de imagen: {str(e)}"
        )

    if not transcription.strip():
        transcription = "[ILEGIBLE]"

    # 5. Crear registro Submission en la BD (estado ANALYZING)
    submission = Submission(
        profesor_id=current_profesor.id,
        marco_id=marco.id if marco else None,
        rubrica_id=rubrica.id,
        alumno_id=alumno_id,
        adaptaciones_alumno=adaptaciones,
        estado="ANALYZING"
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

    # 6. Construir prompt para la evaluación con el LLM
    criterios_format = []
    for c in rubrica.criterios:
        codigo = c.get('criterio_codigo')
        codigo_str = f" [{codigo}]" if codigo else ""
        comps = c.get('competencias_clave')
        comps_str = f" (Competencias: {', '.join(comps)})" if comps else ""
        peso = c.get('peso')
        peso_str = f" (Peso: {peso}%)" if peso is not None else ""
        criterios_format.append(f"- Criterio {c.get('id', '')}{codigo_str} ({c.get('nombre', '')}): {c.get('descripcion', '')}{peso_str}{comps_str}")
    
    rubric_str = "\n".join(criterios_format)

    adaptaciones_str = ""
    if adaptaciones:
        adaptaciones_str += "\n\nADAPTACIONES CURRICULARES DEL ALUMNO APLICADAS (NEAE/NEE):\n"
        for k, v in adaptaciones.items():
            adaptaciones_str += f"- {k}: {v}\n"
        if adaptaciones.get("excluir_ortografia") is True:
            adaptaciones_str += (
                "\nINSTRUCCIÓN DE ADAPTACIÓN CRÍTICA (RGPD/NEAE):\n"
                "El alumno tiene adaptaciones curriculares oficiales por dificultades de aprendizaje (ej. dislexia).\n"
                "1. Identifica y lista TODAS las faltas de ortografía o gramática detectadas en la respuesta del alumno en el campo 'ortografia_detectada'.\n"
                "2. Registra esas mismas faltas de ortografía en el campo 'errores_excluidos_por_adaptacion'.\n"
                "3. Asegúrate de que estas faltas de ortografía NO afecten ni penalicen la puntuación final de ningún criterio de la rúbrica, ni influyan negativamente en la calificación cualitativa general.\n"
                "4. Si creas marcadores visuales para estos errores de ortografía excluidos, clasifícalos con tipo 'error_excluido' (en lugar de 'ERROR') para que la PWA pueda mostrarlos en gris/neutro.\n"
            )

    if marco:
        marco_str = f"Currículo Oficial Xunta de Galicia ({marco.asignatura} - {marco.curso}):\n"
        marco_str += json.dumps(marco.rubrica_completa, indent=2, ensure_ascii=False)
        
        if modo_evaluacion == "COMBINADO":
            rubric_prompt = (
                f"MODO DE EVALUACIÓN: COMBINADO\n"
                f"Instrucción: Fusiona de forma aditiva los saberes básicos oficiales y la rúbrica del docente para calificar.\n\n"
                f"Rúbrica de la Profesora:\n{rubric_str}\n\n"
                f"{marco_str}"
            )
        else:  # AUDITORIA_CURRICULAR
            rubric_prompt = (
                f"MODO DE EVALUACIÓN: AUDITORIA_CURRICULAR\n"
                f"Instrucción: Evalúa la entrega usando la rúbrica de la profesora. Además, audita si la rúbrica docente omite saberes obligatorios o contradice la ley, reportando en 'teacherSummary' cualquier brecha curricular de forma pedagógica.\n\n"
                f"Rúbrica de la Profesora:\n{rubric_str}\n\n"
                f"{marco_str}"
            )
    else:
        # Modo Rúbrica Pura (sin marco normativo)
        rubric_prompt = (
            f"MODO DE EVALUACIÓN: RÚBRICA PURA (Evaluación General)\n"
            f"Instrucción: Corrige la entrega del alumno utilizando única y exclusivamente los criterios de la rúbrica de la profesora.\n\n"
            f"Rúbrica de la Profesora:\n{rubric_str}"
        )

    rubric_prompt += adaptaciones_str

    # 7. Invocar al motor LLM pasándole la transcripción obtenida
    try:
        resultado = await evaluate_answer(
            student_answer=transcription,
            rubric=rubric_prompt,
            question=question or "",
            etapa=etapa
        )
    except Exception as e:
        submission.estado = "FAILED"
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error durante el análisis del motor de IA: {str(e)}"
        )

    # Forzar que la transcripción en el resultado sea exactamente la transcrita
    resultado.transcription = transcription

    # 8. Guardar la evaluación y actualizar estado a REVIEW (HitL)
    evaluacion = Evaluacion(
        submission_id=submission.id,
        resultado_ia=resultado.model_dump(),
        nota_final=None,
        aprobado_por_profesor=False
    )
    db.add(evaluacion)

    # Loguear la acción en el changelog de auditoría
    log_entry = ChangeLog(
        submission_id=submission.id,
        accion="IA_EVALUATION",
        actor="IA",
        datos_anteriores=None,
        datos_nuevos={"estado": "REVIEW", "resultado_ia": resultado.model_dump()},
        audit_metadata={"url_archivo": url}
    )
    db.add(log_entry)

    submission.estado = "REVIEW"
    db.commit()
    db.refresh(evaluacion)
    
    return evaluacion


