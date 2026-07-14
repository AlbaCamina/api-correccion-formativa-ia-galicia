"""
Módulo de modelos de datos y esquemas de validación para los Marcos de Evaluación Oficiales.
Implementa el modelo ORM de SQLAlchemy y los esquemas Pydantic v2 correspondientes.
Soporta metadatos de vigencia legislativa en cumplimiento con el ADR [D-033] y Hito [v0.2-003].
"""
from datetime import date
from typing import Any, Dict, Optional
from sqlalchemy import Column, Integer, String, Boolean, JSON, Date
from pydantic import BaseModel, Field, ConfigDict
from .database import Base


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
    estado_activo = Column(Boolean, default=True, nullable=False)
    
    # Estructura JSONB que contiene competencias, saberes y criterios oficiales
    rubrica_completa = Column(JSON, nullable=False)
    
    # Metadatos de vigencia legislativa [D-033]
    ultima_verificacion_manual = Column(Date, nullable=True)
    fuente_legislativa_url = Column(String(500), nullable=True)


# =====================================================================
# 2. ESQUEMAS PYDANTIC V2 PARA LA API
# =====================================================================
class MarcoCreate(BaseModel):
    """Esquema de entrada para crear un nuevo marco de evaluación."""
    nombre: str = Field(..., min_length=3, max_length=255, description="Nombre del decreto o currículum oficial.")
    asignatura: str = Field(..., min_length=2, max_length=100, description="Asignatura o materia regulada.")
    curso: str = Field(..., min_length=2, max_length=100, description="Curso académico (ej. 1º Bacharelato).")
    estado_activo: bool = Field(default=True, description="Estado operativo del marco.")
    rubrica_completa: Dict[str, Any] = Field(..., description="Estructura curricular completa en formato JSON.")
    ultima_verificacion_manual: Optional[date] = Field(None, description="Fecha de la última revisión de vigencia legal.")
    fuente_legislativa_url: Optional[str] = Field(None, max_length=500, description="Enlace al BOE/DOG oficial.")


class MarcoResponse(BaseModel):
    """Esquema de salida seguro para marcos de evaluación."""
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Identificador único del marco de evaluación.")
    nombre: str = Field(..., description="Nombre del decreto o currículum oficial.")
    asignatura: str = Field(..., description="Asignatura regulada.")
    curso: str = Field(..., description="Curso académico.")
    estado_activo: bool = Field(..., description="Indica si el marco de evaluación está activo.")
    rubrica_completa: Dict[str, Any] = Field(..., description="Estructura curricular en JSON.")
    ultima_verificacion_manual: Optional[date] = Field(None, description="Última verificación manual de vigencia legal.")
    fuente_legislativa_url: Optional[str] = Field(None, description="URL del BOE/DOG de la normativa.")
