from typing import Optional, Literal
import json
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from backend.models.database import get_db
from backend.models.user import Profesor
from backend.models.marco import MarcoEvaluacion
from backend.models.rubrica import RubricaDocente
from backend.models.submission import Submission, Evaluacion, ChangeLog, EvaluacionResponse
from backend.services.auth_service import get_current_profesor
from backend.services.llm_client import evaluate_answer

router = APIRouter(
    prefix="/api/v1",
    tags=["evaluation"],
)

class EvaluationRequest(BaseModel):
    student_answer: str = Field(..., description="Texto de la respuesta dada por el estudiante o transcripción de la prueba.")
    rubrica_id: int = Field(..., description="ID de la rúbrica del docente para evaluar.")
    marco_id: Optional[int] = Field(None, description="ID del marco normativo oficial (dejar null para Rúbrica Pura).")
    modo_evaluacion: Optional[Literal["COMBINADO", "AUDITORIA_CURRICULAR"]] = Field("COMBINADO", description="Estrategia de interacción con el marco legal.")
    question: Optional[str] = Field(None, description="Pregunta, reto o enunciado opcional del examen.")
    alumno_id: Optional[str] = Field(None, max_length=100, description="Identificador seudonimizado del alumno para control de RGPD.")
    adaptaciones_alumno: Optional[dict] = Field(None, description="Configuración de adaptaciones curriculares NEAE si aplican.")

@router.post("/evaluate", response_model=EvaluacionResponse, status_code=status.HTTP_201_CREATED)
async def evaluate_submission(
    request: EvaluationRequest,
    db: Session = Depends(get_db),
    current_profesor: Profesor = Depends(get_current_profesor)
):
    """
    Endpoint de evaluación conectado a base de datos (copiloto formativo).
    1. Recupera la rúbrica de la profesora (validando propiedad).
    2. Si se proporciona marco_id, lo recupera e inyecta en el prompt en base al modo.
    3. Registra la Submission en base de datos.
    4. Invoca al LLM y guarda los resultados estructurados (Evaluacion) y el ChangeLog.
    """
    if not request.student_answer.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La respuesta del estudiante no puede estar vacía."
        )

    # 1. Recuperar y verificar la rúbrica
    rubrica = db.query(RubricaDocente).filter(
        RubricaDocente.id == request.rubrica_id,
        RubricaDocente.profesor_id == current_profesor.id
    ).first()
    if not rubrica:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La rúbrica especificada no existe o no tienes autorización para usarla."
        )

    # 2. Recuperar el marco si aplica
    marco = None
    if request.marco_id is not None:
        marco = db.query(MarcoEvaluacion).filter(
            MarcoEvaluacion.id == request.marco_id,
            MarcoEvaluacion.estado_activo == True
        ).first()
        if not marco:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El marco de evaluación legislativo especificado no existe o no está activo."
            )

    # 3. Crear el registro de la entrega en estado ANALYZING
    submission = Submission(
        profesor_id=current_profesor.id,
        marco_id=marco.id if marco else None,
        rubrica_id=rubrica.id,
        alumno_id=request.alumno_id,
        adaptaciones_alumno=request.adaptaciones_alumno,
        estado="ANALYZING"
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

    # 4. Construir la rúbrica detallada para el prompt del LLM
    rubric_str = "\n".join([
        f"- Criterio {c['id']} ({c['nombre']}): {c['descripcion']} (Peso: {c['peso']}%)"
        for c in rubrica.criterios
    ])

    if marco:
        marco_str = f"Currículo Oficial Xunta de Galicia ({marco.asignatura} - {marco.curso}):\n"
        marco_str += json.dumps(marco.rubrica_completa, indent=2, ensure_ascii=False)
        
        if request.modo_evaluacion == "COMBINADO":
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

    # 5. Invocar al motor LLM
    try:
        resultado = await evaluate_answer(
            student_answer=request.student_answer,
            rubric=rubric_prompt,
            question=request.question or ""
        )
    except Exception as e:
        # Marcar la entrega como fallida en base de datos si el LLM falla
        submission.estado = "FAILED"
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error durante el análisis del motor de IA: {str(e)}"
        )

    # 6. Guardar la evaluación y actualizar estado a REVIEW (Human-in-the-Loop)
    evaluacion = Evaluacion(
        submission_id=submission.id,
        resultado_ia=resultado.model_dump(),
        nota_final=None,  # La profesora asignará la definitiva al aprobar (HitL D-002)
        aprobado_por_profesor=False
    )
    db.add(evaluacion)

    # Loguear la acción en el changelog de auditoría
    log_entry = ChangeLog(
        submission_id=submission.id,
        accion="IA_EVALUATION",
        actor="IA",
        datos_anteriores=None,
        datos_nuevos={"estado": "REVIEW", "resultado_ia": resultado.model_dump()}
    )
    db.add(log_entry)

    # Actualizar estado de submission
    submission.estado = "REVIEW"
    db.commit()
    db.refresh(evaluacion)

    return evaluacion

