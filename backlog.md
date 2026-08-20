# 📋 Backlog — API de Corrección Formativa con IA
**Proyecto:** API de Corrección Formativa con IA (`api-correccion-formativa-ia-galicia`)  
**Fecha:** Julio 2026  
**Metodología:** Iterativo por versiones — cada versión es un entregable funcional

> [!IMPORTANT]
> **Definición del Producto:** API de Corrección Formativa con IA (`api-correccion-formativa-ia-galicia`) es un motor de evaluación formativa multinivel y API educativa que opera bajo el rigor pedagógico de los Decretos gallegos y del modelo finlandés (*Feed Forward* + Evaluación competencial cualitativa), el estándar de equidad y adaptaciones curriculares de la LOMLOE, y el máximo blindaje de privacidad técnica europea al nivel del *Datenschutz* alemán (Seudonimización pre-nube + *Human-in-the-Loop*). El sistema es 100% multimodal y omni-canal: procesa **cualquier tipo de prueba evaluable** (exámenes manuscritos en foto, murales de cartulina, redacciones en texto online o capturas y PDFs de presentaciones tipo Canva).

---

> [!NOTE]
> Este backlog está organizado por versión (milestone). Cada historia de usuario incluye criterios de aceptación concretos. Importar como Issues en GitHub Projects asignando la etiqueta de versión correspondiente.
> **Regla de desbloqueo:** si una historia se atasca, se mueve a la siguiente versión y se sigue avanzando. Las versiones son agrupaciones lógicas, no puertas rígidas.

---

## 🏷️ Etiquetas sugeridas para GitHub Issues

| Etiqueta | Color | Uso |
|---|---|---|
| `v0.1` `v0.2` `v0.3` `v0.4` `v0.5` `v1.0` | Azules | Versión a la que pertenece |
| `backend` | Morado | Trabajo en FastAPI/Python |
| `frontend` | Verde | Trabajo en React/Vite |
| `database` | Amarillo | Trabajo en PostgreSQL/SQLAlchemy |
| `infra` | Naranja | Docker, Redis, despliegue |
| `legal` | Rojo | Cumplimiento RGPD / AI Act |
| `docs` | Gris | Documentación y README |

---

## 🔍 Versión 0.0 — Investigación, Arquitectura y Documentación (Fase 0 Completada ✅)

**Objetivo:** Establecer una base arquitectónica, jurídica, pedagógica y de negocio inexpugnable antes de escribir código o iniciar el desarrollo del backend, garantizando que todas las decisiones de diseño estén motivadas y auditablemente registradas (`decisiones.md`).

---

### [v0.0-001] Blindaje jurídico pre-nube y cumplimiento EU AI Act / RGPD
**Como** arquitecta y desarrolladora,  
**quiero** diseñar un sistema de tratamiento de datos personales de menores que sea 100% legal bajo la EU AI Act y el RGPD  
**para** que el producto pueda presentarse con total seguridad jurídica ante inspecciones educativas, la Auditoría o departamentos de orientación [D-002, D-011, D-021, D-022].

**Criterios de aceptación:**
- [x] Adoptado modelo *Human-in-the-Loop* (HitL): la IA propone un borrador formativo; la profesora toma y aprueba la decisión final (`[D-002]`)
- [x] Diseñado el mecanismo de seudonimización pre-nube: recorte de cabecera con `Pillow` (`[D-022]`) más herramienta de tampón manual en Canvas de la PWA para casos de borde fotográficos (nombre en pie o lateral) (`[D-034]`) *(Corregido 24/07: el recorte de producción definitivo ocurre en PWA/Canvas JS — jamás en backend Python. Pillow fue PoC de validación del algoritmo. Ver D-022, D-034 y AUDITORIA.md §5)*
- [x] Almacenamiento nube en *Cold Storage* con purga automática por *Lifecycle Policy* (*Zero Data Retention* / expiración legal `[D-021]`)
- [x] Inmutabilidad probatoria (*append-only*): las correcciones aprobadas (`GRADED`) se bloquean contra edición para preservar la cadena de custodia educativa (`[v0.5-005]`)

**Etiquetas:** `v0.0` `legal` `infra` `docs`

---

### [v0.0-002] Adopción de la Normativa de Evaluación de Galicia (`Decreto 156/2022 y 157/2022`)
**Como** desarrolladora empadronada en A Coruña (Galicia),  
**quiero** que el motor de evaluación adopte el marco autonómico gallego de la Xunta de Galicia como primer `seed` de base de datos (`JSONB`)  
**para** lograr máxima coherencia con mi entorno institucional (Ciudad de las TIC, Auditoría, Polos de Emprendemento) y soportar evaluación por competencias bilingüe [D-001, D-004].

**Criterios de aceptación:**
- [x] Identificados los decretos rectores gallegos: `Decreto 156/2022` (ESO), `Decreto 157/2022` (Bachillerato) y `Orden de 26 de mayo de 2023` de la Consellería de Educación de la Xunta de Galicia
- [x] Modelado el campo de normativa como `JSONB` en la tabla `marcos_evaluacion` para soportar criterios de evaluación y descriptores competenciales sin alterar el esquema SQL (`[D-004]`)
- [x] El contrato del LLM soporta calificación numérica y cualitativa competencial (*Insuficiente, Suficiente, Bien, Notable, Sobresaliente*) con evaluación bilingüe castellano/gallego (`[D-024]`)

**Etiquetas:** `v0.0` `database` `docs`

---

### [v0.0-003] Equidad pedagógica y adaptaciones curriculares para alumnado NEAE/NEE
**Como** profesora,  
**quiero** que el sistema contemple adaptaciones curriculares (dislexia, TDAH, TEA, altas capacidades)  
**para** que el alumnado con dificultades específicas sea evaluado con justicia según el `Decreto 229/2011` de la Xunta de Galicia y la `LOMLOE` [D-023].

**Criterios de aceptación:**
- [x] Elaborada taxonomía técnica en 4 niveles (Medidas ordinarias DEA, ACNS no significativas, ACS significativas y ACIS altas capacidades) documentada en [marco_normativo_y_adaptaciones.md](file:///c:/Users/34636/Desktop/api-correccion/marco_normativo_y_adaptaciones.md)
- [x] Diseñada la columna `adaptaciones_alumno (JSONB)` en `submissions` (`[v0.2-005]`) para inyectar reglas de exclusión ortográfica en el prompt sin que la IA diagnostique
- [x] El contrato JSON clasifica faltas ortográficas en dislexia como marcadores neutros (`ortografia_excluida`) en gris, separándolos del cálculo de nota penalizadora

**Etiquetas:** `v0.0` `ia` `legal` `docs`

---

### [v0.0-004] Benchmarking y aval internacional: Alemania, Países Nórdicos, UK y USA
**Como** investigadora de producto,  
**quiero** contrastar la arquitectura y pedagogía de api-correccion-formativa-ia-galicia contra las prácticas líderes mundiales (Datenschutz alemán, Fobizz, Finlandia/Abitti, FeedbackFruits, Gradescope, NoMoreMarking, Hattie & Timperley en UK)  
**para** blindar nuestras decisiones de diseño con el mayor aval técnico y legal de Europa [D-022, D-023, D-024].

**Criterios de aceptación:**
- [x] **Aval de Privacidad (Alemania — *Datenschutz* / *KMK / Fobizz*):** Verificado que nuestra seudonimización pre-nube (`[D-022]`) es el diseño exacto utilizado para cumplir con la legislación más estricta de Europa
- [x] **Aval de Pedagogía y Equidad (Países Nórdicos — Finlandia / Suecia / *Abitti*):** Verificado que nuestro deslinde entre formativo y sumativo, el desglose cualitativo competencial y el uso de IA para liberar tiempo para tutoría humana con alumnos NEAE (`[D-023]`) siguen el estándar educativo nórdico
- [x] **Actionable Next Steps (Reino Unido — *Feed Forward*):** Resuelto el problema del feedback "cierto pero inútil". El contrato del LLM exige siempre el campo `siguiente_paso_accionable`: una acción concreta y realizable hoy por el alumno (`[D-024]`)
- [x] **Confidence Score (Índice de Confianza IA):** El contrato del LLM devuelve `confidence_score` (`0.0` a `1.0`). Si la certeza en la lectura o interpretación es `< 0.75`, el panel del docente emite una alerta preventiva recomendando verificación visual (`[D-024]`)

**Etiquetas:** `v0.0` `ia` `legal` `docs`

---

### [v0.0-005] Plan estratégico de empleabilidad, incubación y financiación en Galicia
**Como** programadora junior en búsqueda activa de empleo e incubación,  
**quiero** estructurar un plan de negocio y portfolio dual (`Fase Ninja` sin alta vs. `Fase Comercialización`)  
**para** maximizar mis opciones de inserción y acceso a ayudas en el ecosistema gallego y estatal [D-006, D-009, D-010].

**Criterios de aceptación:**
- [x] Documentadas las convocatorias y redes pre-alta en Galicia (`Red de Polos de Emprendemento de la Xunta en A Coruña`, `Explorer UDC A Coruña`, `Talento 45+ Cámara de A Coruña`, `Generación SAVIA`, `PAEM MicroBank hasta 30.000€`)
- [x] Identificado el contacto e itinerario para presentar el MVP funcional en el hub **Ciudad de las TIC / Auditoría de A Coruña** (`[v1.0-005]`)
- [x] Planificadas las ayudas de inicio de actividad en Galicia (`Emprego Autónomo >45 años de 4.000€ a 7.000€ + Cuota Cero`), `Activa Startups Galicia (hasta 40.000€)` y `ENISA Emprendedoras Digitales` para la fase de comercialización futura

**Etiquetas:** `v0.0` `docs`

---

## 🚀 Versión 0.1 — Motor Síncrono (Prueba de concepto) [GitHub Issue #1 (Closed)]

**Objetivo:** Demostrar que la IA puede recibir texto y devolver un JSON estructurado con nota y análisis formativo. Sin base de datos, sin imágenes, sin asincronía.

---

### [v0.1-000] Smoke test del contrato JSON con la IA ⚡ PREREQUISITO

**Como** desarrolladora,  
**quiero** verificar que la API del LLM devuelve exactamente el JSON esperado **antes** de integrarla en FastAPI  
**para** no construir el servidor sobre un contrato que no funciona.

> [!IMPORTANT]
> Esta historia se ejecuta antes que cualquier otra. Si el contrato falla, se rediseña el prompt antes de escribir una sola línea de FastAPI.

**Criterios de aceptación:**
- [ ] Script standalone `smoke_test_llm.py` en la raíz del proyecto que llama directamente a la API de OpenAI o Anthropic (sin FastAPI)
- [ ] El prompt usado es el mismo que se usará en `services/prompt_builder.py`
- [ ] La respuesta contiene los campos: `transcription`, `rubricBreakdown`, `visualMarkers`, `qualitativeAnalysis`
- [ ] `qualitativeAnalysis` incluye: `strengths[]`, `improvementNeeds.immediate[]`, `improvementNeeds.mediumLongTerm[]`, `teacherSummary`
- [ ] Probado con al menos 1 respuesta de alumno de ejemplo (buena, regular o mala)
- [ ] El script imprime el JSON recibido con formato legible (`json.dumps(..., indent=2)`)
- [ ] La respuesta incluye `calificacion_cualitativa` (valor IN/SU/**BE**/NT/SB), `siguiente_paso_accionable` (string no vacío) y `confidence_score` (float 0.0–1.0) según [D-024, D-042]
- [ ] Si `confidence_score < 0.75`, el script imprime una advertencia ("⚠️ Revisión manual recomendada")

**Etiquetas:** `v0.1` `backend`

---

### [v0.1-001] Estructura base del proyecto FastAPI

**Como** desarrolladora,  
**quiero** tener la estructura de carpetas del proyecto configurada  
**para** poder empezar a añadir endpoints de forma ordenada.

**Criterios de aceptación:**
- [x] Carpeta `backend/` con `main.py`, `routers/`, `models/`, `services/`
- [x] Entorno virtual Python configurado (`venv` o `poetry`)
- [x] FastAPI instalado y servidor arrancando en `localhost:8000`
- [x] Endpoint de health check `GET /health` devuelve `{ "status": "ok" }`
- [x] `.gitignore` configurado (excluye `venv/`, `.env`, `__pycache__/`)
- [x] Repositorio Git inicializado (`git init`) y vinculado al repositorio en GitHub (`git remote add origin...`)
- [x] Primer commit y push realizados a GitHub exclusivamente con la documentación de arquitectura y diseño (`*.md`) antes de escribir la primera línea de código
- [x] `AGENTS.md` generado en la raíz del proyecto ejecutando `/init` en OpenCode (contexto persistente para el agente en todas las sesiones)
- [x] Reglas de **PonyTail** añadidas al `AGENTS.md`: el agente aplica el principio de mínimo código (YAGNI + decisión ladder) para reducir tokens y sobre-ingeniería

**Etiquetas:** `v0.1` `backend` `infra`

---

### [v0.1-002] Modelo Pydantic del contrato de salida de la IA

**Como** desarrolladora,  
**quiero** definir el esquema estricto que la IA debe devolver  
**para** que el servidor rechace automáticamente respuestas malformadas.

**Criterios de aceptación:**
- [x] Modelo `EvaluacionIA` con campos: `transcription`, `rubricBreakdown`, `visualMarkers`, `qualitativeAnalysis`
- [x] `qualitativeAnalysis` incluye: `strengths[]`, `improvementNeeds.immediate[]`, `improvementNeeds.mediumLongTerm[]`, `teacherSummary`
- [x] Modelo incluye `calificacion_cualitativa: Literal["IN","SU","BI","NT","SB"]`, `siguiente_paso_accionable: str` y `confidence_score: float` según [D-024] *(Corregido 24/07: "BI" es error tipográfico — valor correcto es "BE" según D-042. Campo ahora `Optional`: `null` en BACH, enum oficial en ESO — D-049)*
- [x] `visual_markers: Optional[List[VisualMarker]] = []` — array vacío válido en v0.1 (texto plano, sin imagen). El prompt instruye al LLM a devolver `[]` cuando no hay imagen.
- [x] Si la IA devuelve un JSON sin algún campo obligatorio, Pydantic lanza error 422
- [x] Test unitario que valida un JSON correcto, uno incorrecto, y uno con `visual_markers: []`

**Etiquetas:** `v0.1` `backend`

---

### [v0.1-003] Endpoint de corrección síncrona (texto plano)

**Como** profesor,  
**quiero** enviar el texto de una respuesta de alumno junto con una rúbrica  
**para** recibir una corrección estructurada con nota y análisis formativo.

**Criterios de aceptación:**
- [x] `POST /api/v1/evaluate` acepta `{ "student_answer": string, "rubric": string }`
- [x] El servidor llama a la API de OpenAI/Anthropic con un prompt estructurado
- [x] La respuesta de la IA se valida con el modelo Pydantic de `v0.1-002`
- [x] Si la IA devuelve JSON inválido, el servidor reintenta una vez antes de devolver error 500
- [x] Devuelve el objeto `EvaluacionIA` completo con código 200
- [x] Tiempo de respuesta documentado en los logs
- [x] El cliente del LLM (`llm_client.py`) implementa bifurcación plana de formato según `LLM_PROVIDER` (`OpenAI .parse()` vs `Groq json_object` directo con inyección textual de esquema, [D-028]), refactorizado bajo el *Protocolo de Pausa Arquitectónica* ([D-029])

**Etiquetas:** `v0.1` `backend`

---

### [v0.1-004] Ingeniería del prompt base

**Como** desarrolladora,  
**quiero** definir el System Prompt que instruye a la IA  
**para** que evalúe con criterios pedagógicos reales y devuelva siempre el formato correcto.

**Criterios de aceptación:**
- [x] System prompt en archivo separado `services/prompt_builder.py`
- [x] El prompt instruye a la IA a actuar como "evaluador formativo experto en **Filosofía de Bachillerato**, educación secundaria gallega (Decreto 157/2022, Xunta de Galicia)" (asignatura hardcoded en v0.1 — dinámica desde v0.2 vía `marco_id`)
- [x] El prompt exige explícitamente el formato JSON del contrato
- [x] El prompt diferencia entre mejoras inmediatas y a medio/largo plazo
- [x] Probado con al menos 3 respuestas de alumno distintas (buena, regular, mala)

**Etiquetas:** `v0.1` `backend`

---

### [v0.1-005] Gestión de errores y códigos HTTP

**Como** consumidor de la API,  
**quiero** recibir mensajes de error claros y códigos HTTP correctos  
**para** saber exactamente qué ha fallado sin tener que leer logs del servidor.

**Criterios de aceptación:**
- [x] `400` si el body de la petición está mal formado o faltan campos
- [x] `422` si los datos no pasan validación de Pydantic
- [x] `500` si la IA falla o devuelve JSON inválido tras el reintento
- [x] Todos los errores devuelven `{ "error": string, "detail": string }`
- [x] Los errores se registran en log con timestamp

**Etiquetas:** `v0.1` `backend`

---

### [v0.1-006] Variables de entorno y configuración

**Como** desarrolladora,  
**quiero** gestionar las claves de API y configuración mediante variables de entorno  
**para** no exponer credenciales en el repositorio.

**Criterios de aceptación:**
- [x] Archivo `.env.example` con todas las variables necesarias (sin valores reales)
- [x] `API_KEY_OPENAI` o `API_KEY_ANTHROPIC` cargadas desde `.env`
- [x] El servidor no arranca si falta una variable de entorno requerida
- [x] `.env` añadido a `.gitignore`

**Etiquetas:** `v0.1` `backend` `infra`

---

### [v0.1-007] README inicial del proyecto

**Como** visitante del repositorio en GitHub,  
**quiero** entender qué es el proyecto y cómo ejecutarlo  
**para** evaluar el trabajo o contribuir.

**Criterios de aceptación:**
- [x] Descripción del proyecto y propuesta de valor diferencial
- [x] Instrucciones de instalación y ejecución local
- [x] Ejemplo de petición y respuesta del endpoint `POST /api/v1/evaluate`
- [x] Sección `## AI Development Methodology` con los 4 elementos del marco narrativo de BLOQUE 8: qué diseñé yo / qué ejecutaron los agentes / cómo validé / qué aprendí — usando el lenguaje de arquitecta/orquestadora, no el lenguaje defensivo
- [x] Badges de versión y estado

**Etiquetas:** `v0.1` `docs`

---

## 🗄️ Versión 0.2 — Base de Datos [GitHub Issue #2 (Open)]

**Objetivo:** La normativa gallega (Decretos 156/157/2022, Xunta de Galicia) y las rúbricas del profesor dejan de estar hardcoded y pasan a ser datos dinámicos almacenados en PostgreSQL.

---

### [v0.2-001] Configuración de PostgreSQL y SQLAlchemy

**Como** desarrolladora,  
**quiero** conectar la API a una base de datos PostgreSQL  
**para** poder persistir y recuperar datos de forma transaccional.

**Criterios de aceptación:**
- [x] Docker Compose con servicio PostgreSQL levantando en `localhost:5433` (`[D-030]`)
- [x] SQLAlchemy configurado con connection pool (`backend/models/database.py`)
- [x] Alembic configurado para migraciones (`alembic.ini` + `alembic/env.py`)
- [x] Primera migración vacía ejecutada correctamente (`initial empty revision`)
- [ ] *Nota de Deuda/Sincronización:* Generar y aplicar las revisiones de migración de Alembic para sincronizar el historial formal de migraciones con las columnas del esquema actual en BBDD (`estado_feed_forward` y `audit_metadata`) → ver `[v0.2-008]`.


**Etiquetas:** `v0.2` `database` `infra`

---

### [v0.2-002] Modelo de datos: Profesor y autenticación básica

**Como** profesora,  
**quiero** tener una cuenta en el sistema  
**para** que mis rúbricas y correcciones sean privadas.

**Criterios de aceptación:**
- [x] Tabla `profesores` con campos: `id`, `email`, `nombre`, `created_at` (`[ADR D-031 hacheo bcrypt]`)
- [x] `POST /api/v1/auth/register` crea un profesor
- [x] `POST /api/v1/auth/login` devuelve JWT (`OAuth2PasswordBearer` / `login-json`)
- [x] Rutas protegidas requieren JWT válido en header `Authorization` (`get_current_profesor`)


**Etiquetas:** `v0.2` `backend` `database`

---

### [v0.2-003] Modelo de datos: Marco de Evaluación (normativa como variable)

**Como** desarrolladora,  
**quiero** almacenar la normativa gallega (Xunta/LOMLOE) como un registro en base de datos  
**para** que cambios legislativos solo requieran actualizar un registro (no el código), y para que el sistema pueda escalar a otras comunidades autónomas sin modificar la arquitectura.

**Criterios de aceptación:**
- [x] Tabla `marcos_evaluacion` con campos: `id`, `nombre`, `asignatura`, `curso`, `estado_activo`, `rubrica_completa` (JSONB) y metadatos de vigencia legislativa: `ultima_verificacion_manual` (DATE/nullable) y `normativa_fuentes` (JSON list: `{tipo, numero, fecha, url, vigente_desde, vigente_hasta}`) [D-033, D-046 — Issue #12]
- [x] Seed con al menos un marco de evaluación real de Bachillerato o ESO (Decreto autonómico de la Xunta de Galicia) incluyendo fecha de verificación actual
- [x] `GET /api/v1/marcos` devuelve todos los marcos activos
- [x] El endpoint de evaluación acepta `marco_id` para usar el marco correspondiente

**Etiquetas:** `v0.2` `backend` `database`

---

### [v0.2-004] Modelo de datos: Rúbrica del docente

**Como** profesora,  
**quiero** crear y guardar mis propias rúbricas de corrección  
**para** que interactúen con la normativa oficial al evaluar.

> [!NOTE]
> **Dilema arquitectónico original planteado en v0.1:** ¿cómo interactúan la rúbrica del docente y el marco normativo en el prompt? 
> ✅ **Decisión Resuelta (`[D-027]`):** Se adopta un **Modo Flexible y Multicriterio de Evaluación** seleccionable desde la PWA:
> - **`RÚBRICA PURA` (Evaluación General):** Se activa si no se proporciona `marco_id` (`marco_id` es `null`). El motor LLM evalúa utilizando únicamente la rúbrica del docente, sin cruzar con legislación.
> - **`COMBINADO` (Evaluación Rápida Cotidiana):** Requiere `marco_id`. El motor LLM fusiona de forma aditiva los saberes básicos oficiales y los criterios específicos de la rúbrica del docente para calificar con agilidad bajo la LOMLOE.
> - **`AUDITORIA_CURRICULAR` (Coherencia e Inspección Pedagógica):** Requiere `marco_id`. El motor corrige la entrega pero además audita la coherencia de la rúbrica docente contra la ley, informando confidencialmente en `teacherSummary` si la rúbrica omite competencias básicas obligatorias.

**Criterios de aceptación:**
- [x] Tabla `rubricas_docente` con campos: `id`, `profesor_id`, `nombre`, `criterios` (JSONB), `created_at`
- [x] CRUD completo: `POST`, `GET`, `PUT`, `DELETE /api/v1/rubricas`
- [x] Una rúbrica solo puede ser editada por su propietario
- [x] Validación con Pydantic de la estructura de `criterios` y soporte del modo flexible en peticiones de evaluación ([D-027])

**Etiquetas:** `v0.2` `backend` `database`

---

### [v0.2-005] Modelo de datos: Submission con campo alumno_id

**Como** desarrolladora,  
**quiero** preparar la tabla de entregas desde el principio con el campo `alumno_id`  
**para** mantener el anonimato del estudiante en la nube mediante seudonimización y que la profesora pueda cruzar después ese identificador con su lista local de clase sin exponer datos personales (cumplimiento RGPD).

**Criterios de aceptación:**
- [x] Tabla `submissions` con campos: `id`, `profesor_id`, `marco_id` (nullable), `rubrica_id`, `alumno_id` (nullable, anonimizado), `adaptaciones_alumno` (JSONB, nullable) [D-023], `estado` (PENDING/ANALYZING/REVIEW/GRADED), `estado_feed_forward` (PENDIENTE/REALIZADO_ALUMNO/VERIFICADO_EN_PRUEBA_SIGUIENTE) [D-026], `created_at`, `updated_at`
- [x] Tabla `evaluaciones` con campos: `id`, `submission_id`, `resultado_ia` (JSONB), `nota_final`, `aprobado_por_profesor`, `created_at`
- [x] Tabla `changelog` con campos: `id`, `submission_id`, `accion`, `actor`, `datos_anteriores` (JSONB), `datos_nuevos` (JSONB), `audit_metadata` (JSONB, nullable) [D-002], `timestamp`

**Etiquetas:** `v0.2` `database`

---

### [v0.2-006] Endpoint de evaluación actualizado con BBDD

**Como** profesor,  
**quiero** que la corrección use mi rúbrica y opcionalmente el marco normativo seleccionado  
**para** que la evaluación sea flexible y aplicable tanto a actividades diarias como a exámenes formales.

**Criterios de aceptación:**
- [x] `POST /api/v1/evaluate` ahora acepta `marco_id` (opcional/nullable) y `rubrica_id`
- [x] ⚠️ **BREAKING CHANGE (D-041):** `etapa` (`"ESO" | "BACH"`) pasa a ser un campo obligatorio en el payload. Peticiones sin etapa fallarán con `422`.
- [x] Si el profesor declara una etapa que contradice al marco seleccionado, se rechaza con `400 Bad Request`.
- [x] Si `marco_id` es null/None, evalúa en Modo Rúbrica Pura (ignora legislación) pero inyecta la `etapa` provista en la petición para evitar inferencias normativas por la IA.
- [x] El resultado se guarda en `submissions` y `evaluaciones`
- [x] El changelog registra la corrección con `actor = "IA"`

**Etiquetas:** `v0.2` `backend` `database`

---

### [v0.2-007] Adaptaciones curriculares para alumnado NEAE/NEE (`JSONB`)

**Como** profesora,  
**quiero** configurar adaptaciones curriculares en el perfil de mi alumno (ej. dislexia, TDAH, TEA)  
**para** que el sistema detecte y reporte los errores lingüísticos u ortográficos, pero los excluya automáticamente de la penalización en la nota del examen [D-023].

**Criterios de aceptación:**
- [x] La tabla `submissions` incluye la columna `adaptaciones_alumno (JSONB, nullable)` con estructura: `{"tipo": ["dislexia"], "excluir_ortografia": true, "tiempo_extra_pct": 35}`
- [x] `POST /api/v1/evaluate` extrae las adaptaciones de la entrega y condicionalmente añade al prompt del LLM instrucciones precisas para separar faltas ortográficas del cálculo penalizador de nota
- [x] El contrato JSON devuelto por el LLM incorpora los campos `ortografia_detectada` y `errores_excluidos_por_adaptacion`
- [x] Los marcadores visuales sobre la imagen correspondientes a errores ortográficos excluidos por adaptación se clasifican como neutros (`tipo: "ortografia_excluida"`) para mostrarse en gris/neutro y no en rojo en la PWA
- [x] Protección de privacidad (LOPDGDD art.7): la IA jamás infiere o diagnostica NEAE; solo ejecuta la instrucción recibida y solo el profesor asignado puede acceder a dicha configuración

**Etiquetas:** `v0.2` `backend` `ia` `compliance`

---

### [v0.2-008] Deuda Técnica: Sincronización de Migraciones Alembic y Cobertura HTTP 403 en Feed Forward

**Como** desarrolladora y auditora técnica,  
**quiero** saldar la deuda técnica de sincronización y testing identificada durante la implementación del seguimiento formativo (`PR #7`)  
**para** mantener el historial de migraciones alineado con el esquema y verificar el rechazo por permisos en los nuevos endpoints.

**Criterios de aceptación:**
- [x] **Sincronización Alembic:** Crear la revisión de migración (`alembic revision --autogenerate -m "add estado_feed_forward and audit_metadata"`) como deuda de sincronización del historial formal con el esquema actual de SQLAlchemy (no representa un fallo funcional del backend, sino una alineación de versionado de BBDD).
- [x] **Migración Pendiente Extra (Deuda Técnica):** Aislar y ejecutar la migración específica para sincronizar las columnas `audit_metadata` (en `changelog`) y `estado_feed_forward` (en `submissions`) con la base de datos, ya que fueron añadidas a los modelos en commits anteriores pero no migradas.
- [x] **Test HTTP 403 (Permisos de propiedad):** Añadir un fixture con un segundo profesor (`PROFESOR_ID_2`) en `test_evaluation_router.py` y verificar que si intenta llamar a `PATCH /api/v1/submissions/{id}/feed-forward/realizado` o `/verificado` sobre una entrega que no le pertenece, el backend rechaza con `403 Forbidden`.

**Etiquetas:** `v0.2` `tech-debt` `tests` `database`

---

### [v0.2-009] Endpoint HitL de Aprobación Docente (REVIEW ➔ GRADED)

**Como** profesor responsable de la evaluación,  
**quiero** validar y aprobar formalmente el borrador de corrección propuesto por la IA  
**para** convertirlo en una calificación final firme (`GRADED`), garantizando la soberanía humana (`[D-002]`, `AI Act`).

**Criterios de aceptación:**
- [x] `PATCH /api/v1/evaluaciones/{id}/approve` (o `/submissions/{id}/approve`) verifica que el profesor autenticado es el propietario (`HTTP 403 Forbidden` en caso contrario).
- [x] Transiciona el estado de la entrega de `REVIEW` a `GRADED`.
- [x] Registra en `ChangeLog` la acción `EVALUACION_APROBADA` con el `actor = PROFESOR_ID_{id}` (nunca la IA ni el sistema).
- [x] Al completarse, actualiza la fila correspondiente del flujo de evaluación en `AUDITORIA.md` a **Auditado**.

**Etiquetas:** `v0.2` `hitl` `endpoints` `ai-act`

---

### [v0.2-010] Endpoints GET de Consulta y Trazabilidad

**Como** desarrolladora y ponente técnica en la demostración ante la Auditoría,  
**quiero** disponer de endpoints de lectura limpios para listar entregas y consultar el detalle evaluativo  
**para** poder navegar por el flujo completo en vivo en la interfaz de Swagger UI (`/docs`) y verificar la trazabilidad sin consultar la base de datos a mano.

**Criterios de aceptación:**
- [x] `GET /api/v1/submissions` devuelve el listado de entregas pertenecientes al profesor autenticado (`current_user`).
- [x] `GET /api/v1/evaluaciones/{submission_id}` devuelve el JSON evaluativo estructurado (`EvaluacionIA`) y sus metadatos.
- [x] Pruebas unitarias correspondientes en verde en `test_evaluation_router.py`.
- [x] Al completarse, refuerza el pilar de evidencia y visibilidad en `AUDITORIA.md`.

**Etiquetas:** `v0.2` `endpoints` `swagger` `auditoría-demo`

---

### [v0.2-012] Seed de Normativa ESO (Decreto 156/2022)

**Como** desarrolladora,  
**quiero** disponer de un registro base (`seed`) en la BBDD con la normativa oficial de la ESO en Galicia  
**para** poder testear el flujo completo multi-etapa y verificar que el endpoint rechaza contradicciones entre el marco y la etapa (`[D-041]`).

**Criterios de aceptación:**
- [x] Archivo `seed_eso.py` o script equivalente que inyecte un marco de evaluación bajo el Decreto 156/2022 de Galicia.
- [x] Contiene saberes básicos y competencias clave expresadas con la escala cualitativa oficial de ESO (`IN, SU, BE, NT, SB`).
- [x] Validado en entorno local para confirmar que `GET /api/v1/marcos` lo expone correctamente junto al de Bachillerato.

**Etiquetas:** `v0.2` `database` `seed`

---

## 📸 Versión 0.3 — Subida de Imágenes, Anonimización y OCR [GitHub Issue #3 (Open)]

**Objetivo:** El profesor puede subir una foto o PDF del examen manuscrito. La privacidad se garantiza mediante recorte de cabecera en la **PWA del cliente (JavaScript/Canvas)** antes de que el archivo toque la red — el nombre del alumno jamás alcanza el servidor (`[D-022]`, `[D-034]`). El backend recibe únicamente el archivo ya seudonimizado, gestiona el almacenamiento y envía la imagen al motor multimodal (Groq Vision / OpenAI).

---

### [v0.3-001] Endpoint de subida de archivo (multipart)

**Como** profesora,  
**quiero** subir una foto del examen desde mi dispositivo  
**para** que el sistema la procese sin necesidad de transcribir el texto manualmente.

**Criterios de aceptación:**
- [x] `POST /api/v1/submissions/upload` acepta `multipart/form-data` con imagen (JPG, PNG, HEIC) o PDF
- [x] Tamaño máximo en backend: 25 MB (tolerancia para fotos puras o PDFs escaneados de múltiples páginas sin dar error al usuario)
- [x] Nota de arquitectura [D-020]: aunque el servidor acepte hasta 25 MB, la PWA en `v0.5-002` comprimirá y redimensionará localmente el archivo antes de enviarlo para optimizar red y tokens.
- [x] Formatos rechazados devuelven 400 con mensaje claro
- [x] El archivo se guarda en carpeta local `/uploads` (simulando S3) con nombre UUID

**Etiquetas:** `v0.3` `backend`

---

### [v0.3-002] Anonimización Client-Side: Recorte de Cabecera en PWA (JavaScript/Canvas) `[D-022]` `[D-034]`

**Como** docente, **quiero** que la PWA recorte automáticamente el 20% superior del folio (cabecera con nombre del alumno) **en mi propio navegador** antes de enviarlo al servidor, **para** garantizar que ningún dato personal del alumno alcance nunca la nube (Zero Data Retention absoluto).

> [!IMPORTANT]
> Arquitectura invariante: la función de recorte vive en `frontend/src/utils/imageCrop.js` (JavaScript/Canvas API). El backend Python **solo recibe el archivo ya recortado y seudonimizado** — jamás el original con PII.

**Criterios de aceptación:**
- [ ] Función pura `cropHeader(imageData, ratio = 0.20)` en `frontend/src/utils/imageCrop.js`
- [ ] La función recibe un `HTMLCanvasElement` o `ImageBitmap` y devuelve el cuerpo evaluable (sin cabecera)
- [ ] Separación estricta de lógica pura (cálculo de recorte) e I/O (upload del resultado)
- [ ] Tests en **Vitest** cubriendo:
  - [ ] Ratio estándar `0.20`: dado folio 794×1123px → cuerpo resultante 794×899px
  - [ ] Ratio personalizado (`0.15`, `0.25`): verificar proporcionalidad
  - [ ] Conservación de píxeles: `cabecera.alto + cuerpo.alto === original.alto`
  - [ ] Caso borde `ratio = 0.0`: cuerpo === imagen completa
  - [ ] Caso borde `ratio = 1.0`: cuerpo vacío
- [ ] Nota histórica: el algoritmo fue validado matemáticamente en `scratch/pillow_crop_test.py` (PoC 24/07/2026, ignorado por git) antes de portarse a JS

**Etiquetas:** `v0.3` `frontend` `legal` `rgpd`


---

### [v0.3-003] Almacenamiento Resiliente y Desacoplado (`STORAGE_PROVIDER=local|cloudinary`)

**Como** desarrolladora y docente,  
**quiero** contar con una capa de almacenamiento flexible controlada por variable de entorno (`STORAGE_PROVIDER=local|cloudinary`),  
**para** operar de forma autónoma en modo local/stealth y escalar a Cloudinary cuando se requiera persistencia en nube.

**Criterios de aceptación:**
- [ ] Creación de servicio abstracto `StorageService` capaz de alternar de proveedor según la configuración en `.env`.
- [ ] Si `STORAGE_PROVIDER=local`, las imágenes anonimizadas se sirven desde el sistema de archivos local (`/uploads`) y se registran en `submissions.archivos_urls` como rutas locales/relativas.
- [ ] Si `STORAGE_PROVIDER=cloudinary`, las imágenes ya anonimizadas (`[v0.3-002]`) se suben a la nube vía SDK de Cloudinary y se almacena la lista de URLs públicas seguras en `submissions.archivos_urls`.
- [ ] Eliminación de archivos temporales de trabajo tras completarse con éxito la subida o persistencia final (`Cold Storage` [D-021]).

**Etiquetas:** `v0.3` `backend` `infra`

---

### [v0.3-004] Integración con Modelo Multimodal de Visión (`Groq LPU Vision` / Fallback)

**Como** profesora,  
**quiero** que el sistema lea el examen manuscrito automáticamente desde la imagen anonimizada  
**para** transcribir su contenido y evaluarlo contra la rúbrica sin intervención manual de picado de datos.

**Criterios de aceptación:**
- [ ] El cliente LLM (`llm_client.py`) incorpora soporte para modelos multimodales usando `gpt-4o-mini` en OpenAI (modelo Vision activo, ver [D-051]). El modelo soporta imagen vía URL o Base64 y Structured Outputs nativos para el JSON.
- [ ] El servicio recupera `submissions.archivos_urls` (o rutas locales) y adjunta la imagen (en Base64 si es local o URL si es nube) al payload del prompt formativo.
- [ ] El modelo multimodal retorna el contrato JSON estructurado (`EvaluacionIA`), incluyendo la transcripción fiel (`transcription`) del examen manuscrito.
- [ ] Si la caligrafía presenta tramos ilegibles, el modelo los marca pedagógicamente con `[ILEGIBLE]` y sus coordenadas aproximadas sin romper la validación Pydantic del contrato.
- [ ] El resultado y los marcadores visuales (`visualMarkers`) calculados se guardan en `evaluaciones.resultado_ia`.

**Etiquetas:** `v0.3` `backend` `ia` `vision`

---

### [v0.3-005] Migración Urgente de Motor LLM (Deuda Técnica / D-053)

**Como** desarrolladora,  
**quiero** migrar el motor de texto de Groq a OpenAI ante la deprecación inminente de `llama-3.3-70b-versatile`  
**para** garantizar que el sistema no se rompa el 16/08/2026.

**Criterios de aceptación:**
- [x] Probar Qwen en Groq como primera alternativa (fallida: no soporta JSON complejo).
- [x] Migrar el motor de texto a OpenAI (`gpt-4o-mini`) unificando texto y visión.
- [x] Actualizar `llm_client.py`, `.env` y eliminar SDK de Groq.
- [x] Registrar la decisión formal en ADR `[D-053]`.
- [x] Validar que `pytest` pasa en verde con la nueva configuración unificada.

**Etiquetas:** `v0.3` `tech-debt` `llm`

---

### [v0.3-006] Pipeline Completo: Upload → Transcribir → Evaluar `[D-022]` `[D-053]` ✅

**Como** docente, **quiero** un flujo unificado que suba, transcriba y evalúe en una sola petición, **para** simplificar la experiencia de corrección.

**Criterios de aceptación:**
- [x] `POST /api/v1/submissions/upload-and-evaluate` acepta `multipart/form-data` + metadatos JSON (`rubrica_id`, `marco_id`, `alumno_id`)
- [x] El backend valida las proporciones del archivo (señal de recorte en cliente)
- [x] Orquestación: `StorageService.upload()` → `vision_service.transcribir_imagen()` → `llm_client.evaluate()`
- [x] Respuesta incluye el contrato `EvaluacionIA` completo con `transcription` relleno
- [x] Pipeline documentado en `README.md`

**Etiquetas:** `v0.3` `backend` `endpoints`

---

## ⚡ Versión 0.4 — Asincronía y Colas de Tareas

**Objetivo:** El servidor puede recibir múltiples exámenes simultáneamente sin bloquearse. El profesor recibe una notificación cuando cada corrección termina.

---

### [v0.4-001] Configuración de Redis y Celery

**Como** desarrolladora,  
**quiero** configurar Redis como broker de mensajes y Celery como sistema de workers  
**para** poder procesar correcciones en segundo plano.

**Criterios de aceptación:**
- [ ] Redis añadido a Docker Compose
- [ ] Celery configurado con Redis como broker y result backend
- [ ] Worker arranca con `celery -A app.worker worker --loglevel=info`
- [ ] Tarea de prueba `ping` ejecutada correctamente desde FastAPI

**Etiquetas:** `v0.4` `backend` `infra`

---

### [v0.4-002] Endpoint asíncrono de evaluación

**Como** profesora,  
**quiero** subir una entrega con sus folios y recibir confirmación inmediata  
**para** poder seguir trabajando mientras la IA lo procesa.

**Criterios de aceptación:**
- [x] `POST /api/v1/submissions/upload-and-evaluate` acepta imagen recortada o PDF devolviendo `{ "submission_id": "...", "status": "ANALYZING", "message": "Procesamiento de evaluación iniciado en segundo plano." }` (`202 Accepted`) en <500ms [D-055].
- [x] La tarea de corrección multimodal se ejecuta de forma asíncrona vía FastAPI BackgroundTasks (`procesar_evaluacion_en_segundo_plano`) y no bloquea el hilo del servidor HTTP.
- [x] `GET /api/v1/submissions` y `GET /api/v1/submissions/{id}` devuelven el estado actual (ANALYZING/REVIEW/GRADED/ERROR).
- [x] La tarea de segundo plano actualiza el estado a `REVIEW`, persiste la evaluación y el `ChangeLog` (o `ERROR` con trazabilidad si ocurre un fallo).

**Etiquetas:** `v0.4` `backend` `async` `backgroundtasks`


---

### [v0.4-003] Notificación al cliente (Server-Sent Events)

**Como** profesora,  
**quiero** que el panel web me avise automáticamente cuando la corrección esté lista  
**para** no tener que recargar la página manualmente.

**Criterios de aceptación:**
- [ ] `GET /api/v1/submissions/{id}/events` abre un stream SSE
- [ ] El cliente recibe evento `{ "type": "STATUS_UPDATE", "status": "GRADED" }` cuando termina el worker
- [ ] La conexión SSE se cierra automáticamente tras recibir el evento `GRADED`
- [ ] Si el cliente se desconecta, el servidor cierra el stream limpiamente

**Etiquetas:** `v0.4` `backend`

---

### [v0.4-004] Prueba de carga — 5 exámenes simultáneos

**Como** desarrolladora,  
**quiero** verificar que el servidor no colapsa con varias correcciones a la vez  
**para** poder afirmar con confianza que la arquitectura es robusta.

**Criterios de aceptación:**
- [ ] 5 peticiones simultáneas de corrección procesadas sin errores 500
- [ ] El servidor responde a todas en menos de 1 segundo con `202 Accepted`
- [ ] Todas las correcciones completan en menos de 3 minutos
- [ ] Los logs muestran las 5 tareas ejecutándose en workers distintos

> [!NOTE]
> **Implementación MVP:** Se usa `FastAPI BackgroundTasks` como implementación real en v0.4. El README documenta que en producción a escala se reemplazaría por Celery + Redis Worker dedicado. Esto demuestra conocimiento arquitectónico sin bloquear el desarrollo con la complejidad de configuración de Celery en WSL. Celery queda documentado como mejora futura en `## Roadmap`.

**Etiquetas:** `v0.4` `backend` `infra`

---

## 🖥️ Versión 0.5 — Frontend React PWA

**Objetivo:** Interfaz visual completa que funciona en móvil, tablet y escritorio. El profesor puede escanear, ver el análisis y aprobar la corrección.

---

### [v0.5-001] Estructura base React + Vite + PWA

**Como** desarrolladora,  
**quiero** tener el proyecto React configurado como PWA  
**para** que funcione en cualquier dispositivo sin necesidad de instalación desde tienda.

**Criterios de aceptación:**
- [ ] Carpeta `frontend/` con React + Vite configurado
- [ ] `vite-plugin-pwa` instalado y configurado con `manifest.json`
- [ ] La app es instalable desde el navegador en móvil mediante `manifest.json` ("Añadir a pantalla de inicio" sin pasar por tienda [D-007])
- [ ] Configuración de HTTPS local en Vite (`vite-plugin-mkcert` o túnel) para habilitar pruebas de cámara en dispositivos de la red Wi-Fi
- [ ] Service worker registrado y estructura preparada para redimensión en cliente [D-020] y recorte de cabeceras pre-nube [D-022]
- [ ] Diseño responsive desde móvil (360px) hasta pantalla grande (1440px)

**Etiquetas:** `v0.5` `frontend`

---

### [v0.5-002] Pantalla de captura / subida de examen

**Como** profesor,  
**quiero** poder usar la cámara de mi móvil o subir un archivo desde mi PC  
**para** enviar el examen al sistema sin importar qué dispositivo use.

**Criterios de aceptación:**
- [ ] En móvil/tablet: botón para capturar uno o múltiples folios con la cámara trasera
- [ ] En PC: input de subida de archivos múltiples (JPG, PNG) o documento PDF multi-página
- [ ] Compresión y redimensión en cliente [D-020]: las imágenes se reducen automáticamente a ~2048px en su lado largo (~800 KB) antes del envío
- [ ] Seudonimización en cliente [`D-022`]: recorte automático de la cabecera superior (primeros 3 cm) sobre el Canvas
- [ ] **`[D-034]` Herramienta de Tampón/Blackout Box:** vista previa pre-subida donde el docente puede arrastrar recuadros negros adicionales con el dedo o ratón sobre cualquier nombre desplazado al pie, lateral o centro del folio. Los píxeles se destruyen en el navegador antes del `fetch` a la nube
- [ ] Vista previa y reordenación de folios antes de confirmar
- [ ] **Selector obligatorio de `etapa` (ESO/BACH):** La interfaz bloquea el envío y exige seleccionar la etapa educativa, alineándose con el *Breaking Change* de backend (`[D-041]`) para prevenir errores HTTP 422.
- [ ] Botón de envío que transmite el array y datos a `POST /api/v1/submissions`
- [ ] Indicador de carga mientras el servidor encola la corrección asíncrona

**Etiquetas:** `v0.5` `frontend`

---

### [v0.5-003] Panel dual de corrección

**Como** profesora,  
**quiero** ver el examen del alumno junto al análisis de la IA en pantalla  
**para** revisar la corrección sin cambiar de ventana.

**Criterios de aceptación:**
- [ ] Panel izquierdo: visualizador paginado del examen (`archivos_urls`) con zoom y selector de folio
- [ ] Panel derecho: análisis IA (nota, desglose por rúbrica, análisis formativo y cualitativo)
- [ ] Las mejoras inmediatas aparecen en rojo, las de medio plazo en naranja
- [ ] Las fortalezas aparecen en verde
- [ ] En móvil: paneles apilados verticalmente (imagen arriba, análisis abajo)

**Etiquetas:** `v0.5` `frontend`

---

### [v0.5-004] Marcadores visuales sobre la imagen

**Como** profesora,  
**quiero** ver señalados directamente sobre el examen los errores detectados por la IA  
**para** entender de un vistazo qué parte del texto tiene cada problema.

**Criterios de aceptación:**
- [ ] Los `visualMarkers` del JSON se renderizan como puntos o recuadros sobre el folio correspondiente
- [ ] Al hacer hover/tap sobre un marcador, aparece el comentario del error
- [ ] Los marcadores tienen color según tipo: rojo (error), naranja (mejora), verde (correcto)
- [ ] Los marcadores son visibles en móvil con tap

**Etiquetas:** `v0.5` `frontend`

---

### [v0.5-005] Botón de aprobación Human-in-the-Loop

**Como** profesora,  
**quiero** poder aprobar, ajustar o rechazar la corrección de la IA  
**para** mantener siempre la decisión final en mis manos.

**Criterios de aceptación:**
- [ ] Botón "Aprobar corrección" llama a `PUT /api/v1/submissions/{id}/approve`
- [ ] Campo de nota editable por la profesora (sobreescribe la nota de la IA si decide ajustarla)
- [ ] Botón "Solicitar nueva corrección" reinicia el proceso de evaluación de la IA (por ejemplo, tras cambiar una rúbrica o ante una reclamación)
- [ ] El ChangeLog registra inmutabilemente cada decisión o intento de la profesora con su timestamp
- [ ] Una vez aprobada (`GRADED`), la evaluación queda bloqueada (no editable en plaza); si se solicita una re-corrección, se genera una nueva versión (`v2`) conservando el historial probatorio anterior

**Etiquetas:** `v0.5` `frontend` `backend`

---

### [v0.5-006] Evolución de Interfaz: Actor Alumno en `feed-forward/realizado` (`Student PWA`)

**Como** estudiante del centro educativo,  
**quiero** poder marcar directamente desde mi portal o PWA de alumno que he completado mi Siguiente Paso Accionable  
**para** participar en mi propia evaluación continua sin requerir que el docente actúe manualmente como proxy en su panel.

**Criterios de aceptación:**
- [ ] El endpoint `PATCH /api/v1/submissions/{id}/feed-forward/realizado` amplía sus dependencias de seguridad para admitir tanto token JWT del rol `Profesor` propietario como del rol `Alumno` (`alumno_id` vinculado a la entrega).
- [ ] Si la acción la ejecuta el propio estudiante, `ChangeLog` registra un actor específico (ej. `actor = "ALUMNO_ID_<hash>"` o `"ALUMNO"`), manteniendo la trazabilidad probatoria y separada del docente.
- [ ] El semáforo formativo en el panel PWA de la profesora se actualiza visualmente en cuanto el estudiante completa su checklist personal.

**Etiquetas:** `v0.5` `frontend` `backend` `pwa`

---

### [v0.5-007] Entorno de Pruebas de Integración con Postgres en Docker

**Como** desarrolladora y auditora de calidad,  
**quiero** disponer de una suite de pruebas de integración que ejecute `alembic upgrade head` y `pytest` sobre una base de datos PostgreSQL real aislada en Docker  
**para** verificar que todas las migraciones de esquemas y los tipos avanzados (`JSONB`) funcionan idénticamente a producción sin contaminar la base de datos de desarrollo local.

**Criterios de aceptación:**
- [ ] Configurar una fixture de pruebas en `pytest` que levante o se conecte a una BBDD/esquema aislado `api_correccion_test` en PostgreSQL 16 Alpine (Docker).
- [ ] La suite ejecuta las migraciones reales de `alembic upgrade head` antes de lanzar las pruebas de integración.
- [ ] Saldar la deuda técnica documentada en `AUDITORIA.md` (Sección 4, fila Alembic) y en `backlog.md`.
- [ ] Mantener los tests rápidos con SQLite en memoria para desarrollo local ultrarrápido (`pytest -m unit`).

**Etiquetas:** `v0.5` `testing` `docker` `alembic` `tech-debt`


---

## 🏆 Versión 1.0 — MVP Completo y Desplegado

**Objetivo:** El producto está desplegado en una URL pública, documentado y listo para ser mostrado en portfolio y al auditor externo.

---

### [v1.0-001] Despliegue del backend en Railway

**Como** desarrolladora,  
**quiero** tener el backend accesible en una URL pública  
**para** que cualquier persona pueda probar la API sin ejecutarla en local.

**Criterios de aceptación:**
- [ ] Backend desplegado en Railway con PostgreSQL y Redis incluidos
- [ ] Variables de entorno configuradas en Railway (no en el código)
- [ ] URL pública documentada en el README
- [ ] Endpoint `GET /health` devuelve `200` en producción

**Etiquetas:** `v1.0` `infra`

---

### [v1.0-002] Despliegue del frontend PWA

**Como** profesora,  
**quiero** acceder a la PWA desde cualquier dispositivo con una URL  
**para** usarla sin instalar nada.

**Criterios de aceptación:**
- [ ] Frontend desplegado en Vercel o Railway
- [ ] La PWA es instalable desde el navegador en iOS y Android mediante `manifest.json` ("Añadir a pantalla de inicio" sin pasar por tienda [D-007])
- [ ] HTTPS habilitado (requerido para acceso a cámara en móvil)
- [ ] URL pública documentada en el README

**Etiquetas:** `v1.0` `frontend` `infra`

---

### [v1.0-003] README final con Compliance

**Como** visitante del repositorio,  
**quiero** entender la arquitectura, el propósito y el cumplimiento legal del proyecto  
**para** evaluar la madurez técnica y ética de la herramienta.

**Criterios de aceptación:**
- [ ] Sección `## Arquitectura` con diagrama del sistema (texto o imagen)
- [ ] Sección `## AI Development Methodology` — uso transparente de IA en el desarrollo
- [ ] Sección `## Compliance & EU AI Act Readiness` — RGPD (seudonimización en nube y Cold Storage [D-021]), AI Act, y HitL [D-002]
- [ ] Sección `## Cómo ejecutar en local` actualizada y probada
- [ ] Capturas de pantalla del panel de corrección

**Etiquetas:** `v1.0` `docs` `legal`

---

### [v1.0-004] ChangeLog de auditoría completo

**Como** sistema bajo AI Act,  
**quiero** registrar todas las acciones relevantes de forma inmutable  
**para** poder demostrar en una auditoría que el humano tuvo siempre la última palabra.

**Criterios de aceptación:**
- [ ] Cada corrección registra: `submission_id`, `accion`, `actor` (IA / profesora), `timestamp`
- [ ] La nota de la IA y la nota final de la profesora quedan ambas registradas
- [ ] Ningún registro del ChangeLog puede modificarse ni eliminarse (append-only)
- [ ] `GET /api/v1/submissions/{id}/changelog` devuelve el historial completo

**Etiquetas:** `v1.0` `backend` `database` `legal`

---

### [v1.0-005] Aplicación a Programas de Incubación y Portfolio

**Como** desarrolladora junior y creadora del proyecto,  
**quiero** utilizar la Versión 1.0 como llave para mejorar mi empleabilidad y red de contactos  
**para** conseguir apoyo técnico, mentoría o un empleo cualificado sin poner en riesgo mi situación actual.

**Criterios de aceptación:**
- [ ] Portfolio actualizado con el enlace al repositorio y a la URL de producción
- [ ] Solicitud de asesoramiento y tutoría enviada al **Polo de Emprendemento de Galicia** en A Coruña (Xunta)
- [ ] Solicitud enviada al programa **Talento 45+** (Cámara de Comercio de A Coruña + SEPE)
- [ ] Registro completado en la plataforma **Generación SAVIA** (Fundación Endesa)
- [ ] Candidatura valorada para programas de incubación y ayudas en A Coruña (**Explorer UDC / Activa Startups / PAEM Galicia / IGAPE**)
- [ ] Reunión agendada con el contacto de la **Auditoría en A Coruña (Ciudad de las TIC)** para presentarle el sistema funcional

**Etiquetas:** `v1.0` `docs`

---

## 🔮 Roadmap — Mejoras a Futuro

### [Roadmap-001] Sincronización y Auditoría Automática de Vigencia Legislativa (DOG / BOE Tracker)
**Como** administradora del sistema,  
**quiero** que la plataforma verifique periódicamente si los decretos cargados en BBDD siguen vigentes  
**para** evitar que la IA evalúe al alumnado con criterios obsoletos o derogados de forma involuntaria.

* **Dependencias:** `[v0.2-003]` (Modelos base), `[v0.2-005]` (Changelog de auditoría), `feedparser` / `beautifulsoup4` (Scraping oficial).
* **Criterios de aceptación:**
  - Un worker en segundo plano realiza un rastreo periódico (mensual/trimestral) de los boletines oficiales buscando cambios en los decretos rectores.
  - Si detecta un cambio de versión legal, marca el marco antiguo como histórico y el nuevo como borrador pendiente de revisión.
  - Se registra el cambio de vigencia en el `changelog` con actor = "SYSTEM_UPDATE".

---

### [Roadmap-002] Escáner Local Offline de Datos Personales Pre-Nube (`Automated Offline PII Shield`)
**Como** administradora de ciberseguridad del sistema,  
**quiero** que el backend local pase la imagen por un micro-motor OCR offline en RAM antes de conectar con la nube exterior  
**para** detectar y bloquear automáticamente cualquier nombre o rastro de PII del alumnado que haya escapado al recorte manual de cabecera (`[D-034]`).

* **Dependencias:** `[v0.3-002]` (Recorte pre-nube Pillow), `pytesseract` / `presidio-image-redactor`.
* **Candidatos de motor OCR offline (a evaluar en implementación):**
  - `Tesseract` — OCR clásico LSTM, óptimo para texto impreso (cabeceras, nombres tipografiados).
  - `TrOCR` (`microsoft/trocr-base-handwritten`) — Transformer end-to-end, candidato preferido para caligrafía manuscrita escolar irregular (letra del alumno en el cuerpo del examen). Ver `glosario.md`.
* **Criterios de aceptación:**
  - Un middleware local en WSL/Docker inspecciona el buffer de la imagen en memoria antes de llamar al SDK de Cloudinary o al motor de Groq.
  - Si detecta coincidencias con nombres del listado de la clase (`PII Confidence > 0.8`), aborta la subida y devuelve error HTTP `422` alertando al docente para redacción visual en la PWA.
  - El intento bloqueado queda registrado en el `changelog` con `actor = "PII_SHIELD"` para trazabilidad AI Act.

---

### [Roadmap-003] Servidor MCP para Integración Agéntica Externa (Model Context Protocol)
**Como** arquitecta de software,  
**quiero** exponer un servidor MCP (Model Context Protocol) sobre el backend  
**para** que cualquier agente de IA externo (Claude Desktop, IDEs o asistentes de centro) pueda consultar rúbricas y ejecutar la evaluación formativa de forma estandarizada y segura.

* **Dependencias:** `[v0.2-001]` (CRUD Rúbricas SQL), `[v0.2-004]` (Motor Evaluador FastAPI), SDK `mcp` en Python.
* **Criterios de aceptación:**
  - Un servidor MCP en Python (protocolo JSON-RPC) expone las herramientas: `obtener_rubrica_oficial`, `validar_contrato_evaluacion` y `ejecutar_evaluacion_formativa`.
  - Los agentes externos interactúan con la API utilizando esquemas estrictos Pydantic sin necesidad de conectores ad-hoc.
  - Se mantiene la garantía de privacidad por diseño (*Zero Data Retention*) exigida en el sistema.

---

### [Roadmap-004] Generador de Pruebas y Exámenes Competenciales Dinámicos
**Como** docente,  
**quiero** que la API utilice el contexto normativo y las rúbricas almacenadas en la base de datos para generar modelos de examen aleatorios y competenciales  
**para** evaluar a los alumnos con escenarios prácticos donde el uso de IAs generativas por parte del estudiante no invalide la prueba.

* **Dependencias:** `[v0.2-003]` (Marcos Normativos), `[v0.2-004]` (Rúbricas Docentes).
* **Criterios de aceptación:**
  - Un nuevo endpoint `POST /api/v1/exams/generate` acepta un `marco_id` y `rubrica_id`.
  - El LLM cruza los descriptores operativos de la ley con la rúbrica y devuelve un JSON estructurado con preguntas basadas en escenarios prácticos reales (no de memorización).
* **Notas de diseño / Inspiración:**
  - Inspirado en la arquitectura multi-agente de generación de contenidos de Miguel Egea. El diseño evaluará la viabilidad de utilizar plantillas deterministas orquestadas antes de la fase de generación LLM para asegurar la consistencia curricular.

---

### [Roadmap-005] RAG Semántico con Materiales Didácticos del Docente
**Como** docente,  
**quiero** poder subir mis apuntes, fragmentos del libro de texto y criterios específicos del examen al sistema  
**para** que la IA evalúe al alumno conforme a lo que yo he impartido en el aula, y no solo conforme al conocimiento general del modelo y la normativa oficial.

* **Dependencias:** `[v0.2-004]` (Rúbricas Docentes), `[v0.3-001]` (Subida de archivos), vector store (Pinecone, Chroma o PGVector).
* **Contexto:** Limitación conocida y documentada en `[D-054]`. El RAG actual es determinista (recuperación por ID exacto), lo que garantiza consistencia normativa pero impide que el modelo sepa qué temario concreto ha dado el docente hasta la prueba.
* **Criterios de aceptación:**
  - El docente puede subir documentos (PDF, TXT) como "materiales de aula" vinculados a una asignatura y período.
  - El sistema los procesa mediante chunking + embeddings y los indexa en un vector store.
  - En cada evaluación, antes de llamar al LLM, el sistema recupera los fragmentos más relevantes a la pregunta del alumno y los inyecta como contexto adicional en el prompt.
  - Si no hay materiales cargados, el sistema evalúa en modo RAG Determinista actual con aviso en el panel docente.

---

## 🩺 Notas de Deuda Técnica Activa

- **Tests sin validación de migraciones (v0.3-002):** Tests sin validación de migraciones (v0.3-002+): Los tests unitarios utilizan SQLite en memoria llamando a metadata.create_all() en lugar de aplicar revisiones Alembic, por lo que no validan si las migraciones coinciden con los modelos reales. Esta es una limitación técnica conocida que obliga a validar las nuevas columnas (como estado_feed_forward) manualmente contra Postgres.
Ver AUDITORIA.md, sección 4, fila "Alembic (migraciones reales)" — clasificada como Parcial por este mismo motivo (evidencia indirecta, riesgo de falso "verde"). Cerrar esta deuda requiere una suite de tests de integración contra un contenedor Postgres real (no SQLite) que aplique alembic upgrade head antes de cada batería de pruebas.
- **Advertencia de Dependencias (v0.5):** Los tests arrojan un `StarletteDeprecationWarning: Using 'httpx' with 'starlette.testclient' is deprecated; install 'httpx2' instead.` que debe resolverse actualizando la dependencia del cliente HTTP de pruebas.
- **Revisión Pre-Publicación (Open Source):** Antes de cambiar la visibilidad del repositorio a público, se debe ejecutar el siguiente checklist:
  1. **Auditoría de Markdown:** Asegurar que no hay rutas locales absolutas (ej. `C:\Users\...`), comentarios sobre estrategia personal, o planes de networking en `backlog.md`, `decisiones.md`, etc. El tono debe ser estrictamente técnico.
  2. **Limpieza del repositorio:** Eliminar archivos basura, scripts temporales (scratchpads) y verificar que el `.gitignore` funciona correctamente (`__pycache__`, etc).
  3. **Seguridad de Secretos:** Revisar el historial de Git para garantizar que nunca se ha subido una API Key real en el pasado (usar BFG Repo-Cleaner si fuera necesario).
  4. **Licenciamiento:** Añadir un archivo `LICENSE` (ej. MIT License) en la raíz del proyecto.
  5. **README Onboarding:** Añadir una sección de "Getting Started" o "Instalación Local" clara para que un evaluador externo sepa cómo levantar la API en 2 minutos.

---

*Backlog generado el 07/07/2026 — Antigravity para Alba Camiña García*  
*Actualizado el 16/07/2026 — Sincronizadas transiciones formativas [D-026] e incorporadas historias de cierre v0.2 y demo HitL pre-auditoría (`[v0.2-008]`, `[v0.2-009]`, `[v0.2-010]`).*  
*Total de historias: 34 | Versiones: 6 (0.1 → 1.0) | Ítems en Roadmap: 3*  
*Actualizado el 20/07/2026 — Auditoría normativa LOMLOE (D-040–D-045): etapa obligatoria ESO/BACH, escala BE/NA, media ponderada en backend (issue #10, PR #11).*  
*Actualizado el 10/08/2026 — [Roadmap-002] añadido TrOCR como candidato alternativo a Tesseract para Capa 1 PII (caligrafía manuscrita). [D-051] registrado en decisiones.md.*
