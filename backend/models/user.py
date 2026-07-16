"""
Módulo de modelos de datos y esquemas de validación para el Profesor y Autenticación.
Cumple con la Regla 2 de AGENTS.md (Modularidad Plana) aglutinando en un solo archivo
el modelo ORM de SQLAlchemy y los esquemas Pydantic v2 para registro, login y tokens.
Hito [v0.2-002] y ADR [D-031].

JUSTIFICACIÓN ARQUITECTÓNICA Y UMBRAL DE REFACTORIZACIÓN (Scaling Trigger):
- Se adopta deliberadamente la estructura plana (ORM + Pydantic v2 juntos) en cumplimiento
  estricto del principio YAGNI (Regla 2), al gestionar actualmente un número reducido de entidades.
- Umbral de Escalabilidad: Si en futuras fases el dominio supera las 8-10 tablas/entidades en BBDD,
  se procederá a desacoplar este módulo en `models/orm/` y `models/schemas/` para evitar acoplamientos.
"""
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from .database import Base


def utcnow():
    return datetime.now(timezone.utc)


# =====================================================================
# 1. MODELO ORM DE SQLALCHEMY (TABLA 'profesores')
# =====================================================================
class Profesor(Base):
    """
    Entidad de persistencia relacional para las profesoras del sistema.
    Almacena credenciales hacheadas por bcrypt según ADR [D-031].
    """
    __tablename__ = "profesores"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    nombre = Column(String(150), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=utcnow, nullable=False)


# =====================================================================
# 2. ESQUEMAS PYDANTIC V2 PARA ENTRADA Y SALIDA (API CONTRATOS)
# =====================================================================
class ProfesorCreate(BaseModel):
    """Esquema para la petición de registro de una nueva profesora."""
    email: EmailStr = Field(..., description="Correo electrónico único del docente.")
    nombre: str = Field(..., min_length=2, max_length=150, description="Nombre y apellidos del docente.")
    password: str = Field(..., min_length=6, description="Contraseña en texto plano (será hacheada en el servicio).")


class ProfesorLogin(BaseModel):
    """Esquema para la petición de inicio de sesión."""
    email: EmailStr = Field(..., description="Correo electrónico registrado.")
    password: str = Field(..., description="Contraseña de acceso.")


class ProfesorResponse(BaseModel):
    """
    Esquema de salida segura para datos del profesor.
    INVARIANTE DE SEGURIDAD (HTTP Contract Invariant):
    Este modelo Pydantic prohíbe terminantemente incluir campos sensibles como 'hashed_password'
    o tokens internos. Evita por diseño cualquier fuga de credenciales en las respuestas de la API.
    """
    model_config = ConfigDict(from_attributes=True)


    id: int = Field(..., description="Identificador único del profesor en base de datos.")
    email: str = Field(..., description="Correo electrónico del docente.")
    nombre: str = Field(..., description="Nombre y apellidos.")
    created_at: datetime = Field(..., description="Fecha de registro del usuario en el sistema.")


class TokenResponse(BaseModel):
    """Esquema de respuesta al iniciar sesión exitosamente con JWT."""
    access_token: str = Field(..., description="Token JWT firmado en formato Bearer.")
    token_type: str = Field(default="bearer", description="Tipo de token estándar (bearer).")
