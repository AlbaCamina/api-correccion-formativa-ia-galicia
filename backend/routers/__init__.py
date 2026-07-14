from .evaluation import router as evaluation_router
from .auth import router as auth_router
from .marco import router as marco_router
from .rubrica import router as rubrica_router

__all__ = [
    "evaluation_router",
    "auth_router",
    "marco_router",
    "rubrica_router",
]

