import os
import time
import logging
from openai import OpenAI
from backend.models.evaluation import EvaluacionIA
from backend.services.prompt_builder import SYSTEM_PROMPT, build_user_prompt, get_schema_instructions

# Configurar logging básico
logger = logging.getLogger("backend.services.llm_client")
logger.setLevel(logging.INFO)

if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(ch)

def get_llm_client(provider: str) -> OpenAI:
    """
    Retorna el cliente de OpenAI configurado adecuadamente según el proveedor.
    """
    if provider == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or api_key == "tu_api_key_de_groq_aqui":
            raise ValueError("Falta configurar GROQ_API_KEY en las variables de entorno.")
        return OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
    elif provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "tu_api_key_de_openai_aqui":
            raise ValueError("Falta configurar OPENAI_API_KEY en las variables de entorno.")
        return OpenAI(api_key=api_key)
    else:
        raise ValueError(f"Proveedor de LLM '{provider}' no soportado para llamadas reales.")

async def evaluate_answer(student_answer: str, rubric: str, question: str = "") -> EvaluacionIA:
    """
    Llama al LLM (OpenAI o Groq) con el prompt estructurado para evaluar la respuesta del alumno.
    Tiene tolerancia a fallos con un reintento y fallback a json_object si falla el .parse() nativo.
    """
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    model_name = os.getenv("LLM_MODEL", "gpt-4o-mini")

    if provider == "mock":
        logger.info("Modo MOCK activado. Generando respuesta simulada.")
        time.sleep(0.5)  # Simular latencia de red
        from backend.models.evaluation import RubricItem, QualitativeAnalysis, ImprovementNeeds, VisualMarker
        return EvaluacionIA(
            transcription=student_answer,
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
            visualMarkers=[
                VisualMarker(
                    x=12.5,
                    y=45.0,
                    type="error_excluido",
                    comment="El término 'esfuerço' contiene un error ortográfico pero se excluye de penalización por la adaptación de dislexia del alumno."
                )
            ],
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
            confidence_score=0.92,
            ortografia_detectada=["esfuerço"],
            errores_excluidos_por_adaptacion=["esfuerço"]
        )

    client = get_llm_client(provider)
    user_prompt = build_user_prompt(student_answer, rubric, question)

    max_attempts = 2
    last_exception = None

    for attempt in range(1, max_attempts + 1):
        start_time = time.time()
        logger.info(f"Intento {attempt}/{max_attempts} evaluando en {provider.upper()} con {model_name}...")
        try:
            if provider == "groq":
                # Groq: 1 sola llamada directa y limpia con json_object + instrucciones en prompt
                completion = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT + get_schema_instructions()},
                        {"role": "user", "content": user_prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.2,
                )
                raw_json = completion.choices[0].message.content
                if not raw_json:
                    raise ValueError("El LLM retornó contenido vacío.")
                resultado = EvaluacionIA.model_validate_json(raw_json)
            elif provider == "openai":
                # OpenAI: 1 sola llamada directa a Structured Outputs nativos de Pydantic (.parse)
                completion = client.beta.chat.completions.parse(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt}
                    ],
                    response_format=EvaluacionIA,
                    temperature=0.2,
                )
                resultado = completion.choices[0].message.parsed
                if resultado is None:
                    raise ValueError("El parseador del LLM retornó parsed=None.")
            else:
                raise ValueError(f"Proveedor no soportado: {provider}")

            duration = time.time() - start_time
            logger.info(f"¡Éxito! Llamada completada en {duration:.2f}s en intento {attempt}")
            return resultado

        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Fallo en intento {attempt} ({duration:.2f}s): {e}")
            last_exception = e
            if attempt < max_attempts:
                time.sleep(0.5)

    raise RuntimeError(f"Error tras {max_attempts} intentos de llamada formativa a la IA: {last_exception}")
