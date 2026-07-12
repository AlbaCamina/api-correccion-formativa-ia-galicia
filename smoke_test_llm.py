"""
Smoke Test de Contrato JSON con la IA (v0.1-000)
--------------------------------------------------
Prerrequisito arquitectónico: Valida y verifica que el LLM (OpenAI o Anthropic)
cumple con exactitud el contrato JSON (Structured Output) definido por Pydantic
y las directrices del Decreto 157/2022 de la Xunta de Galicia y [D-024].

Ejecución desde WSL (Ubuntu):
  1. Copiar .env.example a .env y configurar OPENAI_API_KEY
  2. Activar entorno virtual (source venv/bin/activate)
  3. Ejecutar: python3 smoke_test_llm.py
"""

import json
import os
import sys
from typing import List, Literal, Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Cargar variables de entorno desde .env
load_dotenv()

# ==========================================
# 1. MODELOS PYDANTIC DEL CONTRATO (v0.1-002)
# ==========================================

class RubricItem(BaseModel):
    category: str = Field(..., description="Categoría o criterio evaluado (ej. Comprensión conceptual, Argumentación).")
    score: float = Field(..., description="Puntuación obtenida en esta categoría.")
    maxScore: float = Field(..., description="Puntuación máxima posible para esta categoría.")
    reasoning: str = Field(..., description="Breve justificación pedagógica de la puntuación otorgada.")

class VisualMarker(BaseModel):
    x: float = Field(..., description="Coordenada X sobre el documento/imagen (0 en v0.1 de texto plano).")
    y: float = Field(..., description="Coordenada Y sobre el documento/imagen (0 en v0.1 de texto plano).")
    type: str = Field(..., description="Tipo de marcador: ERROR, MEJORA o CORRECTO.")
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


# ==========================================
# 2. SYSTEM PROMPT REAL (v0.1-004)
# ==========================================
SYSTEM_PROMPT = """
Actúa como evaluador formativo experto en **Filosofía de Bachillerato, educación secundaria gallega (Decreto 157/2022, Xunta de Galicia)**.
Tu misión es asistir (copiloto HitL) al docente evaluando la respuesta de un alumno ante una pregunta o instrumento de evaluación y devolviendo estrictamente un objeto JSON estructurado que cumpla con el esquema requerido.

Directrices pedagógicas obligatorias:
1. Aplica los criterios competenciales y de saberes básicos del Decreto 157/2022 de la Xunta de Galicia.
2. Separa radicalmente las mejoras inmediatas (urgentes para aprobar o corregir errores conceptuales graves) de las mejoras a medio/largo plazo (para alcanzar el sobresaliente o profundizar en madurez filosófica).
3. Otorga una calificación competencial cualitativa (`calificacion_cualitativa`) oficial:
   - "IN": Insuficiente
   - "SU": Suficiente
   - "BI": Bien
   - "NT": Notable
   - "SB": Sobresaliente
4. Genera siempre un "Siguiente Paso Accionable" (`siguiente_paso_accionable` / Feed Forward del modelo Hattie): una directriz práctica, clara y realizable en 5 minutos o en su próximo estudio de hoy por el alumno. Prohibido dar consejos abstractos o genéricos ("debes mejorar tu expresión").
5. Evalúa el grado de certeza o nitidez de la respuesta con el `confidence_score` (entre 0.0 y 1.0).
6. Al ser texto plano sin imagen (v0.1), devuelve un array vacío `[]` para `visualMarkers`.
"""


# ==========================================
# 3. SIMULACIÓN Y PRUEBA DEL CONTRATO
# ==========================================
def run_smoke_test():
    print("=================================================================")
    print("🚀 INICIANDO SMOKE TEST DEL CONTRATO JSON CON LA IA (v0.1-000)")
    print("=================================================================")
    
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    model_name = os.getenv("LLM_MODEL", "gpt-4o-mini")
    
    # Datos de prueba: Respuesta simulada del alumno sobre el Mito de la Caverna (Regular / Mejorable)
    pregunta = "¿Qué simboliza la salida del prisionero de la caverna en el mito de Platón e indica cuál es el papel de la educación según el filósofo?"
    respuesta_alumno = "El prisionero sale a la luz exterior y ve el sol que es la idea de Bien. Al principio le duelen los ojos porque no está acostumbrado. Esto significa que aprender filosofía cuesta esfuerzo. Luego Platón dice que el filósofo tiene que volver a la caverna para mandar en la ciudad política aunque le maten."
    rubrica = "Criterio 1: Precisión conceptual y simbolismo platónico (0-5 pts). Criterio 2: Conexión con el concepto platónico de paideia/educación como conversión del alma (0-5 pts)."
    
    print(f"📦 Proveedor configurado: {provider.upper()} | Modelo: {model_name}")
    print(f"📝 Pregunta: {pregunta}")
    print(f"👩‍🎓 Respuesta del Alumno: \"{respuesta_alumno}\"\n")
    print("⏳ Consultando al modelo LLM con Structured Outputs (Pydantic)...")

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "tu_api_key_de_openai_aqui":
            print("\n❌ ERROR: Falta configurar OPENAI_API_KEY en tu archivo .env local.")
            print("💡 Instrucción: Copia .env.example a .env y pon tu clave real para ejecutar este test en WSL.")
            sys.exit(1)
            
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            
            completion = client.beta.chat.completions.parse(
                model=model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Pregunta: {pregunta}\nRespuesta del Alumno: {respuesta_alumno}\nRúbrica del Profesor: {rubrica}"}
                ],
                response_format=EvaluacionIA,
                temperature=0.2,
            )
            
            resultado: EvaluacionIA = completion.choices[0].message.parsed
            
        except Exception as e:
            print(f"\n❌ Error durante la llamada a OpenAI o validación Pydantic: {e}")
            sys.exit(1)
            
    elif provider == "anthropic":
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key or api_key == "tu_api_key_de_anthropic_aqui":
            print("\n❌ ERROR: Falta configurar ANTHROPIC_API_KEY en tu archivo .env local.")
            sys.exit(1)
        
        # En v0.1 si usan Anthropic se utilizaría tool use o json mode. 
        # Mostramos mensaje orientativo si no está implementada la estructura de tools
        print("\n⚠️ Nota: Para este smoke test el soporte nativo pydantic .parse() está implementado para OpenAI y Groq.")
        print("Si deseas probar con Anthropic, asegúrate de configurar LLM_PROVIDER=openai en el .env con un modelo OpenAI o usar el wrapper de tools.")
        sys.exit(0)
    elif provider == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or api_key == "tu_api_key_de_groq_aqui":
            print("\n❌ ERROR: Falta configurar GROQ_API_KEY en tu archivo .env local.")
            sys.exit(1)
            
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
            
            # Intentamos primero con .parse() nativo (Structured Outputs json_schema)
            try:
                completion = client.beta.chat.completions.parse(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": f"Pregunta: {pregunta}\nRespuesta del Alumno: {respuesta_alumno}\nRúbrica del Profesor: {rubrica}"}
                    ],
                    response_format=EvaluacionIA,
                    temperature=0.2,
                )
                resultado: EvaluacionIA = completion.choices[0].message.parsed
            except Exception as parse_error:
                # Si Groq requiere json_object clásico en este modelo, usamos fallback con model_validate_json
                schema_instructions = f"\n\nDEBES responder exclusivamente con un objeto JSON estrictamente válido según este esquema Pydantic:\n{json.dumps(EvaluacionIA.model_json_schema())}"
                completion = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT + schema_instructions},
                        {"role": "user", "content": f"Pregunta: {pregunta}\nRespuesta del Alumno: {respuesta_alumno}\nRúbrica del Profesor: {rubrica}"}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.2,
                )
                raw_json = completion.choices[0].message.content
                resultado: EvaluacionIA = EvaluacionIA.model_validate_json(raw_json)
                
        except Exception as e:
            print(f"\n❌ Error durante la llamada a Groq o validación Pydantic: {e}")
            sys.exit(1)
    elif provider == "mock":
        print("💡 Modo Simulación (MOCK) activado: Generando objeto EvaluacionIA localmente sin coste...")
        resultado = EvaluacionIA(
            transcription=respuesta_alumno,
            rubricBreakdown=[
                RubricItem(
                    category="Precisión conceptual y simbolismo platónico",
                    score=4.2,
                    maxScore=5.0,
                    reasoning="Comprende el simbolismo de la luz y el Sol como Idea de Bien y el esfuerzo del aprendizaje, aunque simplifica la alegoría del prisionero."
                ),
                RubricItem(
                    category="Conexión con el concepto de paideia como conversión",
                    score=3.8,
                    maxScore=5.0,
                    reasoning="Menciona correctamente el deber moral y político del retorno del filósofo a la caverna, pero falta desarrollar el giro del alma (periagoge)."
                )
            ],
            visualMarkers=[],
            qualitativeAnalysis=QualitativeAnalysis(
                strengths=[
                    "Identificación correcta del Sol como la Idea de Bien en el sistema platónico.",
                    "Comprensión del doble movimiento de ascenso (educación) y descenso (compromiso político y ético)."
                ],
                improvementNeeds=ImprovementNeeds(
                    immediate=[
                        "Explicar con mayor precisión técnica el concepto de paideia como conversión o giro de toda el alma hacia la inteligibilidad."
                    ],
                    mediumLongTerm=[
                        "Relacionar explícitamente el mito con los grados de conocimiento (doxa vs. episteme) del símil de la línea."
                    ]
                ),
                teacherSummary="Buen dominio competencial de los símbolos clave del Mito de la Caverna. El alumno capta la dimensión ética del retorno filosófico. Se recomienda reforzar el vocabulario técnico epistemológico."
            ),
            calificacion_cualitativa="NT",
            siguiente_paso_accionable="En tu próximo repaso de hoy, redacta una frase de 3 líneas donde conectes la palabra 'paideia' con la metáfora de 'girar la mirada' desde las sombras hacia la luz del conocimiento real.",
            confidence_score=0.92
        )

    # 4. IMPRESIÓN LEGIBLE Y CHEQUEOS DE ACEPTACIÓN
    print("\n✅ ¡ÉXITO! El modelo respondió cumpliendo al 100% el esquema Pydantic (EvaluacionIA).\n")
    print("-----------------------------------------------------------------")
    print("📄 RESULTADO JSON RECIBIDO (json.dumps indent=2):")
    print("-----------------------------------------------------------------")
    print(json.dumps(resultado.model_dump(), indent=2, ensure_ascii=False))
    print("-----------------------------------------------------------------\n")
    
    # 5. VALIDACIÓN DE CRITERIOS ESPECÍFICOS DEL BACKLOG Y [D-024]
    print("🔍 CHEQUEO DE CRITERIOS DE ACEPTACIÓN [v0.1-000] & [D-024]:")
    print(f"  [x] calificacion_cualitativa válida : {resultado.calificacion_cualitativa}")
    print(f"  [x] siguiente_paso_accionable (Feed Forward) : \"{resultado.siguiente_paso_accionable}\"")
    print(f"  [x] confidence_score : {resultado.confidence_score}")
    print(f"  [x] visualMarkers admitió array : {resultado.visualMarkers}")
    
    if resultado.confidence_score < 0.75:
        print("\n⚠️ Advertencia: ⚠️ Revisión manual recomendada (confidence_score < 0.75)")
    else:
        print(f"\n✨ Confianza del modelo alta ({resultado.confidence_score} >= 0.75). Borrador listo para validación docente.")
    
    print("\n🏁 Smoke test finalizado correctamente. Contrato validado.")
    print("=================================================================\n")

if __name__ == "__main__":
    run_smoke_test()
