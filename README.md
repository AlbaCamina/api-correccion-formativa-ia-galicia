# api-correccion-formativa-ia-galicia 🎓⚡

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python 3.14+](https://img.shields.io/badge/Python-3.14%2B-blue?style=flat&logo=python)](https://www.python.org/)
[![Groq](https://img.shields.io/badge/LLM-Groq%20%2F%20OpenAI-orange?style=flat)](https://groq.com/)
[![Decreto 157/2022](https://img.shields.io/badge/Normativa-Decreto%20157%2F2022%20Galicia-lightblue?style=flat)](#)
[![Version](https://img.shields.io/badge/Version-v0.1--001-green?style=flat)](#)

API de Corrección Formativa con IA diseñada para asistir al profesorado de **Filosofía de Bachillerato** en la Comunidad Autónoma de Galicia. Estructurada bajo el marco pedagógico oficial de la **LOMLOE**, el **Decreto 157/2022 (Xunta de Galicia)**, y las directrices de privacidad de la Unión Europea (**RGPD / AI Act**).

---

## 🌟 Propuesta de Valor Diferencial

*   **Alineamiento Curricular Gallego:** Diseñada específicamente sobre las competencias clave, competencias específicas y criterios de evaluación de la materia de Filosofía de Bachillerato definidos por la Xunta de Galicia.
*   **Deslinde Formativo vs Sumativo:** El sistema no califica de forma fría; realiza un desglose cualitativo por rúbricas pedagógicas y devuelve un **Siguiente Paso Accionable (Feed Forward)** y un **Índice de Confianza IA** para evitar alucinaciones.
*   **Diseño de Privacidad Pre-Nube (Stealth/Phase Ninja):** Seudonimización local que impide el envío de datos personales identificables del alumnado a las APIs de los modelos de lenguaje (LLM).
*   **Resiliencia Multiproveedor:** Integración directa con OpenAI y Groq con mecanismo dinámico de fallback a `json_object` si falla la API de Structured Outputs de algún proveedor.

---

## 🛠️ Instalación y Ejecución Local (WSL / Ubuntu)

### Prerrequisitos

*   Python 3.12 o superior (probado en Python 3.14)
*   Entorno de WSL (Windows Subsystem for Linux) o Linux

### 1. Clonar e inicializar el entorno

```bash
# Activar entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r backend/requirements.txt
```

### 2. Configurar variables de entorno

Copia el archivo de ejemplo a tu `.env` local:

```bash
cp .env.example .env
```

Abre `.env` y configura tus API Keys reales de Groq/OpenAI o mantén `LLM_PROVIDER=mock` para desarrollo local en memoria sin coste.

### 3. Ejecutar el Servidor FastAPI

```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

El servidor estará accesible en `http://127.0.0.1:8000`. Puedes consultar la documentación interactiva en `http://127.0.0.1:8000/docs`.

### 4. Ejecutar la Suite de Pruebas

```bash
python3 -m unittest discover -s backend/tests/
```

---

## 📡 Integración de la API: POST `/api/v1/evaluate`

Envía la respuesta de un alumno y la rúbrica asociada para obtener la evaluación estructurada en base al contrato estricto de Pydantic.

### Ejemplo de Petición (Request)

```bash
curl -X POST http://127.0.0.1:8000/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "student_answer": "El prisionero sale de la caverna y ve la luz.",
    "rubric": "Criterio 1: Simbolismo conceptual y precisión platónica (0-5 pts)",
    "question": "¿Qué simboliza la salida del prisionero de la caverna?"
  }'
```

### Ejemplo de Respuesta (Response)

```json
{
  "transcription": "El prisionero sale de la caverna y ve la luz.",
  "rubricBreakdown": [
    {
      "category": "Criterio 1: Simbolismo conceptual",
      "score": 3.0,
      "maxScore": 5.0,
      "reasoning": "La respuesta menciona la salida de la caverna y ver la luz, lo cual es parte del simbolismo de la alegoría de la caverna de Platón. Sin embargo, no profundiza en qué representa la caverna o la luz en términos de conocimiento y realidad."
    }
  ],
  "visualMarkers": [],
  "qualitativeAnalysis": {
    "strengths": [
      "Menciona elementos clave de la alegoría de la caverna como la salida y la luz."
    ],
    "improvementNeeds": {
      "immediate": [
        "Desarrollar una explicación más detallada sobre qué representa la caverna en el contexto filosófico."
      ],
      "mediumLongTerm": [
        "Relacionar la salida del prisionero con conceptos como la realidad inteligible de las Ideas."
      ]
    },
    "teacherSummary": "El alumno muestra una comprensión inicial de la alegoría de la caverna, pero necesita profundizar en su significado filosófico."
  },
  "calificacion_cualitativa": "SU",
  "siguiente_paso_accionable": "Investiga y explica qué representan la luz del Sol y el exterior en la alegoría platónica frente a las sombras de la caverna.",
  "confidence_score": 0.95
}
```

---

## 🧠 AI Development Methodology

Este proyecto sigue una metodología de desarrollo acelerada y robusta mediante colaboración con IA:

1.  **Qué diseñé yo (Arquitectura y Prompting):** Diseñé el modelo de datos de la evaluación educativa formativa mediante Pydantic (`EvaluacionIA`), estructuré el flujo del backend síncrono en FastAPI y definí el **Protocolo de Pausa Arquitectónica (*Stop & Consult*)** junto con la lógica de **bifurcación plana por proveedor** (`OpenAI .parse()` vs `Groq json_object` directo con inyección textual de esquema). Esto elimina fallbacks anidados innecesarios y optimiza las políticas de reintento para asegurar un servicio rápido, limpio y tolerante a fallos. Asimismo, redacté el system prompt alineado con el Decreto 157/2022 gallego.
2.  **Qué ejecutaron los agentes (Generación de Código e Infraestructura):** El agente de IA generó los archivos físicos del backend en base a mis directrices de estructuración, configúró las dependencias, inicializó el entorno virtual local de Python, y completó los registros históricos de diseño (`decisiones.md` y `backlog.md`).
3.  **Cómo validé (Pruebas Automatizadas y de Campo):** Validé el comportamiento del backend implementando pruebas unitarias de modelos Pydantic y pruebas de integración para el endpoint `/api/v1/evaluate` usando `TestClient` de FastAPI. Adicionalmente, realicé comprobaciones reales haciendo llamadas contra la API del modelo de lenguaje de Groq (`llama-3.3-70b-versatile`) con respuestas reales simuladas.
4.  **Qué aprendí (Lecciones y Conclusiones):** Aprendí la vital importancia de aplicar el principio PonyTail (Modularidad Plana y YAGNI) y el Protocolo de Pausa Arquitectónica al orquestar agentes de IA: en lugar de permitir que la IA apile parches locales o `try-except` anidados sobre la marcha cuando un proveedor no soporta `.parse()`, la dirección técnica humana es esencial para pausar, analizar el impacto global y bifurcar limpiamente desde el diseño. La automatización del andamiaje ahorra hasta un 80% de tiempo en boilerplate, permitiendo concentrarse en el diseño pedagógico y la fiabilidad.
