# api-correccion-formativa-ia-galicia 🎓⚡

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python 3.14+](https://img.shields.io/badge/Python-3.14%2B-blue?style=flat&logo=python)](https://www.python.org/)
[![PostgreSQL 16](https://img.shields.io/badge/PostgreSQL-16--Alpine-316192?style=flat&logo=postgresql)](https://www.postgresql.org/)
[![Groq](https://img.shields.io/badge/LLM-Groq%20%2F%20OpenAI-orange?style=flat)](https://groq.com/)
[![Decretos 156/2022 e 157/2022](https://img.shields.io/badge/Normativa-Decretos%20156%2F2022%20e%20157%2F2022%20Galicia-lightblue?style=flat)](#)
[![Version](https://img.shields.io/badge/Version-v0.3--001-brightgreen?style=flat)](#)

API de Corrección Formativa con IA diseñada para asistir al profesorado de **Filosofía de Bachillerato** en la Comunidad Autónoma de Galicia. Estructurada bajo el marco pedagógico oficial de la **LOMLOE**, los **Decretos 156/2022 y 157/2022 (Xunta de Galicia)** (garantizando el blindaje estricto de la etapa educativa ESO/BACH), y las directrices de privacidad de la Unión Europea (**RGPD / AI Act / ENS**).

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

> ⚠️ **IMPORTANTE — `SECRET_KEY`:** El servidor valida en el arranque que esta variable contenga un valor personalizado y único. Si se deja el valor por defecto del `.env.example`, el proceso **abortará con error crítico**. Genera una clave segura con:
> ```bash
> openssl rand -hex 32
> ```

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

## 📡 API Endpoints

### Implementados

| Endpoint | Verbo | Auth | Descripción |
|---|---|---|---|
| `/health` | `GET` | ❌ Pública | Estado del servidor |
| `/api/v1/auth/register` | `POST` | ❌ Pública | Registro de profesora |
| `/api/v1/auth/login` | `POST` | ❌ Pública | Login → devuelve JWT Bearer |
| `/api/v1/auth/login-json` | `POST` | ❌ Pública | Login en JSON (compatible Swagger) |
| `/api/v1/auth/me` | `GET` | ✅ JWT | Verificar sesión activa |
| `/api/v1/marcos` | `GET` | ✅ JWT | Listar marcos normativos (Xunta) |
| `/api/v1/rubricas` | `POST / GET` | ✅ JWT | Crear y listar rúbricas del docente |
| `/api/v1/evaluate` | `POST` | ✅ JWT | Corrección formativa con IA (`REVIEW`) |

### Próximos (Roadmap)

| Endpoint | Verbo | Versión | Descripción |
|---|---|---|---|
| `/api/v1/submissions/upload` | `POST` | 🔜 v0.3 | Subida de imagen/PDF del examen |
| `/api/v1/evaluaciones/{id}/approve` | `PATCH` | 🔜 v0.3 | Aprobación HitL docente (`REVIEW → GRADED`) |
| `/api/v1/submissions` | `GET` | 🔜 v0.4 | Lista paginada de entregas |
| `/api/v1/submissions/{id}/events` | `GET SSE` | 🔜 v0.4 | Notificación en tiempo real |
| `/api/v1/submissions/{id}/changelog` | `GET` | 🔜 v1.0 | Historial inmutable de auditoría AI Act |

> La documentación interactiva completa (Swagger UI) está disponible en `http://127.0.0.1:8000/docs` al ejecutar el servidor en local.

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

## 📚 Marco Normativo Gallego: GET `/api/v1/marcos` (`[v0.2-003]`)

Devuelve los marcos de evaluación oficiales cargados en la base de datos (Decretos 156/157/2022 de la Xunta de Galicia). El motor de corrección usa estos marcos para evaluar competencias según la legislación vigente (`modo_evaluacion: COMBINADO` o `AUDITORIA_CURRICULAR`).

```bash
curl -X GET http://127.0.0.1:8000/api/v1/marcos \
  -H "Authorization: Bearer <TU_TOKEN_JWT_AQUI>"
```

Respuesta de ejemplo:

```json
[
  {
    "id": 1,
    "nombre": "Filosofía de Bachillerato — Galicia",
    "asignatura": "Filosofía",
    "curso": "1º Bachillerato",
    "etapa": "BACH",
    "estado_activo": true,
    "fuente_legislativa_url": "https://www.xunta.gal/dog/Publicados/2022/20220804/AnuncioG0655-280722-0001_es.html",
    "ultima_verificacion_manual": "2026-07-10"
  }
]
```

---

## 📋 Rúbricas del Docente: POST / GET `/api/v1/rubricas` (`[v0.2-004]`)

Permite al docente crear y recuperar sus rúbricas de corrección personalizadas. Una rúbrica pertenece exclusivamente a la profesora que la creó — ningún otro docente puede acceder ni modificarla.

### Crear una rúbrica: POST `/api/v1/rubricas`

```bash
curl -X POST http://127.0.0.1:8000/api/v1/rubricas \
  -H "Authorization: Bearer <TU_TOKEN_JWT_AQUI>" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Rúbrica Alegoría de la Caverna",
    "criterios": {
      "precision_conceptual": {"peso": 0.5, "descripcion": "Identifica correctamente el simbolismo platónico"},
      "argumentacion": {"peso": 0.3, "descripcion": "Justifica con coherencia filosófica"},
      "expresion_escrita": {"peso": 0.2, "descripcion": "Claridad y estructura del texto"}
    }
  }'
```

### Listar mis rúbricas: GET `/api/v1/rubricas`

```bash
curl -X GET http://127.0.0.1:8000/api/v1/rubricas \
  -H "Authorization: Bearer <TU_TOKEN_JWT_AQUI>"
```

---

## 📡 Corrección Formativa con IA: POST `/api/v1/evaluate` (`[v0.2-004]` - `[v0.2-007]`)

Endpoint protegido por **Token Bearer JWT transaccional** conectado a base de datos PostgreSQL. Valida la pertenencia de la rúbrica al docente que realiza la petición (`[v0.2-004]`), inyecta el marco normativo gallego si se solicita (`modo_evaluacion`), aplica las instrucciones de exclusión pedagógica para adaptaciones NEAE/NEE (Decreto 229/2011) (`[v0.2-007]`), y registra la entrega y la evaluación de forma inmutable (`submissions`, `evaluaciones`, `changelog`).

### Ejemplo de Petición (Request)

> ⚠️ **BREAKING CHANGE (D-041):** El campo `etapa` ("ESO" | "BACH") es obligatorio en el payload. Sin él la API devuelve `422 Unprocessable Entity`, y si su valor contradice la etapa del marco normativo seleccionado devuelve `400 Bad Request`.

Requiere cabecera de autenticación `Authorization: Bearer <token>` transaccional:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/evaluate \
  -H "Authorization: Bearer <TU_TOKEN_JWT_AQUI>" \
  -H "Content-Type: application/json" \
  -d '{
    "student_answer": "El prisionero sale de la caverna y ve el sol o la luz...",
    "rubrica_id": 1,
    "marco_id": 1,
    "etapa": "BACH",
    "modo_evaluacion": "COMBINADO",
    "question": "¿Qué simboliza la salida del prisionero de la caverna?",
    "alumno_id": "A-14",
    "adaptaciones_alumno": {
      "tipo": ["dislexia"],
      "excluir_ortografia": true,
      "tiempo_extra_pct": 35
    }
  }'
```

### Ejemplo de Respuesta (Response: `EvaluacionResponse`)

El servidor guarda la entrega en PostgreSQL y devuelve la evaluación estructurada con marcadores visuales neutros (`type: "error_excluido"`) y registro de ortografía excluida por adaptación. *Nota: En el ejemplo la calificación cualitativa es "NA" (Bachillerato). En ESO la escala oficial es IN, SU, BE, NT, SB (D-042: BE, no BI).*

```json
{
  "submission_id": "8905b4e7-91f8-4cb2-a723-8c43919e1e23",
  "evaluacion_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "estado": "REVIEW",
  "resultado_ia": {
    "transcription": "El prisionero sale de la caverna y ve el sol o la luz...",
    "rubricBreakdown": [
      {
        "category": "Precisión conceptual y simbolismo platónico",
        "score": 4.0,
        "maxScore": 5.0,
        "reasoning": "El estudiante identifica correctamente el Sol y el exterior como símbolos platónicos. Se valora el contenido sin penalizar ortografía según adaptación."
      }
    ],
    "visualMarkers": [
      {
        "x": 12.5,
        "y": 45.0,
        "type": "error_excluido",
        "comment": "Error ortográfico detectado pero NO penalizado (Adaptación Dislexia activa)."
      }
    ],
    "qualitativeAnalysis": {
      "strengths": [
        "Comprende la alegoría y su relación con la luz inteligible."
      ],
      "improvementNeeds": {
        "immediate": [
          "Vincular el papel del filósofo con el retorno a la caverna."
        ],
        "mediumLongTerm": [
          "Relacionar el mito con el dualismo epistemológico platónico."
        ]
      },
      "teacherSummary": "Excelente base conceptual adaptada al perfil NEAE del alumno."
    },
    "calificacion_numerica": 8.0,
    "calificacion_cualitativa": "NA",
    "siguiente_paso_accionable": "Explica en un párrafo por qué el prisionero liberado debe regresar con sus compañeros en la oscuridad.",
    "confidence_score": 0.95,
    "ortografia_detectada": true,
    "errores_excluidos_por_adaptacion": [
      "Falta de tilde en término aislado (excluido por dislexia)."
    ]
  }
}
```

---

## 🎯 Seguimiento Formativo y Auditoría (Feed Forward + HitL) (`[D-026]`)

El backend gestiona el seguimiento formativo del **Siguiente Paso Accionable (`estado_feed_forward`)** de forma independiente a la calificación sumativa del examen (`[D-026]`). El ciclo de vida formativo avanza de manera estrictamente unidireccional: `PENDIENTE` → `REALIZADO_ALUMNO` → `VERIFICADO_EN_PRUEBA_SIGUIENTE`. Cualquier intento de salto no permitido devuelve `409 Conflict`.

### Endpoints de Transición Formativa

| Endpoint transicional | Método | Auth | Descripción |
| :--- | :---: | :---: | :--- |
| `/api/v1/submissions/{id}/feed-forward/realizado` | `PATCH` | ✅ JWT | Marca que el estudiante ha completado su acción de mejora (`REALIZADO_ALUMNO`). |
| `/api/v1/submissions/{id}/feed-forward/verificado` | `PATCH` | ✅ JWT | Confirma que la mejora se ha comprobado en la siguiente evaluación (`VERIFICADO_EN_PRUEBA_SIGUIENTE`). |

### Trazabilidad y Cumplimiento (`[D-002]`)

1. **El motor LLM no persiste nunca el estado formativo:** Aunque la IA devuelva en su evaluación recomendaciones de verificación (`feed_forward_verification_suggestion`), la actualización en BBDD requiere confirmación humana explícita a través de los endpoints transicionables.
2. **Auditoría estructurada en `ChangeLog`:** Cada transición persiste un registro atómico inmutable que separa el cambio de estado (`datos_anteriores` / `datos_nuevos`) del contexto de auditoría (`audit_metadata`, donde se traza si la IA recomendó el cambio y el ID de evaluación vinculada). El `actor` registrado en la base de datos es siempre el profesor autenticado (`PROFESOR_ID_X`).

---


## 🧠 AI Development & Governance Methodology (`Phase Ninja`)

Este proyecto sigue una rigurosa metodología de ingeniería de software acelerada y gobernada mediante colaboración humano-IA (`Human-in-the-Loop` y `PonyTail Coding`):

1.  **Qué diseñé yo (Soberanía Arquitectónica y Prompting):** Diseñé el modelo pedagógico de evaluación educativa mediante Pydantic v2 (`EvaluacionIA`), estructuré el flujo del backend en FastAPI y definí el **Protocolo de Pausa Arquitectónica (*Stop & Consult*)** y el **Freno Conductual** (`Regla 5 de AGENTS.md`) que prohíbe ediciones no autorizadas. Asimismo, dirigí las decisiones de diseño arquitectónico (ADRs `[D-030]` y `[D-031]`), imponiendo la **Seudonimización Estricta (`alumno_id=A-14`)** para los menores en lugar de cifrados de columna con claves maestras frágiles en `.env`, blindando el sistema ante pérdidas catastróficas de datos y garantizando el cumplimiento normativo del **ENS y RGPD**.
2.  **Qué ejecutaron los agentes (Generación de Código e Infraestructura):** El agente orquestado por IA generó los esquemas ORM y Pydantic agrupados en **Modularidad Plana (`backend/models/user.py`)** bajo el principio YAGNI con su respectivo *Scaling Trigger* documentado para el umbral de 8-10 tablas. Además, el agente configuró el contenedor Docker de PostgreSQL en el puerto exclusivo **`5433:5432`**, gestionó las dependencias de seguridad (`passlib[bcrypt]`, `pyjwt`, `pydantic[email]`) y generó de forma automática los scripts de versionado de esquema en `Alembic`.
3.  **Cómo validé yo (Pruebas Unitarias, Terminal y Auditoría por Pares IA):** Validé el comportamiento transaccional ejecutando yo misma en consola WSL la activación de entornos virtuales (`source venv/bin/activate`), la aplicación de migraciones relacionales (`alembic upgrade head`) y los flujos de control de versiones con Git en *Modo Copiloto*. Para certificar el máximo nivel de excelencia y seguridad sin sesgos, sometí la arquitectura de autenticación e invariantes de Pydantic a una **Auditoría de Pares Multi-Motor (`Multi-Agent Peer Review` por Token Multiplexing en Perplexity Pro / ChatGPT / Claude)**, obteniendo una calificación unánime de **10/10 en seguridad práctica sin sobreingeniería**.
4.  **Qué aprendí (Lecciones de FinOps y Gobernanza):** Aprendí que la verdadera maestría en el desarrollo asistido por IA no consiste en dejar que el modelo genere código abstracto sin control, sino en ejercer la dirección técnica mediante protocolos de pausa y revisión por pares entre distintos motores LLM. La modularidad plana combinada con hacheo unidireccional y seudonimización elimina por completo la deuda técnica de la criptografía ad-hoc, logrando un portfolio 100% autoinstalable, auditable y conforme a la ley gallega y europea.

