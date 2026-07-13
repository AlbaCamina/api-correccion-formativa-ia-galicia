from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from backend.models.evaluation import EvaluacionIA
from backend.services.llm_client import evaluate_answer

router = APIRouter(
    prefix="/api/v1",
    tags=["evaluation"],
)

class EvaluationRequest(BaseModel):
    student_answer: str = Field(..., description="Texto de la respuesta dada por el estudiante.")
    rubric: str = Field(..., description="Criterios de evaluación o rúbrica de corrección.")
    question: Optional[str] = Field(None, description="Pregunta o enunciado opcional del examen.")

@router.post("/evaluate", response_model=EvaluacionIA)
async def evaluate_submission(request: EvaluationRequest):
    """
    Endpoint síncrono que recibe una respuesta de alumno y rúbrica,
    y devuelve la corrección estructurada con notas y Feed Forward formativo.
    """
    if not request.student_answer.strip():
        raise HTTPException(status_code=400, detail="La respuesta del estudiante no puede estar vacía.")
    if not request.rubric.strip():
        raise HTTPException(status_code=400, detail="La rúbrica o criterios de evaluación no pueden estar vacíos.")

    try:
        resultado = await evaluate_answer(
            student_answer=request.student_answer,
            rubric=request.rubric,
            question=request.question or ""
        )
        return resultado
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fallo en la corrección formativa: {str(e)}")
