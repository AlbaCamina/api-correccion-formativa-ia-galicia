"""
Módulo de servicio de autenticación y seguridad para el profesorado (JWT + bcrypt).
Implementa hacheo unidireccional (ADR [D-031]) e inyección de dependencia para rutas protegidas.
Cumple con el principio YAGNI y Modularidad Plana.
"""
import os
from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
import bcrypt as _bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend.models.database import get_db
from backend.models.user import Profesor

# Configuración del algoritmo bcrypt (nativo, sin passlib)

# Configuración de JWT
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-galicia-2026-hitl-ninja")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440")) # 24 horas

# Esquema de autenticación Bearer Token de FastAPI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def hash_password(password: str) -> str:
    """
    Convierte una contraseña en texto claro en un hash unidireccional irreversible con bcrypt.
    """
    return _bcrypt.hashpw(password.encode("utf-8"), _bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto claro coincide con el hash almacenado.
    """
    return _bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Genera un token JWT firmado digitalmente conteniendo el email del docente en el claim 'sub'.
    Se utiliza estrictamente para autenticación básica transaccional (login de profesorado),
    prescindiendo deliberadamente de scopes complejos o control RBAC según el principio YAGNI.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_profesor(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Profesor:
    """
    Dependencia de FastAPI para proteger endpoints requeridos por autenticación [v0.2-002].
    Extrae y decodifica el Bearer JWT, busca al docente por ID/email y devuelve la entidad ORM.
    Si el token ha expirado, es inválido o la profesora ya no existe, lanza HTTPException 401.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación inválidas o expiradas.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    profesor = db.query(Profesor).filter(Profesor.email == user_email).first()
    if profesor is None:
        raise credentials_exception
    return profesor
