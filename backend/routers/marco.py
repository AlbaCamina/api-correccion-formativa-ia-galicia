"""
Módulo de enrutamiento (FastAPI) para gestionar los Marcos de Evaluación oficiales.
Implementa el endpoint GET /api/v1/marcos para listar los marcos activos.
Hito [v0.2-003].
"""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.models.database import get_db
from backend.models.marco import MarcoEvaluacion, MarcoResponse

router = APIRouter(prefix="/api/v1/marcos", tags=["marcos_evaluacion"])


@router.get("", response_model=List[MarcoResponse])
def get_marcos_activos(db: Session = Depends(get_db)):
    """
    Devuelve la lista de todos los marcos de evaluación activos en la base de datos.
    Permite al profesor seleccionar la normativa legislativa de la Xunta de Galicia a aplicar.
    """
    marcos = db.query(MarcoEvaluacion).filter(MarcoEvaluacion.estado_activo == True).all()
    return marcos
