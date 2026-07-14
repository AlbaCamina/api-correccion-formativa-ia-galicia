"""
Módulo de modelos de datos y esquemas de validación para las Entregas (Submissions),
Evaluaciones y el Registro de Auditoría (ChangeLog).
Cumple con la Regla 2 (Modularidad Plana) aglutinando en un solo archivo
los modelos ORM de SQLAlchemy y los esquemas Pydantic v2 correspondientes.
Hito [v0.2-005] y ADR [D-002], [D-023], [D-024], [D-026].
"""
import uuid
from datetime import datetime
from typing import Any, Dict, Optional
from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, ConfigDict
from .database import Base
from .evaluation import EvaluacionIA


# =====================================================================
# 1. MODELOS ORM DE SQLALCHEMY
# =====================================================================

class Submission(Base):
    """
    Entidad de persistencia relacional para las entregas de los alumnos.
    Utiliza un identificador UUID para prevenir la predictibilidad de IDs en la nube.
    Soporta la anonimización mediante 'alumno_id' y el almacenamiento de adaptaciones NEAE.
    """
    __tablename__ = "submissions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    profesor_id = Column(Integer, ForeignKey("profesores.id", ondelete="CASCADE"), nullable=False)
    marco_id = Column(Integer, ForeignKey("marcos_evaluacion.id", ondelete="SET NULL"), nullable=True)
    rubrica_id = Column(Integer, ForeignKey("rubricas_docente.id", ondelete="CASCADE"), nullable=False)
    
    # Anonimización/Seudonimización bajo RGPD y LOPDGDD
    alumno_id = Column(String(100), nullable=True)
    
    # Campo flexible JSONB para guardar adaptaciones del alumno (DEA/ACNS/ACS) según Decreto 229/2011
    adaptaciones_alumno = Column(JSON, nullable=True)
    
    # Estados del ciclo de vida de la corrección
    estado = Column(String(50), default="PENDING", nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relaciones
    profesor = relationship("Profesor")
    marco = relationship("MarcoEvaluacion")
    rubrica = relationship("RubricaDocente")
    evaluaciones = relationship("Evaluacion", back_populates="submission", cascade="all, delete-orphan")
    changelog = relationship("ChangeLog", back_populates="submission", cascade="all, delete-orphan")


class Evaluacion(Base):
    """
    Entidad de persistencia para el resultado final de la corrección de una entrega.
    El resultado estructurado de la IA se guarda en formato JSONB para conservar toda la metadata.
    """
    __tablename__ = "evaluaciones"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    submission_id = Column(String(36), ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False)
    
    # JSON estructurado con la corrección detallada (EvaluacionIA)
    resultado_ia = Column(JSON, nullable=False)
    
    # Calificación final decidida/validada por el docente (Human-in-the-Loop)
    nota_final = Column(Float, nullable=True)
    
    # Firma oficial del docente (HitL) que valida el resultado
    aprobado_por_profesor = Column(Boolean, default=False, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    submission = relationship("Submission", back_populates="evaluaciones")


class ChangeLog(Base):
    """
    Tabla append-only para auditoría e inmutabilidad probatoria requerida por el AI Act.
    Registra todas las acciones importantes (creación, edición, aprobación) sobre una entrega.
    """
    __tablename__ = "changelog"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    submission_id = Column(String(36), ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False)
    
    accion = Column(String(255), nullable=False)  # Ej. "SUBMIT", "IA_EVALUATION", "TEACHER_UPDATE", "GRADED"
    actor = Column(String(100), nullable=False)   # Ej. "IA", "PROFESOR_ID_1"
    
    # Capturas de estado para trazabilidad e inmutabilidad
    datos_anteriores = Column(JSON, nullable=True)
    datos_nuevos = Column(JSON, nullable=True)
    
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    submission = relationship("Submission", back_populates="changelog")


# =====================================================================
# 2. ESQUEMAS PYDANTIC V2 PARA LA API (CONTRATOS)
# =====================================================================

class SubmissionCreate(BaseModel):
    """Esquema de entrada para registrar una nueva entrega a corregir."""
    marco_id: Optional[int] = Field(None, description="ID del marco normativo oficial (dejar null para Rúbrica Pura).")
    rubrica_id: int = Field(..., description="ID de la rúbrica del docente requerida para evaluar.")
    alumno_id: Optional[str] = Field(None, max_length=100, description="Identificador seudonimizado del alumno (RGPD).")
    adaptaciones_alumno: Optional[Dict[str, Any]] = Field(None, description="Adaptaciones NEAE configuradas.")


class SubmissionResponse(BaseModel):
    """Esquema de salida seguro para información general de entregas."""
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(..., description="ID único de la entrega (UUID).")
    profesor_id: int = Field(..., description="ID del profesor asignado.")
    marco_id: Optional[int] = Field(..., description="ID del marco normativo si aplica.")
    rubrica_id: int = Field(..., description="ID de la rúbrica utilizada.")
    alumno_id: Optional[str] = Field(..., description="Identificador anónimo del alumno.")
    adaptaciones_alumno: Optional[Dict[str, Any]] = Field(..., description="Adaptaciones asociadas.")
    estado: str = Field(..., description="Estado del ciclo de vida (PENDING/ANALYZING/REVIEW/GRADED).")
    created_at: datetime = Field(..., description="Fecha de recepción.")
    updated_at: datetime = Field(..., description="Fecha de última actualización.")


class EvaluacionResponse(BaseModel):
    """Esquema de salida seguro para el detalle de la evaluación."""
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID de la evaluación.")
    submission_id: str = Field(..., description="ID de la entrega asociada.")
    resultado_ia: EvaluacionIA = Field(..., description="Contrato estructurado detallado de la IA.")
    nota_final: Optional[float] = Field(..., description="Nota final del examen asignada o firmada.")
    aprobado_por_profesor: bool = Field(..., description="Indica si el profesor ha validado la corrección.")
    created_at: datetime = Field(..., description="Fecha de generación.")


class ChangeLogResponse(BaseModel):
    """Esquema de salida para las entradas de auditoría y trazabilidad."""
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID de la entrada del log.")
    submission_id: str = Field(..., description="ID de la entrega asociada.")
    accion: str = Field(..., description="Acción realizada.")
    actor: str = Field(..., description="Usuario o sistema que la realizó.")
    datos_anteriores: Optional[Dict[str, Any]] = Field(..., description="Estado anterior.")
    datos_nuevos: Optional[Dict[str, Any]] = Field(..., description="Estado nuevo.")
    timestamp: datetime = Field(..., description="Marca de tiempo del log.")
