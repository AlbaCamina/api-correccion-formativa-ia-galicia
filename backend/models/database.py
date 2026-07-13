"""
Módulo de base de datos relacional para la API de Corrección Formativa con IA.
Implementa conexión y pool transaccional con SQLAlchemy sobre PostgreSQL (v0.2).
Cumple con la Regla 2 (Modularidad Plana): todo el acceso a datos reside en backend/models/.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Obtener URL de conexión desde variables de entorno
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgrespassword@localhost:5433/api_correccion_galicia"

)

# Crear motor de SQLAlchemy con pool de conexiones configurado
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)

# Fábrica de sesiones transaccionales
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base declarativa para los modelos ORM de SQLAlchemy
Base = declarative_base()


def get_db():
    """
    Dependencia de FastAPI para inyectar la sesión de base de datos en las peticiones.
    Garantiza el cierre limpio de la transacción al finalizar el endpoint.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
