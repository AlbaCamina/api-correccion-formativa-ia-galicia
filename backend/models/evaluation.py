from typing import List, Literal, Optional
from pydantic import BaseModel, Field

class RubricItem(BaseModel):
    category: str = Field(..., description="Categoría o criterio evaluado (ej. Comprensión conceptual, Argumentación).")
    score: float = Field(..., description="Puntuación obtenida en esta categoría.")
    maxScore: float = Field(..., description="Puntuación máxima posible para esta categoría.")
    reasoning: str = Field(..., description="Breve justificación pedagógica de la puntuación otorgada.")

class VisualMarker(BaseModel):
    x: float = Field(..., description="Coordenada X sobre el documento/imagen (0 en v0.1 de texto plano).")
    y: float = Field(..., description="Coordenada Y sobre el documento/imagen (0 en v0.1 de texto plano).")
    type: Literal["ERROR", "MEJORA", "CORRECTO", "error_excluido"] = Field(
        ..., 
        description="Tipo de marcador: ERROR (rojo), MEJORA (amarillo), CORRECTO (verde) u error_excluido (gris/neutro para NEAE)."
    )
    comment: str = Field(..., description="Comentario o explicación del marcador visual.")

class ImprovementNeeds(BaseModel):
    immediate: List[str] = Field(..., description="Lista de acciones de mejora urgentes o inmediatas (alta prioridad).")
    mediumLongTerm: List[str] = Field(..., description="Lista de acciones de mejora de consolidación a medio o largo plazo.")

class QualitativeAnalysis(BaseModel):
    strengths: List[str] = Field(..., description="Puntos fuertes detectados en la respuesta del estudiante.")
    improvementNeeds: ImprovementNeeds = Field(..., description="Necesidades de mejora clasificadas por urgencia formativa.")
    teacherSummary: str = Field(..., description="Resumen cualitativo condensado para el cuaderno del profesor.")

class EvaluacionIA(BaseModel):
    transcription: str = Field(..., description="Transcripción del texto evaluado (en v0.1 texto plano, coincide con la respuesta).")
    rubricBreakdown: List[RubricItem] = Field(..., description="Desglose por criterios y rúbrica del profesor/normativa.")
    visualMarkers: Optional[List[VisualMarker]] = Field(default_factory=list, description="Marcadores visuales sobre la imagen. [] válido en v0.1.")
    qualitativeAnalysis: QualitativeAnalysis = Field(..., description="Análisis pedagógico cualitativo con fortalezas y mejoras.")
    
    # Campos exigidos por la Decisión de Arquitectura [D-024] y Decretos gallegos 156/157/2022
    calificacion_cualitativa: Literal["IN", "SU", "BI", "NT", "SB"] = Field(
        ..., 
        description="Calificación oficial cualitativa según Decretos gallegos: Insuficiente (IN), Suficiente (SU), Bien (BI), Notable (NT), Sobresaliente (SB)."
    )
    siguiente_paso_accionable: str = Field(
        ..., 
        description="Siguiente Paso Accionable (Feed Forward): Directriz clara, concreta y realizable hoy por el alumno."
    )
    confidence_score: float = Field(
        ..., 
        description="Índice de Confianza IA (0.0 a 1.0) en la claridad de lectura/interpretación de la respuesta."
    )

    # Campos de Adaptaciones Curriculares NEAE/NEE (Hito v0.2-007 y ADR D-023)
    ortografia_detectada: Optional[List[str]] = Field(
        default_factory=list,
        description="Lista de faltas de ortografía o errores gramaticales detectados en la respuesta."
    )
    errores_excluidos_por_adaptacion: Optional[List[str]] = Field(
        default_factory=list,
        description="Subconjunto de errores ortográficos que han sido detectados pero excluidos de la penalización de nota final por adaptaciones del alumno."
    )

