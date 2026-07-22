"""
Esquema estructurado de salida del agente de IA (contrato EvaluacionIA).
Corregido para: abreviatura legal 'BE' (no 'BI'), soporte multi-etapa ESO/BACH,
trazabilidad criterio->competencia clave, y semántica de nota orientativa (HitL).
Base normativa: Decreto 156/2022 (ESO) y Decreto 157/2022 (Bachillerato) - Xunta de Galicia.
"""
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, model_validator
from backend.models.marco import Etapa

# Escala cualitativa OFICIAL (Art. 27.1, Decreto 156/2022 - ESO).
# CORRECCIÓN CRÍTICA: "Bien" se abrevia "BE", NUNCA "BI".
# Se añade "NA" porque en Bachillerato la cualitativa NO es oficial (solo la numérica 0-10).
CalificacionCualitativa = Literal["IN", "SU", "BE", "NT", "SB", "NA"]

# Competencias clave LOMLOE (comunes a todas las CCAA).
CompetenciaClave = Literal["CCL", "CP", "STEM", "CD", "CPSAA", "CC", "CE", "CCEC"]

class RubricItem(BaseModel):
    # --- Trazabilidad normativa (criterio -> competencia clave) ---
    criterio_codigo: Optional[str] = Field(
        None,
        description="Código oficial del criterio de evaluación del anexo del decreto (ej. 'FILO-B2.3'). None si es criterio libre de la rúbrica docente sin código oficial."
    )
    competencias_clave: List[CompetenciaClave] = Field(
        default_factory=list,
        description="Competencias clave asociadas a este criterio vía descriptores operativos del perfil de salida. Permite al backend agregar el grado de competencias del trimestre."
    )
    # --- Valoración ---
    category: str = Field(..., description="Nombre del criterio evaluado (ej. Comprensión conceptual, Argumentación).")
    score: float = Field(..., description="Puntuación obtenida en este criterio (admite decimales; orientativa).")
    maxScore: float = Field(..., description="Puntuación máxima posible de este criterio.")
    peso: Optional[float] = Field(
        None, ge=0.0, le=100.0,
        description="Peso (%) del criterio, según rúbrica del departamento. Usado para la media ponderada de la nota de prueba."
    )
    nivel_logro: Optional[Literal[1, 2, 3, 4]] = Field(
        None,
        description="Nivel de logro si el departamento usa rúbrica 1-4 (1=No conseguido, 2=En proceso, 3=Adquirido, 4=Avanzado). Configuración de centro, no obligatorio por ley."
    )
    reasoning: str = Field(..., description="Justificación pedagógica de la puntuación, referida a la evidencia del alumno.")

class VisualMarker(BaseModel):
    x: float = Field(..., description="Coordenada X sobre el documento/imagen (0 en v0.1 de texto plano).")
    y: float = Field(..., description="Coordenada Y sobre el documento/imagen (0 en v0.1 de texto plano).")
    type: Literal["ERROR", "MEJORA", "CORRECTO", "error_excluido"] = Field(
        ...,
        description="Tipo de marcador: ERROR (rojo), MEJORA (amarillo), CORRECTO (verde) u error_excluido (gris/neutro para NEAE)."
    )
    comment: str = Field(..., description="Comentario o explicación del marcador visual.")

class ImprovementNeeds(BaseModel):
    immediate: List[str] = Field(..., description="Acciones de mejora urgentes (errores conceptuales graves o lo necesario para aprobar).")
    mediumLongTerm: List[str] = Field(..., description="Acciones de consolidación a medio/largo plazo (hacia sobresaliente o madurez competencial).")

class QualitativeAnalysis(BaseModel):
    strengths: List[str] = Field(..., description="Puntos fuertes detectados en la respuesta del estudiante.")
    improvementNeeds: ImprovementNeeds = Field(..., description="Necesidades de mejora clasificadas por urgencia formativa.")
    teacherSummary: str = Field(
        ...,
        description="Resumen cualitativo para el cuaderno del profesor. Incluye aquí avisos de configuración: pesos que no suman 100 %, criterios sin evaluar, o brechas curriculares detectadas en modo AUDITORIA_CURRICULAR."
    )

class EvaluacionIA(BaseModel):
    transcription: str = Field(..., description="Transcripción del texto evaluado (en v0.1 texto plano, coincide con la respuesta).")
    rubricBreakdown: List[RubricItem] = Field(
        ...,
        description="Desglose POR CRITERIO. Cada ítem traza criterio -> competencias clave. Es el referente legal de calificación (Art. 24.3 Decreto 157/2022)."
    )
    visualMarkers: Optional[List[VisualMarker]] = Field(default_factory=list, description="Marcadores visuales sobre la imagen. [] válido en v0.1.")
    qualitativeAnalysis: QualitativeAnalysis = Field(..., description="Análisis pedagógico cualitativo con fortalezas y mejoras.")

    # --- Etapa: determina si la cualitativa es oficial ---
    etapa: Etapa = Field(
        ...,
        description="Etapa educativa. En ESO la calificación oficial fuerte es la cualitativa; en BACH es la numérica y la cualitativa es solo orientativa (usar 'NA')."
    )

    # --- Calificación ORIENTATIVA (HitL: el docente decide y redondea al aprobar) ---
    calificacion_cualitativa: CalificacionCualitativa = Field(
        ...,
        description="Cualitativa Decreto 156/2022 (SOLO oficial en ESO): IN=1-4, SU=5, BE=6, NT=7-8, SB=9-10. En BACH usar 'NA'."
    )
    calificacion_numerica: float = Field(
        ..., ge=0.0, le=10.0,
        description="Nota ORIENTATIVA sobre 10 (admite decimales, NO redondear). MEDIA PONDERADA por peso de los criterios (normalizados score/maxScore*10), NO suma simple. El redondeo a entero de boletín lo hace el docente (HitL)."
    )
    siguiente_paso_accionable: str = Field(
        ...,
        description="Feed Forward (Hattie): directriz concreta y realizable hoy por el alumno. Prohibido lo genérico. Debe decir QUÉ y CÓMO."
    )
    confidence_score: float = Field(
        ..., ge=0.0, le=1.0,
        description="Índice de confianza IA (0.0-1.0) en la claridad de lectura/interpretación de la respuesta."
    )

    # --- Adaptaciones NEAE/NEE (ADR D-023) ---
    ortografia_detectada: Optional[List[str]] = Field(
        default_factory=list,
        description="Faltas de ortografía o errores gramaticales detectados en la respuesta."
    )
    errores_excluidos_por_adaptacion: Optional[List[str]] = Field(
        default_factory=list,
        description="Subconjunto de errores ortográficos detectados pero EXCLUIDOS de penalización por adaptaciones del alumno."
    )

    @model_validator(mode="after")
    def recalcular_media_ponderada(self) -> "EvaluacionIA":
        """
        Mutador (D-043): La IA no suma. El backend recalcula la nota de prueba
        de forma determinista como media ponderada sobre 10. Nunca lanza 422.
        """
        try:
            pesos_validos = [item for item in self.rubricBreakdown if item.peso is not None and item.maxScore > 0]
            
            if pesos_validos:
                total_peso = sum(item.peso for item in pesos_validos)
                if total_peso > 0:
                    nota_calculada = sum(
                        ((item.score / item.maxScore) * 10.0) * (item.peso / total_peso)
                        for item in pesos_validos
                    )
                    self.calificacion_numerica = round(nota_calculada, 2)
        except Exception:
            # Silencioso en Pydantic para no romper la respuesta del LLM (fallback a lo devuelto por la IA)
            # Logueable externamente si fuera necesario
            pass
            
        return self
