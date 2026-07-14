"""
Módulo de enrutamiento (FastAPI) para el CRUD completo de las Rúbricas del Docente.
Cumple con la Regla 2 (Modularidad Plana) ubicando en routers/ los endpoints de la API.
Garantiza que una rúbrica solo puede ser leída, editada o eliminada por su docente propietario.
Hito [v0.2-004] y ADR [D-027].
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.models.database import get_db
from backend.models.user import Profesor
from backend.models.rubrica import RubricaDocente, RubricaCreate, RubricaResponse
from backend.services.auth_service import get_current_profesor

router = APIRouter(prefix="/api/v1/rubricas", tags=["rubricas_docente"])


@router.post("", response_model=RubricaResponse, status_code=status.HTTP_201_CREATED)
def create_rubrica(
    rubrica_in: RubricaCreate,
    db: Session = Depends(get_db),
    current_profesor: Profesor = Depends(get_current_profesor)
):
    """
    Crea una nueva rúbrica personalizada para el docente autenticado.
    El campo 'criterios' se valida automáticamente contra el esquema Pydantic.
    """
    # Mapear los criterios a diccionarios JSON nativos para persistencia
    criterios_dict = [c.model_dump() for c in rubrica_in.criterios]
    
    new_rubrica = RubricaDocente(
        profesor_id=current_profesor.id,
        nombre=rubrica_in.nombre,
        criterios=criterios_dict
    )
    
    db.add(new_rubrica)
    db.commit()
    db.refresh(new_rubrica)
    return new_rubrica


@router.get("", response_model=List[RubricaResponse])
def get_rubricas(
    db: Session = Depends(get_db),
    current_profesor: Profesor = Depends(get_current_profesor)
):
    """
    Devuelve la lista completa de rúbricas personalizadas creadas por el docente autenticado.
    """
    rubricas = db.query(RubricaDocente).filter(
        RubricaDocente.profesor_id == current_profesor.id
    ).all()
    return rubricas


@router.get("/{rubrica_id}", response_model=RubricaResponse)
def get_rubrica_by_id(
    rubrica_id: int,
    db: Session = Depends(get_db),
    current_profesor: Profesor = Depends(get_current_profesor)
):
    """
    Recupera una rúbrica específica por su ID, validando la propiedad de la misma.
    """
    rubrica = db.query(RubricaDocente).filter(
        RubricaDocente.id == rubrica_id,
        RubricaDocente.profesor_id == current_profesor.id
    ).first()
    
    if not rubrica:
        # Intentar buscarla para discernir entre no encontrada y no autorizada
        exists = db.query(RubricaDocente).filter(RubricaDocente.id == rubrica_id).first()
        if exists:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para acceder a esta rúbrica."
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La rúbrica solicitada no existe."
        )
    return rubrica


@router.put("/{rubrica_id}", response_model=RubricaResponse)
def update_rubrica(
    rubrica_id: int,
    rubrica_in: RubricaCreate,
    db: Session = Depends(get_db),
    current_profesor: Profesor = Depends(get_current_profesor)
):
    """
    Modifica una rúbrica existente si pertenece al docente autenticado.
    Vuelve a validar que los criterios estructurados cumplan con los tipos requeridos.
    """
    rubrica = db.query(RubricaDocente).filter(
        RubricaDocente.id == rubrica_id,
        RubricaDocente.profesor_id == current_profesor.id
    ).first()
    
    if not rubrica:
        exists = db.query(RubricaDocente).filter(RubricaDocente.id == rubrica_id).first()
        if exists:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes autorización para editar esta rúbrica."
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La rúbrica que intentas modificar no existe."
        )
        
    criterios_dict = [c.model_dump() for c in rubrica_in.criterios]
    rubrica.nombre = rubrica_in.nombre
    rubrica.criterios = criterios_dict
    
    db.commit()
    db.refresh(rubrica)
    return rubrica


@router.delete("/{rubrica_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rubrica(
    rubrica_id: int,
    db: Session = Depends(get_db),
    current_profesor: Profesor = Depends(get_current_profesor)
):
    """
    Elimina permanentemente una rúbrica si pertenece al docente autenticado.
    """
    rubrica = db.query(RubricaDocente).filter(
        RubricaDocente.id == rubrica_id,
        RubricaDocente.profesor_id == current_profesor.id
    ).first()
    
    if not rubrica:
        exists = db.query(RubricaDocente).filter(RubricaDocente.id == rubrica_id).first()
        if exists:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes autorización para eliminar esta rúbrica."
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La rúbrica que intentas eliminar no existe."
        )
        
    db.delete(rubrica)
    db.commit()
    return None
