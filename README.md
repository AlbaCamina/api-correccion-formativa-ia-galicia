# api-correccion-formativa-ia-galicia 🎓⚡

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python 3.14+](https://img.shields.io/badge/Python-3.14%2B-blue?style=flat&logo=python)](https://www.python.org/)
[![PostgreSQL 16](https://img.shields.io/badge/PostgreSQL-16--Alpine-316192?style=flat&logo=postgresql)](https://www.postgresql.org/)
[![Groq](https://img.shields.io/badge/LLM-Groq%20%2F%20OpenAI-orange?style=flat)](https://groq.com/)
[![Decreto 157/2022](https://img.shields.io/badge/Normativa-Decreto%20157%2F2022%20Galicia-lightblue?style=flat)](#)
[![Version](https://img.shields.io/badge/Version-v0.2--002-green?style=flat)](#)

API de Corrección Formativa con IA diseñada para asistir al profesorado de **Filosofía de Bachillerato** en la Comunidad Autónoma de Galicia. Estructurada bajo el marco pedagógico oficial de la **LOMLOE**, el **Decreto 157/2022 (Xunta de Galicia)**, y las directrices de privacidad de la Unión Europea (**RGPD / AI Act / ENS**).

---

## 🌟 Propuesta de Valor Diferencial

*   **Alineamiento Curricular Gallego:** Diseñada específicamente sobre las competencias clave, competencias específicas y criterios de evaluación de la materia de Filosofía de Bachillerato definidos por la Xunta de Galicia (`[D-027] Modo Dual de Rúbrica`).
*   **Deslinde Formativo vs Sumativo (`HitL`):** El sistema no califica de forma fría ni automática; realiza un desglose cualitativo por rúbricas pedagógicas, devuelve un **Siguiente Paso Accionable (Feed Forward)** y un **Índice de Confianza IA** para evitar alucinaciones. El docente siempre conserva la soberanía y firma la nota (`[D-002]`).
*   **Blindaje de Privacidad y Seguridad (`Stealth/Phase Ninja`):** Seudonimización estricta del alumnado en la nube (`alumno_id = "A-14"`) sin cifrado de columnas frágil (`[D-031]`). La libreta de equivalencia con la identidad real del menor reside en exclusiva en el cuaderno local de la profesora, y la autenticación docente se resguarda con hacheo unidireccional irreversible `bcrypt` + sesiones `JWT`.
*   **Resiliencia y Optimización FinOps:** Integración primaria con Groq LPU (`llama-3.3-70b-versatile` en `[D-028]`) con fallback dinámico a `json_object` si falla la API de Structured Outputs de algún proveedor.

---

## 🛠️ Instalación y Ejecución Local (WSL / Ubuntu)

### Prerrequisitos

*   Python 3.12 o superior (probado en Python 3.14 en entorno WSL)
*   Docker y Docker Compose (para el contenedor transaccional de PostgreSQL 16 Alpine)
*   Entorno Linux / WSL (Windows Subsystem for Linux)

### 1. Desplegar la Base de Datos Relacional en Docker

El sistema utiliza un contenedor PostgreSQL aislado expuesto en el **Puerto Dedicado 5433** (`[D-030]`) para evitar colisiones nativas con bases de datos locales:

```bash
docker compose up -d
```

### 2. Clonar e inicializar el entorno virtual Python

```bash
# Activar entorno virtual en WSL
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias del proyecto (incluyendo seguridad passlib[bcrypt], pyjwt y pydantic[email])
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Copia el archivo de ejemplo a tu `.env` local:

```bash
cp .env.example .env
```

Abre `.env` y configura tus API Keys reales de Groq/OpenAI, la cadena `DATABASE_URL` y tu `SECRET_KEY` transaccional para los tokens Bearer.

### 4. Ejecutar las Migraciones Transaccionales de Alembic

Sincroniza el esquema relacional (`profesores` y tablas del sistema) con tu base de datos PostgreSQL:

```bash
alembic upgrade head
```

### 5. Ejecutar el Servidor FastAPI

```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

El servidor estará accesible en `http://127.0.0.1:8000`. Puedes consultar la documentación interactiva Swagger UI en `http://127.0.0.1:8000/docs`.

### 6. Ejecutar la Suite de Pruebas

```bash
python3 -m unittest discover -s backend/tests/
```

---

## 🔒 Autenticación y Seguridad: Endpoints `/api/v1/auth/*` (`[v0.2-002]`)

El backend incorpora autenticación transaccional por token Bearer transaccional, separando el registro docente del login y la validación de sesión.

### 1. Registro Docente: POST `/api/v1/auth/register`

Registra una nueva cuenta de profesora en la tabla `profesores`. La contraseña se hachea matemáticamente con `bcrypt` y jamás se almacena en texto claro ni se devuelve en las respuestas.

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alba.camina@edu.xunta.gal",
    "nombre": "Alba Camiña García",
    "password": "PasswordSeguroGalicia2026"
  }'
```

### 2. Inicio de Sesión (Obtener JWT): POST `/api/v1/auth/login`

Acepta tanto **OAuth2 Form Data** nativo de FastAPI (compatible con el candado de Swagger UI `/docs`) como cargas JSON en `/api/v1/auth/login-json`. Devuelve el Bearer Token JWT transaccional.

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login-json \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alba.camina@edu.xunta.gal",
    "password": "PasswordSeguroGalicia2026"
  }'
```

### 3. Verificar Sesión Activa: GET `/api/v1/auth/me`

Ruta protegida que valida la cabecera `Authorization: Bearer <token>` transaccional.

```bash
curl -X GET http://127.0.0.1:8000/api/v1/auth/me \
  -H "Authorization: Bearer <TU_TOKEN_JWT_AQUI>"
```

---

## 📡 Corrección Formativa con IA: POST `/api/v1/evaluate`

Envía la respuesta de un alumno y la rúbrica asociada para obtener la evaluación cualitativa estructurada en base al contrato estricto de Pydantic.

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

## 🧠 AI Development & Governance Methodology (`Phase Ninja`)

Este proyecto sigue una rigurosa metodología de ingeniería de software acelerada y gobernada mediante colaboración humano-IA (`Human-in-the-Loop` y `PonyTail Coding`):

1.  **Qué diseñé yo (Soberanía Arquitectónica y Prompting):** Diseñé el modelo pedagógico de evaluación educativa mediante Pydantic v2 (`EvaluacionIA`), estructuré el flujo del backend en FastAPI y definí el **Protocolo de Pausa Arquitectónica (*Stop & Consult*)** y el **Freno Conductual** (`Regla 5 de AGENTS.md`) que prohíbe ediciones no autorizadas. Asimismo, dirigí las decisiones de diseño arquitectónico (ADRs `[D-030]` y `[D-031]`), imponiendo la **Seudonimización Estricta (`alumno_id=A-14`)** para los menores en lugar de cifrados de columna con claves maestras frágiles en `.env`, blindando el sistema ante pérdidas catastróficas de datos y garantizando el cumplimiento normativo del **ENS y RGPD**.
2.  **Qué ejecutaron los agentes (Generación de Código e Infraestructura):** El agente orquestado por IA generó los esquemas ORM y Pydantic agrupados en **Modularidad Plana (`backend/models/user.py`)** bajo el principio YAGNI con su respectivo *Scaling Trigger* documentado para el umbral de 8-10 tablas. Además, el agente configuró el contenedor Docker de PostgreSQL en el puerto exclusivo **`5433:5432`**, gestionó las dependencias de seguridad (`passlib[bcrypt]`, `pyjwt`, `pydantic[email]`) y generó de forma automática los scripts de versionado de esquema en `Alembic`.
3.  **Cómo validé yo (Pruebas Unitarias, Terminal y Auditoría por Pares IA):** Validé el comportamiento transaccional ejecutando yo misma en consola WSL la activación de entornos virtuales (`source venv/bin/activate`), la aplicación de migraciones relacionales (`alembic upgrade head`) y los flujos de control de versiones con Git en *Modo Copiloto*. Para certificar el máximo nivel de excelencia y seguridad sin sesgos, sometí la arquitectura de autenticación e invariantes de Pydantic a una **Auditoría de Pares Multi-Motor (`Multi-Agent Peer Review` por Token Multiplexing en Perplexity Pro / ChatGPT / Claude)**, obteniendo una calificación unánime de **10/10 en seguridad práctica sin sobreingeniería**.
4.  **Qué aprendí (Lecciones de FinOps y Gobernanza):** Aprendí que la verdadera maestría en el desarrollo asistido por IA no consiste en dejar que el modelo genere código abstracto sin control, sino en ejercer la dirección técnica mediante protocolos de pausa y revisión por pares entre distintos motores LLM. La modularidad plana combinada con hacheo unidireccional y seudonimización elimina por completo la deuda técnica de la criptografía ad-hoc, logrando un portfolio 100% autoinstalable, auditable y conforme a la ley gallega y europea.

