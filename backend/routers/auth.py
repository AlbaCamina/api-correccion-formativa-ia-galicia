"""
Módulo de enrutamiento (FastAPI) para autenticación y registro de profesores.
Cumple con la Regla 2 (Modularidad Plana) ubicando en routers/ los endpoints de auth.
Hito [v0.2-002].
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.models.database import get_db
from backend.models.user import Profesor, ProfesorCreate, ProfesorLogin, ProfesorResponse, TokenResponse
from backend.services.auth_service import hash_password, verify_password, create_access_token, get_current_profesor

router = APIRouter(prefix="/api/v1/auth", tags=["autenticacion"])


@router.post("/register", response_model=ProfesorResponse, status_code=status.HTTP_201_CREATED)
def register_profesor(profesor_in: ProfesorCreate, db: Session = Depends(get_db)):
    """
    Registra una nueva cuenta de profesora en el sistema.
    Hachea la contraseña con bcrypt antes de guardarla en PostgreSQL.
    """
    # Verificar si el email ya existe en la base de datos
    existing_profesor = db.query(Profesor).filter(Profesor.email == profesor_in.email).first()
    if existing_profesor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ingresado ya se encuentra registrado en el sistema."
        )

    # Crear entidad ORM con contraseña hacheada
    new_profesor = Profesor(
        email=profesor_in.email,
        nombre=profesor_in.nombre,
        hashed_password=hash_password(profesor_in.password)
    )
    db.add(new_profesor)
    db.commit()
    db.refresh(new_profesor)
    return new_profesor


@router.post("/login", response_model=TokenResponse)
def login_profesor(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Inicia sesión en el sistema usando Form Data estándar de OAuth2 (compatibilidad nativa con Swagger UI /docs).
    El campo 'username' corresponde al correo electrónico ('email') del profesor.
    Devuelve el token Bearer JWT transaccional.
    """
    profesor = db.query(Profesor).filter(Profesor.email == form_data.username).first()
    if not profesor or not verify_password(form_data.password, profesor.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo electrónico o contraseña incorrectos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generar Bearer JWT
    access_token = create_access_token(data={"sub": profesor.email})
    return TokenResponse(access_token=access_token, token_type="bearer")


@router.post("/login-json", response_model=TokenResponse)
def login_profesor_json(login_in: ProfesorLogin, db: Session = Depends(get_db)):
    """
    Endpoint alternativo de inicio de sesión recibiendo payload JSON (compatible con SPAs/PWAs que no usan Form Data).
    Devuelve el token Bearer JWT.
    """
    profesor = db.query(Profesor).filter(Profesor.email == login_in.email).first()
    if not profesor or not verify_password(login_in.password, profesor.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo electrónico o contraseña incorrectos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": profesor.email})
    return TokenResponse(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=ProfesorResponse)
def get_me(current_profesor: Profesor = Depends(get_current_profesor)):
    """
    Endpoint protegido para validar que la cabecera 'Authorization: Bearer <jwt>'
    funciona correctamente y devuelve el perfil del docente autenticado.
    """
    return current_profesor
