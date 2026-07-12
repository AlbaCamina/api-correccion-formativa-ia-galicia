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
**para** que el producto pueda presentarse con total seguridad jurídica ante inspecciones educativas, la AESIA o departamentos de orientación [D-002, D-011, D-021, D-022].

**Criterios de aceptación:**
- [x] Adoptado modelo *Human-in-the-Loop* (HitL): la IA propone un borrador formativo; la profesora toma y aprueba la decisión final (`[D-002]`)
- [x] Diseñado el mecanismo de seudonimización pre-nube: el cliente (Canvas) o buffer local recorta y elimina los 3 cm superiores de cabecera con datos identificativos antes del envío al almacenamiento externo (`[D-022]`)
- [x] Almacenamiento nube en *Cold Storage* con purga automática por *Lifecycle Policy* (*Zero Data Retention* / expiración legal `[D-021]`)
- [x] Inmutabilidad probatoria (*append-only*): las correcciones aprobadas (`GRADED`) se bloquean contra edición para preservar la cadena de custodia educativa (`[v0.5-005]`)

**Etiquetas:** `v0.0` `legal` `infra` `docs`

---

### [v0.0-002] Adopción de la Normativa de Evaluación de Galicia (`Decreto 156/2022 y 157/2022`)
**Como** desarrolladora empadronada en A Coruña (Galicia),  
**quiero** que el motor de evaluación adopte el marco autonómico gallego de la Xunta de Galicia como primer `seed` de base de datos (`JSONB`)  
**para** lograr máxima coherencia con mi entorno institucional (Ciudad de las TIC, AESIA, Polos de Emprendemento) y soportar evaluación por competencias bilingüe [D-001, D-004].

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
- [x] Elaborada taxonomía técnica en 4 niveles (Medidas ordinarias DEA, ACNS no significativas, ACS significativas y ACIS altas capacidades) documentada en [marco_normativo_y_adaptaciones.md](file:///c:/Users/34636/Desktop/qia-correction/marco_normativo_y_adaptaciones.md)
- [x] Diseñada la columna `adaptaciones_alumno (JSONB)` en `submissions` (`[v0.2-005]`) para inyectar reglas de exclusión ortográfica en el prompt sin que la IA diagnostique
- [x] El contrato JSON clasifica faltas ortográficas en dislexia como marcadores neutros (`ortografia_excluida`) en gris, separándolos del cálculo de nota penalizadora

**Etiquetas:** `v0.0` `ia` `legal` `docs`

---

### [v0.0-004] Benchmarking y aval internacional: Alemania, Países Nórdicos, UK y USA
**Como** investigadora de producto,  
**quiero** contrastar la arquitectura y pedagogía de QIA-Correction contra las prácticas líderes mundiales (Datenschutz alemán, Fobizz, Finlandia/Abitti, FeedbackFruits, Gradescope, NoMoreMarking, Hattie & Timperley en UK)  
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
- [x] Identificado el contacto e itinerario para presentar el MVP funcional en el hub **Ciudad de las TIC / AESIA de A Coruña** (`[v1.0-005]`)
- [x] Planificadas las ayudas de inicio de actividad en Galicia (`Emprego Autónomo >45 años de 4.000€ a 7.000€ + Cuota Cero`), `Activa Startups Galicia (hasta 40.000€)` y `ENISA Emprendedoras Digitales` para la fase de comercialización futura

**Etiquetas:** `v0.0` `docs`

---

## 🚀 Versión 0.1 — Motor Síncrono (Prueba de concepto)

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

**Etiquetas:** `v0.1` `backend`

---

### [v0.1-001] Estructura base del proyecto FastAPI

**Como** desarrolladora,  
**quiero** tener la estructura de carpetas del proyecto configurada  
**para** poder empezar a añadir endpoints de forma ordenada.

**Criterios de aceptación:**
- [ ] Carpeta `backend/` con `main.py`, `routers/`, `models/`, `services/`
- [ ] Entorno virtual Python configurado (`venv` o `poetry`)
- [ ] FastAPI instalado y servidor arrancando en `localhost:8000`
- [ ] Endpoint de health check `GET /health` devuelve `{ "status": "ok" }`
- [ ] `.gitignore` configurado (excluye `venv/`, `.env`, `__pycache__/`)
- [ ] Repositorio Git inicializado (`git init`) y vinculado al repositorio en GitHub (`git remote add origin...`)
- [ ] Primer commit y push realizados a GitHub exclusivamente con la documentación de arquitectura y diseño (`*.md`) antes de escribir la primera línea de código
- [ ] `AGENTS.md` generado en la raíz del proyecto ejecutando `/init` en OpenCode (contexto persistente para el agente en todas las sesiones)
- [ ] Reglas de **PonyTail** añadidas al `AGENTS.md`: el agente aplica el principio de mínimo código (YAGNI + decisión ladder) para reducir tokens y sobre-ingeniería

**Etiquetas:** `v0.1` `backend` `infra`

---

### [v0.1-002] Modelo Pydantic del contrato de salida de la IA

**Como** desarrolladora,  
**quiero** definir el esquema estricto que la IA debe devolver  
**para** que el servidor rechace automáticamente respuestas malformadas.

**Criterios de aceptación:**
- [ ] Modelo `EvaluacionIA` con campos: `transcription`, `rubricBreakdown`, `visualMarkers`, `qualitativeAnalysis`
- [ ] `qualitativeAnalysis` incluye: `strengths[]`, `improvementNeeds.immediate[]`, `improvementNeeds.mediumLongTerm[]`, `teacherSummary`
- [ ] Si la IA devuelve un JSON sin algún campo obligatorio, Pydantic lanza error 422
- [ ] Test unitario que valida un JSON correcto y uno incorrecto

**Etiquetas:** `v0.1` `backend`

---

### [v0.1-003] Endpoint de corrección síncrona (texto plano)

**Como** profesor,  
**quiero** enviar el texto de una respuesta de alumno junto con una rúbrica  
**para** recibir una corrección estructurada con nota y análisis formativo.

**Criterios de aceptación:**
- [ ] `POST /api/v1/evaluate` acepta `{ "student_answer": string, "rubric": string }`
- [ ] El servidor llama a la API de OpenAI/Anthropic con un prompt estructurado
- [ ] La respuesta de la IA se valida con el modelo Pydantic de `v0.1-002`
- [ ] Si la IA devuelve JSON inválido, el servidor reintenta una vez antes de devolver error 500
- [ ] Devuelve el objeto `EvaluacionIA` completo con código 200
- [ ] Tiempo de respuesta documentado en los logs

**Etiquetas:** `v0.1` `backend`

---

### [v0.1-004] Ingeniería del prompt base

**Como** desarrolladora,  
**quiero** definir el System Prompt que instruye a la IA  
**para** que evalúe con criterios pedagógicos reales y devuelva siempre el formato correcto.

**Criterios de aceptación:**
- [ ] System prompt en archivo separado `services/prompt_builder.py`
- [ ] El prompt instruye a la IA a actuar como "evaluador formativo experto en **Filosofía de Bachillerato**, educación secundaria andaluza" (asignatura hardcoded en v0.1 — dinámica desde v0.2 vía `marco_id`)
- [ ] El prompt exige explícitamente el formato JSON del contrato
- [ ] El prompt diferencia entre mejoras inmediatas y a medio/largo plazo
- [ ] Probado con al menos 3 respuestas de alumno distintas (buena, regular, mala)

**Etiquetas:** `v0.1` `backend`

---

### [v0.1-005] Gestión de errores y códigos HTTP

**Como** consumidor de la API,  
**quiero** recibir mensajes de error claros y códigos HTTP correctos  
**para** saber exactamente qué ha fallado sin tener que leer logs del servidor.

**Criterios de aceptación:**
- [ ] `400` si el body de la petición está mal formado o faltan campos
- [ ] `422` si los datos no pasan validación de Pydantic
- [ ] `500` si la IA falla o devuelve JSON inválido tras el reintento
- [ ] Todos los errores devuelven `{ "error": string, "detail": string }`
- [ ] Los errores se registran en log con timestamp

**Etiquetas:** `v0.1` `backend`

---

### [v0.1-006] Variables de entorno y configuración

**Como** desarrolladora,  
**quiero** gestionar las claves de API y configuración mediante variables de entorno  
**para** no exponer credenciales en el repositorio.

**Criterios de aceptación:**
- [ ] Archivo `.env.example` con todas las variables necesarias (sin valores reales)
- [ ] `API_KEY_OPENAI` o `API_KEY_ANTHROPIC` cargadas desde `.env`
- [ ] El servidor no arranca si falta una variable de entorno requerida
- [ ] `.env` añadido a `.gitignore`

**Etiquetas:** `v0.1` `backend` `infra`

---

### [v0.1-007] README inicial del proyecto

**Como** visitante del repositorio en GitHub,  
**quiero** entender qué es el proyecto y cómo ejecutarlo  
**para** evaluar el trabajo o contribuir.

**Criterios de aceptación:**
- [ ] Descripción del proyecto y propuesta de valor diferencial
- [ ] Instrucciones de instalación y ejecución local
- [ ] Ejemplo de petición y respuesta del endpoint `POST /api/v1/evaluate`
- [ ] Sección `## AI Development Methodology` con los 4 elementos del marco narrativo de BLOQUE 8: qué diseñé yo / qué ejecutaron los agentes / cómo validé / qué aprendí — usando el lenguaje de arquitecta/orquestadora, no el lenguaje defensivo
- [ ] Badges de versión y estado

**Etiquetas:** `v0.1` `docs`

---

## 🗄️ Versión 0.2 — Base de Datos

**Objetivo:** La normativa andaluza y las rúbricas del profesor dejan de estar hardcoded y pasan a ser datos dinámicos almacenados en PostgreSQL.

---

### [v0.2-001] Configuración de PostgreSQL y SQLAlchemy

**Como** desarrolladora,  
**quiero** conectar la API a una base de datos PostgreSQL  
**para** poder persistir y recuperar datos de forma transaccional.

**Criterios de aceptación:**
- [ ] Docker Compose con servicio PostgreSQL levantando en `localhost:5432`
- [ ] SQLAlchemy configurado con connection pool
- [ ] Alembic configurado para migraciones
- [ ] Primera migración vacía ejecutada correctamente

**Etiquetas:** `v0.2` `database` `infra`

---

### [v0.2-002] Modelo de datos: Profesor y autenticación básica

**Como** profesora,  
**quiero** tener una cuenta en el sistema  
**para** que mis rúbricas y correcciones sean privadas.

**Criterios de aceptación:**
- [ ] Tabla `profesores` con campos: `id`, `email`, `nombre`, `created_at`
- [ ] `POST /api/v1/auth/register` crea un profesor
- [ ] `POST /api/v1/auth/login` devuelve JWT
- [ ] Rutas protegidas requieren JWT válido en header `Authorization`

**Etiquetas:** `v0.2` `backend` `database`

---

### [v0.2-003] Modelo de datos: Marco de Evaluación (normativa como variable)

**Como** desarrolladora,  
**quiero** almacenar la normativa gallega (Xunta/LOMLOE) como un registro en base de datos  
**para** que cambios legislativos solo requieran actualizar un registro (no el código), y para que el sistema pueda escalar a otras comunidades autónomas sin modificar la arquitectura.

**Criterios de aceptación:**
- [ ] Tabla `marcos_evaluacion` con campos: `id`, `nombre`, `asignatura`, `curso`, `estado_activo`, `rubrica_completa` (JSONB)
- [ ] Seed con al menos un marco de evaluación real de Bachillerato o ESO (Decreto autonómico de la Xunta de Galicia)
- [ ] `GET /api/v1/marcos` devuelve todos los marcos activos
- [ ] El endpoint de evaluación acepta `marco_id` para usar el marco correspondiente

**Etiquetas:** `v0.2` `backend` `database`

---

### [v0.2-004] Modelo de datos: Rúbrica del docente

**Como** profesora,  
**quiero** crear y guardar mis propias rúbricas de corrección  
**para** que interactúen con la normativa oficial al evaluar.

> [!NOTE]
> **Decisión pendiente antes de implementar esta historia:** ¿cómo interactúan la rúbrica del docente y el marco normativo en el prompt? Dos opciones a evaluar cuando llegue v0.2:
> - **Opción A — Combinación:** rúbrica y normativa se fusionan en el prompt como criterios complementarios.
> - **Opción B — Coherencia:** la IA usa la rúbrica del docente y verifica que sea coherente con la normativa, señalando contradicciones.
>
> Registrar la decisión en `decisiones.md` antes de escribir código.

**Criterios de aceptación:**
- [ ] Tabla `rubricas_docente` con campos: `id`, `profesor_id`, `nombre`, `criterios` (JSONB), `created_at`
- [ ] CRUD completo: `POST`, `GET`, `PUT`, `DELETE /api/v1/rubricas`
- [ ] Una rúbrica solo puede ser editada por su propietario
- [ ] Validación con Pydantic de la estructura de `criterios`

**Etiquetas:** `v0.2` `backend` `database`

---

### [v0.2-005] Modelo de datos: Submission con campo alumno_id

**Como** desarrolladora,  
**quiero** preparar la tabla de entregas desde el principio con el campo `alumno_id`  
**para** mantener el anonimato del estudiante en la nube mediante seudonimización y que la profesora pueda cruzar después ese identificador con su lista local de clase sin exponer datos personales (cumplimiento RGPD).

**Criterios de aceptación:**
- [ ] Tabla `submissions` con campos: `id`, `profesor_id`, `marco_id`, `rubrica_id`, `alumno_id` (nullable, anonimizado), `adaptaciones_alumno` (JSONB, nullable) [D-023], `estado` (PENDING/ANALYZING/REVIEW/GRADED), `created_at`, `updated_at`
- [ ] Tabla `evaluaciones` con campos: `id`, `submission_id`, `resultado_ia` (JSONB), `nota_final`, `aprobado_por_profesor`, `created_at`
- [ ] Tabla `changelog` con campos: `id`, `submission_id`, `accion`, `actor`, `datos_anteriores` (JSONB), `datos_nuevos` (JSONB), `timestamp`

**Etiquetas:** `v0.2` `database`

---

### [v0.2-006] Endpoint de evaluación actualizado con BBDD

**Como** profesor,  
**quiero** que la corrección use mi rúbrica y el marco normativo seleccionado  
**para** que la evaluación sea coherente con la legislación y mis criterios propios.

**Criterios de aceptación:**
- [ ] `POST /api/v1/evaluate` ahora acepta `marco_id` y `rubrica_id`
- [ ] El sistema recupera ambos de la BBDD y los inyecta en el prompt según la estrategia arquitectónica elegida en v0.2-004 (Combinación vs. Coherencia)
- [ ] El resultado se guarda en `submissions` y `evaluaciones`
- [ ] El changelog registra la corrección con `actor = "IA"`

**Etiquetas:** `v0.2` `backend` `database`

---

### [v0.2-007] Adaptaciones curriculares para alumnado NEAE/NEE (`JSONB`)

**Como** profesora,  
**quiero** configurar adaptaciones curriculares en el perfil de mi alumno (ej. dislexia, TDAH, TEA)  
**para** que el sistema detecte y reporte los errores lingüísticos u ortográficos, pero los excluya automáticamente de la penalización en la nota del examen [D-023].

**Criterios de aceptación:**
- [ ] La tabla `submissions` incluye la columna `adaptaciones_alumno (JSONB, nullable)` con estructura: `{"tipo": ["dislexia"], "excluir_ortografia": true, "tiempo_extra_pct": 35}`
- [ ] `POST /api/v1/evaluate` extrae las adaptaciones de la entrega y condicionalmente añade al prompt del LLM instrucciones precisas para separar faltas ortográficas del cálculo penalizador de nota
- [ ] El contrato JSON devuelto por el LLM incorpora los campos `ortografia_detectada` y `errores_excluidos_por_adaptacion`
- [ ] Los marcadores visuales sobre la imagen correspondientes a errores ortográficos excluidos por adaptación se clasifican como neutros (`tipo: "ortografia_excluida"`) para mostrarse en gris/neutro y no en rojo en la PWA
- [ ] Protección de privacidad (LOPDGDD art.7): la IA jamás infiere o diagnostica NEAE; solo ejecuta la instrucción recibida y solo el profesor asignado puede acceder a dicha configuración

**Etiquetas:** `v0.2` `backend` `ia` `compliance`

---

## 📸 Versión 0.3 — Subida de Imágenes y OCR

**Objetivo:** El profesor puede subir una foto del examen manuscrito. El sistema la procesa con un modelo multimodal y devuelve el análisis.

---

### [v0.3-001] Endpoint de subida de archivo (multipart)

**Como** profesora,  
**quiero** subir una foto del examen desde mi dispositivo  
**para** que el sistema la procese sin necesidad de transcribir el texto manualmente.

**Criterios de aceptación:**
- [ ] `POST /api/v1/submissions/upload` acepta `multipart/form-data` con imagen (JPG, PNG, HEIC) o PDF
- [ ] Tamaño máximo en backend: 25 MB (tolerancia para fotos puras o PDFs escaneados de múltiples páginas sin dar error al usuario)
- [ ] Nota de arquitectura [D-020]: aunque el servidor acepte hasta 25 MB, la PWA en `v0.5-002` comprimirá y redimensionará localmente el archivo antes de enviarlo para optimizar red y tokens.
- [ ] Formatos rechazados devuelven 400 con mensaje claro
- [ ] El archivo se guarda en carpeta local `/uploads` (simulando S3) con nombre UUID

**Etiquetas:** `v0.3` `backend`

---

### [v0.3-002] Almacenamiento en Cloudinary

**Como** desarrolladora,  
**quiero** almacenar las imágenes en Cloudinary  
**para** no saturar el servidor con archivos pesados y tener URLs públicas estables.

**Criterios de aceptación:**
- [ ] Credenciales de Cloudinary en `.env`
- [ ] El archivo (o múltiples imágenes) se sube a Cloudinary y se reciben la URL o lista de URLs
- [ ] La lista de URLs se guarda en la tabla `submissions` en el campo `archivos_urls` (JSONB o Array para soportar múltiples folios/PDF)
- [ ] Los archivos temporales del backend se eliminan tras subir a la nube, donde el histórico permanece resguardado ante reclamaciones bajo política de Cold Storage y retención legal [D-021]

**Etiquetas:** `v0.3` `backend` `infra`

---

### [v0.3-003] Integración con modelo multimodal (visión)

**Como** profesora,  
**quiero** que el sistema lea el examen manuscrito automáticamente  
**para** no tener que transcribirlo yo.

**Criterios de aceptación:**
- [ ] El sistema recupera el array `archivos_urls` y envía la imagen (o lista ordenada de URLs si son varios folios/páginas) a GPT-4o Vision o Claude con el prompt de evaluación
- [ ] El modelo devuelve el JSON estructurado incluyendo `transcription` (texto extraído)
- [ ] Si la caligrafía es ilegible, el campo `transcription` incluye `[ILEGIBLE]` con coordenadas aproximadas
- [ ] El resultado completo se guarda en `evaluaciones.resultado_ia`

**Etiquetas:** `v0.3` `backend`

---

### [v0.3-004] Anonimización básica de imagen

**Como** desarrolladora (y como cumplimiento RGPD),  
**quiero** que los nombres del alumno en la cabecera del examen no se envíen a la IA  
**para** cumplir con la normativa de protección de datos de menores.

**Criterios de aceptación:**
- [ ] El sistema recorta o difumina la cabecera del folio (primeros 3 cm) en memoria local antes de subir el archivo a la nube
- [ ] La imagen ya anonimizada es la única que se sube a Cloudinary/S3 y la que se envía a la IA
- [ ] El archivo temporal original con el nombre del alumno se purga de inmediato y nunca se almacena en la nube (cumplimiento total RGPD/Regla 9)
- [ ] El campo `alumno_id` se asigna manualmente por el profesor (ej. número de lista)

**Etiquetas:** `v0.3` `backend` `legal`

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
- [ ] `POST /api/v1/submissions` acepta `archivos_urls`, `marco_id`, `rubrica_id` y `alumno_id` devolviendo `{ "submission_id": "...", "status": "PENDING" }` (`202 Accepted`) en <500ms
- [ ] La tarea de corrección multimodal se encola en Celery y no bloquea al servidor
- [ ] `GET /api/v1/submissions/{id}` devuelve el estado actual (PENDING/ANALYZING/REVIEW/GRADED)
- [ ] El worker actualiza el estado y guarda las evaluaciones en BBDD al terminar

**Etiquetas:** `v0.4` `backend`

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
- [ ] Seudonimización en cliente [D-022]: recorte o difuminado automático de la cabecera superior (primeros 3 cm) sobre el Canvas
- [ ] Vista previa y reordenación de folios antes de confirmar
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

## 🏆 Versión 1.0 — MVP Completo y Desplegado

**Objetivo:** El producto está desplegado en una URL pública, documentado y listo para ser mostrado en portfolio y al contacto de la AESIA.

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
- [ ] Reunión agendada con el contacto de la **AESIA en A Coruña (Ciudad de las TIC)** para presentarle el sistema funcional

**Etiquetas:** `v1.0` `docs`

---

*Backlog generado el 07/07/2026 — Antigravity para Alba Camiña García*  
*Actualizado el 09/07/2026 — sincronizadas reglas de trabajo, seudonimización legal [D-022], compresión en cliente [D-020] y Cold Storage [D-021]*  
*Total de historias: 29 | Versiones: 6 (0.1 → 1.0)*
