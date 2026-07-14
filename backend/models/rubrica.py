"""
Módulo de modelos de datos y esquemas de validación para las Rúbricas del Docente.
Cumple con la Regla 2 (Modularidad Plana) aglutinando en un solo archivo
el modelo ORM de SQLAlchemy y los esquemas Pydantic v2.
Hito [v0.2-004] y ADR [D-027] / [D-030].
"""
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, ConfigDict
from .database import Base


# =====================================================================
# 1. SUB-ESQUEMAS PYDANTIC V2 PARA LA ESTRUCTURA INTERNA DE CRITERIOS
# =====================================================================
class NivelCriterio(BaseModel):
    """Esquema para modelar un nivel de logro específico dentro de un criterio."""
    puntos: float = Field(..., description="Puntuación o peso asignado a este nivel.")
    descripcion: str = Field(..., description="Descripción detallada de la expectativa de logro.")


class CriterioRubrica(BaseModel):
    """Esquema que define un criterio individual de evaluación con sus niveles de logro."""
    id: str = Field(..., min_length=1, max_length=15, description="Identificador único corto (ej: C1, ORT).")
    nombre: str = Field(..., min_length=2, max_length=100, description="Título del criterio (ej: Ortografía).")
    descripcion: str = Field(..., min_length=5, max_length=500, description="Explicación detallada de qué evalúa.")
    peso: float = Field(..., ge=0.0, le=100.0, description="Peso porcentual relativo sobre el total (ej: 25.0).")
    niveles: Optional[List[NivelCriterio]] = Field(None, description="Niveles opcionales de rúbrica analítica.")


# =====================================================================
# 2. MODELO ORM DE SQLALCHEMY (TABLA 'rubricas_docente')
# =====================================================================
class RubricaDocente(Base):
    """
    Entidad de persistencia relacional para las rúbricas personalizadas de las docentes.
    Almacena los criterios analíticos en un campo JSONB de base de datos.
    """
    __tablename__ = "rubricas_docente"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    profesor_id = Column(Integer, ForeignKey("profesores.id", ondelete="CASCADE"), nullable=False)
    nombre = Column(String(255), nullable=False)
    
    # Campo JSON que contendrá la lista validada de CriterioRubrica
    criterios = Column(JSON, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relación de conveniencia
    profesor = relationship("Profesor")


# =====================================================================
# 3. ESQUEMAS PYDANTIC V2 PARA LA API (CONTRATOS)
# =====================================================================
class RubricaCreate(BaseModel):
    """Esquema de entrada para crear o actualizar una rúbrica de evaluación."""
    nombre: str = Field(..., min_length=3, max_length=255, description="Nombre de la rúbrica (ej: Rúbrica de Comentario de Texto).")
    criterios: List[CriterioRubrica] = Field(..., min_length=1, description="Lista estructurada de criterios de evaluación.")


class RubricaResponse(BaseModel):
    """Esquema de salida segura para retornar información de rúbricas."""
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Identificador único de la rúbrica.")
    profesor_id: int = Field(..., description="ID del docente propietario.")
    nombre: str = Field(..., description="Nombre de la rúbrica.")
    criterios: List[CriterioRubrica] = Field(..., description="Lista de criterios validados.")
    created_at: datetime = Field(..., description="Fecha de creación del recurso.")
