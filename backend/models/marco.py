"""
Módulo de modelos de datos y esquemas de validación para los Marcos de Evaluación Oficiales.
Implementa el modelo ORM de SQLAlchemy y los esquemas Pydantic v2 correspondientes.
Soporta metadatos de vigencia legislativa en cumplimiento con el ADR [D-033] y Hito [v0.2-003].
"""
import enum
from datetime import date
from typing import Any, Dict, List, Optional
from sqlalchemy import Column, Integer, String, Boolean, JSON, Date
from pydantic import BaseModel, Field, ConfigDict
from .database import Base

class Etapa(str, enum.Enum):
    """Etapa educativa: gobierna la escala de calificación y la oficialidad de la cualitativa (D-041, D-046)."""
    ESO = "ESO"
    BACH = "BACH"

# =====================================================================
# 1. MODELO ORM DE SQLALCHEMY (TABLA 'marcos_evaluacion')
# =====================================================================
class MarcoEvaluacion(Base):
    """
    Entidad de persistencia relacional para los marcos oficiales de evaluación.
    Almacena el currículum de la Xunta de Galicia en formato JSONB extensible.
    Contiene campos de vigencia legislativa en cumplimiento de la EU AI Act y el ADR [D-033].
    """
    __tablename__ = "marcos_evaluacion"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    asignatura = Column(String(100), nullable=False)
    curso = Column(String(100), nullable=False)
    etapa = Column(String(10), nullable=False)
    estado_activo = Column(Boolean, default=True, nullable=False)
    
    # Estructura JSONB que contiene competencias, saberes y criterios oficiales
    rubrica_completa = Column(JSON, nullable=False)
    
    # Metadatos de vigencia legislativa [D-033]
    ultima_verificacion_manual = Column(Date, nullable=True)
    normativa_fuentes = Column(JSON, nullable=True)


# =====================================================================
# 2. ESQUEMAS PYDANTIC V2 PARA LA API
# =====================================================================
class MarcoCreate(BaseModel):
    """Esquema de entrada para crear un nuevo marco de evaluación."""
    nombre: str = Field(..., min_length=3, max_length=255, description="Nombre del decreto o currículum oficial.")
    asignatura: str = Field(..., min_length=2, max_length=100, description="Asignatura o materia regulada.")
    curso: str = Field(..., min_length=2, max_length=100, description="Curso académico (ej. 1º Bacharelato).")
    etapa: Etapa = Field(..., description="Etapa educativa: 'ESO' (cualitativa oficial 1-10) o 'BACH' (numérica 0-10).")
    estado_activo: bool = Field(default=True, description="Estado operativo del marco.")
    rubrica_completa: Dict[str, Any] = Field(..., description="Estructura curricular completa en formato JSON.")
    ultima_verificacion_manual: Optional[date] = Field(None, description="Fecha de la última revisión de vigencia legal (meta-auditoría, no normativa en sí).")
    normativa_fuentes: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="Lista de fuentes legislativas. Cada objeto: {tipo, numero, fecha, url, vigente_desde, vigente_hasta}."
    )


class MarcoResponse(BaseModel):
    """Esquema de salida seguro para marcos de evaluación."""
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Identificador único del marco de evaluación.")
    nombre: str = Field(..., description="Nombre del decreto o currículum oficial.")
    asignatura: str = Field(..., description="Asignatura regulada.")
    curso: str = Field(..., description="Curso académico.")
    etapa: Etapa = Field(..., description="Etapa educativa (ESO/BACH).")
    estado_activo: bool = Field(..., description="Indica si el marco de evaluación está activo.")
    rubrica_completa: Dict[str, Any] = Field(..., description="Estructura curricular en JSON.")
    ultima_verificacion_manual: Optional[date] = Field(None, description="Última verificación manual de vigencia legal (meta-auditoría).")
    normativa_fuentes: Optional[List[Dict[str, Any]]] = Field(None, description="Lista estructurada de fuentes legislativas.")
