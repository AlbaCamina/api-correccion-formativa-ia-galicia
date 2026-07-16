# 📖 Glosario — API de Corrección Formativa con IA (`api-correccion-formativa-ia-galicia`)
**Proyecto:** API de Corrección Formativa con IA (`api-correccion-formativa-ia-galicia`)  
**Responsable:** Alba Camiña García  
**Inicio:** Julio 2026

> [!NOTE]
> Documento vivo. Cada vez que aparezca un término nuevo en el proyecto, se añade aquí con su explicación. Los términos están organizados por categoría y ordenados alfabéticamente dentro de cada una.

---

## 1. Conceptos generales de desarrollo web

**API** (Application Programming Interface — Interfaz de Programación de Aplicaciones)  
Canal estandarizado por el que dos programas se comunican. En este proyecto, la API es el backend de FastAPI: recibe peticiones (exámenes) y devuelve respuestas (correcciones JSON).

**Backend**  
La parte del sistema que no ve el usuario. Procesa los datos, llama a la IA, guarda en la base de datos. En este proyecto: Python + FastAPI corriendo en el servidor.

**Boilerplate**  
Código repetitivo y estructural que hay que escribir en casi todo proyecto aunque no hace nada específico del negocio (imports, configuración inicial, estructura de carpetas). Los agentes de IA lo generan bien.

**CORS** (Cross-Origin Resource Sharing — Intercambio de Recursos de Origen Cruzado)  
Mecanismo de seguridad de los navegadores web que restringe las peticiones HTTP realizadas desde un dominio o puerto (ej. `http://localhost:5173` en Vite) hacia otro diferente (`http://127.0.0.1:8000` en FastAPI). Por especificación oficial, cuando se permite el envío de credenciales o tokens Bearer (`allow_credentials=True`), está prohibido usar un comodín (`allow_origins=["*"]`) por riesgo de seguridad; se exige declarar explícitamente los orígenes confiables.

**Debug / Debugging**  
Proceso de encontrar y corregir errores en el código. Literalmente "quitar los bichos".

**Deploy / Despliegue**  
Publicar el código en un servidor accesible desde internet. Antes solo funciona en tu máquina local; tras el deploy, cualquiera puede usarlo.

**Deprecado / Deprecation (`Deprecated`)**  
Estado o cualidad de un método, función o tecnología que sigue funcionando temporalmente por motivos de compatibilidad con código antiguo, pero cuyo uso oficial ha sido desaconsejado o declarado obsoleto por sus creadores (generalmente porque existe una alternativa superior, más segura o moderna, o porque será eliminado definitivamente en una futura versión). En este proyecto: el reemplazo de `datetime.utcnow()` (deprecado en Python 3.12+ por no incluir zona horaria explícita) por `datetime.now(timezone.utc)` y callables `utcnow()` para evitar advertencias (`DeprecationWarning`) de SQLAlchemy/Pytest y garantizar timestamps precisos en UTC sin riesgo de ruptura en futuras actualizaciones del lenguaje.

**Endpoint**  
Una URL concreta de la API a la que se puede hacer una petición HTTP con un verbo específico. Cada endpoint tiene una responsabilidad única y bien definida. Los verbos más usados en este proyecto son:
- `POST` — crea o procesa algo nuevo (subir examen, registrar profesor, evaluar)
- `GET` — consulta o recupera datos sin modificar nada (ver historial, listar rúbricas)
- `PATCH` — modifica parcialmente un recurso existente (aprobar una evaluación con `actor=PROFESOR`)
- `PUT` — reemplaza un recurso completo (editar una rúbrica)
- `DELETE` — elimina un recurso

**Endpoints públicos vs. protegidos por JWT:**
- **Públicos** (no requieren token): `POST /api/v1/auth/register`, `POST /api/v1/auth/login`, `GET /health`
- **Protegidos** (requieren `Authorization: Bearer <token>` en la cabecera): todos los demás — el servidor verifica la identidad del docente antes de procesar la petición

**Endpoints reales de api-correccion-formativa-ia-galicia (por versión):**

| Versión | Endpoint | Verbo | Función |
|---|---|---|---|
| v0.1 | `/api/v1/evaluate` | `POST` | Corrección síncrona con texto plano |
| v0.2 | `/api/v1/auth/register` | `POST` | Registro de profesora |
| v0.2 | `/api/v1/auth/login` | `POST` | Login → devuelve JWT |
| v0.2 | `/api/v1/rubricas` | `POST/GET` | Crear y listar rúbricas |
| v0.2 | `/api/v1/evaluate` | `POST` | Corrección con BBDD + marco normativo |
| v0.3 | `/api/v1/submissions/upload` | `POST` | Subida de imagen/PDF del examen |
| v0.3 | `/api/v1/evaluaciones/{id}/approve` | `PATCH` | Aprobación HitL docente (`REVIEW → GRADED`) |
| v0.4 | `/api/v1/submissions` | `GET` | Lista paginada de entregas del docente |
| v0.4 | `/api/v1/submissions/{id}/events` | `GET` (SSE) | Stream de estado en tiempo real |
| v1.0 | `/api/v1/submissions/{id}/changelog` | `GET` | Historial inmutable de auditoría AI Act |

**Frontend**  
La parte del sistema que ve el usuario: botones, pantallas, formularios. En este proyecto: React + Vite (se implementa en v0.5).

**Full-stack**  
Desarrolladora que trabaja tanto en frontend como en backend. Es el perfil de este proyecto.

**Health check**  
Endpoint mínimo (`GET /health`) que devuelve `{ "status": "ok" }` para comprobar que el servidor está vivo. Es lo primero que se crea.

**HTTP** (HyperText Transfer Protocol — Protocolo de Transferencia de Hipertexto)  
El protocolo que usa internet para enviar y recibir datos. Define los códigos de respuesta:
- `200 OK` — todo bien
- `202 Accepted` — recibido, procesando
- `400 Bad Request` — la petición está mal formada
- `422 Unprocessable Entity` — los datos no pasan validación Pydantic
- `500 Internal Server Error` — algo falló en el servidor

**HTTPS** (HyperText Transfer Protocol Secure — Protocolo HTTP Seguro)  
Versión segura y cifrada de HTTP (el candado en el navegador). Es un requisito estricto en dispositivos móviles para permitir instalar una PWA y para autorizar el acceso a la cámara o micrófono.

**JSON** (JavaScript Object Notation — Notación de Objetos de JavaScript)  
Formato estándar para intercambiar datos entre sistemas. Parece un diccionario de Python con llaves y valores. Es el formato que devuelve la IA con la corrección del examen.

**Librería / Framework (Biblioteca de código)**  
Una **librería** es un conjunto de código ya escrito y empaquetado que resuelve un problema concreto y que puedes reutilizar en tu proyecto sin escribirlo desde cero. Un **framework** es similar, pero con una diferencia clave: la librería tú la llamas cuando quieres; el framework llama a tu código según sus propias reglas (él manda la estructura).

Librerías y frameworks clave de api-correccion-formativa-ia-galicia:

| Librería / Framework | Tipo | Para qué sirve |
|---|---|---|
| `fastapi` | Framework | Construye todos los endpoints REST del backend |
| `pydantic` | Librería | Valida que el JSON de la IA tenga exactamente los campos correctos |
| `sqlalchemy` | Librería | Habla con PostgreSQL escribiendo Python en vez de SQL crudo |
| `alembic` | Librería | Gestiona cambios de estructura de BBDD con control de versiones |
| `passlib[bcrypt]` | Librería | Hashea contraseñas de profesoras de forma irreversible |
| `pyjwt` | Librería | Genera y verifica tokens Bearer JWT de autenticación |
| `pillow` | Librería | Recorta la cabecera del examen (nombre del alumno) en memoria pre-nube |
| `python-dotenv` | Librería | Carga variables de entorno del archivo `.env` |
| `pytesseract` | Librería | *(Roadmap v0.8)* OCR offline para el escáner de PII pre-nube (`[D-034]`) |
| `react` | Framework | Construye la interfaz de usuario de la PWA del docente |

**Nativo / Integración Nativa (`Native / Built-in`)**  
Capacidad o funcionalidad que viene incorporada de fábrica en el núcleo de una herramienta o tecnología, sin necesidad de instalar librerías de terceros, añadir capas intermedias o usar parches artesanales. En nuestra arquitectura priorizamos soluciones nativas para mantener un código limpio, rápido y con mínimas dependencias (`YAGNI`): por ejemplo, la validación gramatical nativa de `Structured Outputs` con `.parse()` en OpenAI, la generación de documentación Swagger en `/docs` nativa de FastAPI, y la gestión del pool de conexiones nativo en SQLAlchemy.

**Parseo / Parsear (`Parsing` / `.parse()`)**  
Proceso informático de analizar, desgranar y convertir una cadena de datos en bruto (como un texto plano o una respuesta JSON por red) en una estructura de datos tipada, navegable y comprensible para el lenguaje de programación (como un objeto o instancia Pydantic en Python). En nuestro backend, cuando el modelo de IA responde con un string, el método `.parse()` o `model_validate_json` *parsea* ese texto, verificando rigurosamente campo por campo y tipo por tipo que el contrato `EvaluacionIA` se cumpla al 100% antes de procesar la nota en base de datos.

**PEP 8 (`Python Enhancement Proposal 8`)**  
Guía de estilo oficial para la escritura de código en el lenguaje Python. Define normas ampliamente aceptadas de legibilidad, organización y formato, como la agrupación de importaciones en bloques (librería estándar, paquetes de terceros y módulos locales separados por líneas en blanco), el uso de dos líneas en blanco antes de funciones y clases de nivel superior, la indentación de 4 espacios y convenciones de nombres como `snake_case` para funciones/variables y `PascalCase` para clases y modelos. En este proyecto, la aplicación sistemática de PEP 8 refuerza la modularidad plana y el tipado estricto, manteniendo un backend claro, mantenible y alineado con los estándares profesionales de la comunidad Python. En particular, se ha reforzado la agrupación correcta de importaciones y el espaciado vertical en archivos como `submission.py`.

**Pipeline** (Cadena de Procesamiento o Tubería de Datos)  
Secuencia ordenada y automatizada de pasos donde la salida (*output*) de un proceso se convierte directamente en la entrada (*input*) del siguiente paso, similar a una cadena de montaje industrial. En api-correccion-formativa-ia-galicia se analiza en la Versión 0.3 (`sesion_03_ocr_vs_multimodal_vision.md`) comparando un *Pipeline en 2 pasos* (Foto $\rightarrow$ OCR $\rightarrow$ LLM $\rightarrow$ JSON) frente a un *Pipeline Unificado Multimodal en 1 paso* (Foto $\rightarrow$ Vision LLM $\rightarrow$ JSON con marcadores espaciales x,y).

**Scaffolding** (Andamiaje o Estructura Inicial de Código)  
Generación automática o manual del esqueleto básico de un proyecto antes de empezar a escribir la lógica interna de negocio. Consiste en crear la jerarquía de carpetas principales, archivos de configuración (como `package.json`, `.env.example`, `main.py` o `docker-compose.yml`) y plantillas estructurales vacías. Proporciona los cimientos ordenados sobre los que evoluciona el código.

**Stateless vs. Stateful** (Sin Estado vs. con Estado / Transaccional)  
Un sistema es **Stateless** cuando el servidor no conserva memoria ni registro de las peticiones previas (como nuestra API v0.1: evaluaba un texto y olvidaba al usuario instantáneamente). Un sistema es **Stateful o Transaccional** cuando mantiene un estado coherente y persistente en el tiempo (como nuestra API v0.2: autentica al docente con JWT, verifica la propiedad de la rúbrica en base de datos, almacena la entrega en la tabla `Submission` y audita cada acción en un `ChangeLog` inmutable).

**Refactor**  
Reescribir código para que sea más limpio o eficiente sin cambiar lo que hace. Como reordenar una habitación sin tirar nada.

**README**  
Archivo de texto en la raíz del repositorio que explica qué es el proyecto, cómo instalarlo y cómo usarlo. Es lo primero que ve cualquier persona que visita el repositorio en GitHub.

**REST / Arquitectura REST (`RESTful`)**  
Estilo arquitectónico que define cómo deben comunicarse los sistemas en internet mediante HTTP. No es un protocolo ni una librería — es un conjunto de principios de diseño que, si se cumplen, la API se denomina "RESTful". Los principios clave que aplica api-correccion-formativa-ia-galicia son:
- **Cliente-Servidor:** React (PWA) y FastAPI son independientes y se comunican solo por HTTP.
- **Sin estado (`Stateless`):** Cada petición lleva toda la información necesaria en la cabecera JWT — el servidor no recuerda sesiones entre peticiones.
- **Interfaz Uniforme:** Las URLs nombran *recursos* y los verbos HTTP nombran *acciones* (`POST /rubricas` crea, `GET /rubricas` lista, `DELETE /rubricas/{id}` elimina). Una API no REST pondría el verbo en la URL: `POST /deleteRubrica`.
- **Sistema en Capas:** El docente llama a FastAPI; FastAPI llama a Groq y PostgreSQL internamente sin que la PWA lo sepa.
- **Recursos Identificables:** Cada entidad tiene su propia URL única (`/api/v1/evaluaciones/f47ac10b` identifica una sola evaluación).

**Stack tecnológico**  
El conjunto de tecnologías que usa un proyecto. En api-correccion-formativa-ia-galicia: Python + FastAPI + PostgreSQL + React + Vite + Redis + Celery.

**Swagger / OpenAPI**  
Estándar para describir y documentar APIs REST. FastAPI lo integra nativamente: al arrancar el servidor, genera automáticamente una interfaz web interactiva en la ruta `/docs` que permite probar todos los endpoints desde el navegador sin escribir código ni instalar herramientas.

---

## 2. Python y backend

**Alembic**  
Herramienta oficial de migraciones transaccionales para SQLAlchemy. Funciona como un "Git para la estructura de tu base de datos": en lugar de crear o modificar tablas a mano con comandos SQL sueltos (lo que causaría caos entre entornos), Alembic genera archivos de revisión temporales en Python (`alembic revision -m "nombre"`) dentro de `alembic/versions/` que describen exactamente cómo subir (`upgrade`) o retroceder (`downgrade`) el esquema. Al ejecutar `alembic upgrade head`, el motor aplica las revisiones en orden estricto, garantizando que la estructura de la base de datos sea siempre auditable, reproducible y 100% idéntica entre tu WSL local, tu Docker y el servidor de producción (`[D-030]`).


**FastAPI**  
El framework de Python con el que se construye toda la API REST de este proyecto. Su característica más importante es el uso de **decoradores** — instrucciones que se ponen encima de una función para que FastAPI sepa que esa función es un endpoint:

```python
@router.post("/evaluate")          # ← decorador: "este POST /evaluate llama a esta función"
async def evaluate(                # ← función asíncrona (no bloquea el servidor)
    body: EvaluarRequest,          # ← Pydantic valida el cuerpo automáticamente
    db: Session = Depends(get_db), # ← inyección de dependencias: FastAPI da la BBDD
    profesor = Depends(get_current_profesor) # ← FastAPI verifica el JWT
):
    ...
```

Ventajas clave sobre Django o Flask: tipado nativo con Pydantic, async/await nativo, y generación automática de Swagger UI en `/docs` sin configuración adicional.

**Event Loop & Corrutina (`async / await`)**  
El **Event Loop** (Bucle de Eventos de `asyncio`) es el motor que permite al servidor Uvicorn gestionar cientos de peticiones concurrentes en un solo hilo de procesador. Una **Corrutina** (`async def`) cede el control al bucle cuando encuentra una operación de entrada/salida precedida por `await` (como una llamada HTTP a Groq o consulta a base de datos), permitiendo que el servidor atienda a otros profesores mientras la red responde (`I/O-Bound`). Si se usa código síncrono bloqueante como `time.sleep()`, todo el bucle se paraliza.

**Inyección de Dependencias** (`Dependency Injection` — `Depends()`)  
Patrón de diseño central en FastAPI por el cual una función o endpoint no instancia ni busca directamente sus recursos externos (como una conexión a base de datos `get_db` o la validación de un usuario `get_current_profesor`), sino que el framework se los suministra automáticamente en la firma de la función. Este desacoplamiento permite inyectar dependencias simuladas o transaccionales en memoria (`sqlite:///:memory:`) durante los tests (`dependency_overrides`) sin modificar el código de producción.

**Pydantic**  
Librería de Python que valida datos automáticamente. Defines cómo debe ser un objeto (campos, tipos) y Pydantic rechaza cualquier dato que no encaje. En este proyecto actúa como guardián del JSON que devuelve la IA.

**Poetry**  
Gestor de dependencias para Python. Alternativa más moderna a `pip`. Gestiona qué librerías necesita el proyecto y en qué versión.

**SQLAlchemy**  
ORM (Object-Relational Mapper — Traductor entre objetos de código y tablas de base de datos) para Python. Equivalente a Prisma en el ecosistema Node.js. Permite trabajar con la base de datos escribiendo Python en lugar de SQL puro.

**Uvicorn**  
El servidor que ejecuta FastAPI. Cuando escribes `uvicorn main:app` en la terminal, estás arrancando el servidor local. Es rápido y compatible con operaciones asíncronas.

**venv** (virtual environment — entorno virtual)  
Un espacio aislado de Python donde se instalan las dependencias del proyecto sin afectar al resto del sistema. Cada proyecto tiene el suyo. Se activa con `source venv/bin/activate` en WSL.

---

## 3. Base de datos

**Append-only**  
Registro al que solo se pueden añadir entradas, nunca modificar ni borrar las existentes. El ChangeLog de auditoría es append-only para que no se pueda alterar el historial.

**ChangeLog**  
Tabla de auditoría que registra todas las acciones importantes del sistema con timestamp: quién hizo qué y cuándo. Requerido por el AI Act para demostrar que el humano tuvo siempre la última palabra.

**Connection pool**  
Conjunto de conexiones abiertas a la base de datos que se mantienen activas y se reutilizan entre peticiones en lugar de abrir y cerrar una conexión física con cada endpoint. En api-correccion-formativa-ia-galicia se implementa nativamente en `backend/models/database.py` (`pool_size=10, max_overflow=20`), evitando saturar PostgreSQL y garantizando latencias mínimas en concurrencia (`[D-030]`).


**CRUD** (Create, Read, Update, Delete — Crear, Leer, Actualizar, Eliminar)  
Las cuatro operaciones básicas sobre cualquier dato. Decir "CRUD completo" significa que se pueden hacer las cuatro.

**JSONB**  
Tipo de campo especial de PostgreSQL que guarda JSON de forma comprimida y permite hacer búsquedas dentro del JSON. Se usa para la normativa educativa gallega (campo flexible que puede cambiar sin alterar la estructura de la tabla).

**Migración**  
Cambio controlado en la estructura de la base de datos (añadir una tabla, un campo, cambiar un tipo). Alembic las gestiona y guarda el historial.

**ORM** (Object-Relational Mapper — Traductor entre objetos y tablas)  
Herramienta que permite trabajar con la base de datos usando objetos del lenguaje de programación en lugar de SQL puro. SQLAlchemy es el ORM de este proyecto.

**PostgreSQL**  
Base de datos relacional de código abierto. Guarda los datos estructurados del proyecto (profesores, exámenes, evaluaciones). La misma que usaste en QUANTIA.

**Puerto Dedicado / Mapeo de Puertos (Port Mapping)**  
Asignación de un puerto externo exclusivo y reservado en `docker-compose.yml` (ej. `ports: - "5433:5432"`) para aislar el contenedor de base de datos del proyecto frente a otras instancias o servicios locales del sistema operativo. Aunque internamente PostgreSQL sigue operando en su puerto nativo 5432, desde Windows o WSL nos conectamos al puerto 5433 (`DATABASE_URL`). Esto previene colisiones (`Bind for 0.0.0.0:5432 failed`) cuando conviven varios proyectos o prácticas profesionales en el mismo ordenador (`[D-030]`).

**Seed**  
Datos iniciales que se insertan en la base de datos al crearla para que no esté vacía. En este proyecto: al menos un marco de evaluación de Bachillerato o ESO según el decreto autonómico de la Xunta de Galicia.

**UUID** (Universally Unique Identifier — Identificador Único Universal)  
Un código alfanumérico generado automáticamente que identifica un registro de forma única en todo el sistema. Ejemplo: `a3f8c2d1-4b5e-...`. Se usa como ID de submissions para evitar IDs secuenciales predecibles.

---

## 4. Inteligencia Artificial

**Claude**  
Modelo de lenguaje de la empresa Anthropic. Alternativa a GPT-4o. Se considera especialmente bueno para tareas de razonamiento y escritura estructurada.

**Confidence Score** (Índice de Confianza IA)  
Medida numérica devuelta por el modelo (`0.0` a `1.0`) que indica la certeza o fiabilidad de la interpretación y lectura de un examen. En api-correccion-formativa-ia-galicia (`[D-024]`), si la confianza es `< 0.75` (caligrafía confusa, borrones), el sistema emite una alerta visual para que la profesora revise con especial atención prioritaria.

**Contrato JSON (`[D-024]` / `EvaluacionIA`)**  
Acuerdo estricto de estructura y tipado definido con Pydantic v2 que transforma a los motores de Inteligencia Artificial (por naturaleza generadores probabilísticos de texto libre) en componentes deterministas de software. Al exigir la validación estricta (`Structured Outputs` / `.parse()`), se prohíbe al LLM emitir saludos, texto libre o formatos alucinados, garantizando que el backend reciba invariablemente campos tipados (calificaciones, marcadores x-y, desglose de rúbricas y `confidence_score`) listos para persistirse en PostgreSQL y mostrarse en la PWA del profesor.

**Generador Asistido de Rúbricas (Copiloto Pre-Corrección)**  
Funcionalidad de asistencia de api-correccion-formativa-ia-galicia (`Capa 4` relacional) por la que el docente solo necesita subir o describir el enunciado de una prueba o tarea evaluable. El motor LLM cruza automáticamente la normativa general (`Capa 1`), la programación del departamento (`Capa 2`) y el acuerdo transversal del centro (`Capa 3`) para generar una propuesta de rúbrica en 4 niveles de logro (*Insuficiente, Suficiente/Bien, Notable y Sobresaliente*). El profesor la valida con un clic en su PWA, reduciendo un 90% del tiempo burocrático de diseño de baremos.

**GPT-4o** / **GPT-4o Vision**  
Modelo de lenguaje de OpenAI. La variante Vision acepta imágenes además de texto, lo que permite enviarle la foto del examen para que lo lea y evalúe.

**Jerarquía Normativa en 5 Capas Relacionales (`JSONB`)**  
Modelo arquitectónico multinivel de api-correccion-formativa-ia-galicia que desacopla y combina sin ambigüedad la legislación pública (`Capa 1: Decreto Xunta`), la programación anual del departamento (`Capa 2: Saberes y Criterios`), las normas comunes del colegio (`Capa 3: PEC/CCP`), la rúbrica de la prueba asistida (`Capa 4: El Profesor`) y las adaptaciones individuales de equidad (`Capa 5: NEAE/NEE en JSONB`).

**LLM** (Large Language Model — Modelo de Lenguaje Grande)  
Modelo de inteligencia artificial entrenado con enormes cantidades de texto. Es la IA que corrige los exámenes en este proyecto (GPT-4o o Claude).

**Modo Dual de Rúbrica (`COMBINADO` vs `AUDITORIA_CURRICULAR`)**  
Parámetro arquitectónico de interacción pedagógica (`[D-027]`, `modo_evaluacion`) que resuelve la tensión entre los criterios oficiales de la Xunta y las rúbricas ad-hoc de los docentes sin sobreingeniería en el backend. En modo `COMBINADO`, la IA fusiona los saberes de la ley con la rúbrica de la profesora para calificar entregas diarias con agilidad. En modo `AUDITORIA_CURRICULAR`, la IA corrige la tarea y adicionalmente orienta al docente contrastando su rúbrica contra los Decretos 156/157/2022, advirtiendo en `teacherSummary` de posibles omisiones competenciales.

**Multimodal / Omni-canal**  
Un modelo de IA que procesa texto, imagen y estructuras combinadas de forma simultánea (ej. GPT-4o o Claude 3.5 Sonnet). En api-correccion-formativa-ia-galicia esto permite evaluar **cualquier tipo de prueba evaluable**: no solo fotos de exámenes manuscritos, sino murales de cartulina de aula, redacciones en campos de texto online (`Form Text`) y PDFs o capturas de presentaciones hechas a ordenador (como *Canva* o *Google Slides*).

**OCR** (Optical Character Recognition — Reconocimiento Óptico de Caracteres)  
Tecnología integrada en la IA multimodal que extrae y convierte la caligrafía manuscrita de la foto del examen o el texto gráfico de un mural/cartulina en datos legibles para evaluarlos contra la rúbrica.

**Prueba evaluable (Instrumento de evaluación)**  
Cualquier evidencia de aprendizaje del alumno sometida a corrección formativa. En api-correccion-formativa-ia-galicia abarca los 3 formatos del aula moderna: papel manuscrito (foto), creación plástica/visual (foto de mural o cartulina) y entregas digitales (redacciones online o exportaciones PDF/PNG de presentaciones de Canva).

**Prompt**  
El texto de instrucciones que se envía al modelo de IA. Se divide en dos partes con roles distintos:

- **`system prompt` (instrucción de rol):** Define quién es la IA y cómo debe comportarse en todas sus respuestas. En este proyecto: *"Eres un evaluador formativo experto en Filosofía de Bachillerato del sistema educativo gallego (Decreto 157/2022, Xunta de Galicia). Devuelves ÚNICAMENTE JSON estructurado con el esquema EvaluacionIA. Jamás diagnosticas condiciones médicas ni educativas."* — establece el rol, el idioma, las restricciones legales y el contrato de salida.
- **`user prompt` (la tarea concreta):** Contiene los datos variables de cada corrección: la respuesta del alumno, la rúbrica de la profesora, el marco normativo y las adaptaciones NEAE. Cambia en cada petición.

El `prompt_builder.py` construye dinámicamente el `user prompt` combinando estos datos. El `system prompt` permanece constante en todas las correcciones.

**Structured Outputs** (Salidas Estructuradas)  
Mecanismo que fuerza al modelo de IA a devolver siempre un JSON con un esquema fijo, en lugar de responder en texto libre. Explicado en detalle en `sesion_02_storage_y_structured_outputs.md`.

**Token** (en contexto de IA)  
La unidad mínima de texto que procesa un modelo de lenguaje. Aproximadamente `1 token ≈ 0,75 palabras` en español (o 4 caracteres en inglés). Los modelos cobran por tokens consumidos en ambas direcciones:

| Motor | Precio input | Precio output | Contexto máximo |
|---|---|---|---|
| `Groq llama-3.3-70b` | **Gratuito** (cota) | **Gratuito** (cota) | 128.000 tokens |
| `GPT-4o` | ~$2,50 / M tokens | ~$10 / M tokens | 128.000 tokens |
| `Claude Sonnet` | ~$3 / M tokens | ~$15 / M tokens | 200.000 tokens |

**Ventana de contexto (`context window`):** el límite de tokens que el modelo puede leer de una vez (prompt + respuesta juntos). Si un examen escaneado con mucho texto supera ese límite, el modelo trunca o falla — por eso en `[D-020]` se comprime la imagen en la PWA antes de enviarla.

**En este proyecto:** Groq es el motor primario (`[D-028]`) precisamente porque su cota gratuita permite desarrollar y demostrar el sistema sin coste, con inferencia ultrarrápida.

---

## 5. Almacenamiento e infraestructura

**BLOB / Objeto Binario Grande (Binary Large Object)**  
Colección o bloque en crudo de datos en formato binario (como imágenes en alta resolución `.webp/.jpg` o documentos `.pdf` de exámenes escaneados). En nuestra arquitectura es un antipatrón almacenar BLOBs directamente dentro de las tablas de PostgreSQL porque encarecen el disco y ralentizan las consultas relacionales de auditoría; en su lugar, el archivo físico viaja a un *Object Storage* externo (S3/Cloudinary) y la base de datos solo almacena su URL ligera y metadatos.

**Buffer (en memoria / en disco)**  
Zona intermedia y temporal donde se almacenan datos en tránsito antes de que sean procesados o persistidos definitivamente. En api-correccion-formativa-ia-galicia aparece en dos variantes con implicaciones legales distintas:
- **Buffer en RAM (`BytesIO`):** La imagen del examen se carga directamente en la memoria del proceso Python sin escribirse en ningún fichero físico del disco. `Pillow` recorta la cabecera con el nombre del alumno dentro de ese bloque de bytes en memoria y el resultado anonimizado se envía a la nube. El archivo original con PII **nunca toca el disco** del servidor (`[D-022]`, estándar *Datenschutz* alemán).
- **Buffer local en disco (`/uploads/`):** El archivo temporal se escribe en disco con un nombre UUID y se borra inmediatamente tras completar la subida a la nube (`[D-021]`). Es la opción más simple para el MVP `[v0.3-001]`.

**Broker**  
En el contexto de colas de tareas: el intermediario que recibe las tareas pendientes y las distribuye a los workers. En este proyecto Redis actúa como broker de Celery.

**Celery**  
Librería de Python para ejecutar tareas en segundo plano (de forma asíncrona). Cuando un profesor sube un examen, Celery encola la tarea de corrección para que el servidor no se quede bloqueado esperando. Explicado en `sesion_01_asincronia_y_colas.md`.

**Cold Storage / Almacenamiento en frío**  
Almacenamiento en la nube de muy bajo coste diseñado para archivar archivos que rara vez se consultan pero deben conservarse por imperativo legal (como los exámenes ante posibles reclamaciones). Equivalente digital a un archivo de cajas en un sótano. AWS Glacier y Cloudinary Archive son ejemplos.

**Cloudinary**  
Servicio de almacenamiento y gestión de imágenes en la nube. Las fotos de los exámenes se guardan aquí, no en la base de datos. Tiene capa gratuita generosa. Explicado en `sesion_02_storage_y_structured_outputs.md`.

**Docker** / **Docker Compose**  
Docker permite empaquetar una aplicación con todo lo que necesita en una unidad aislada llamada **contenedor**. La diferencia clave entre sus dos conceptos:

- **Imagen:** la receta — un archivo estático que describe el sistema operativo, las dependencias y la configuración (ej. `postgres:16-alpine` es una imagen de PostgreSQL lista para usar)
- **Contenedor:** la receta ejecutándose — una instancia viva de la imagen, con su propia memoria y red aislada

**Por qué lo usas en este proyecto en lugar de instalar Postgres directamente:**
1. Aislas el PostgreSQL del proyecto del resto del sistema — sin colisiones con otras instalaciones
2. Con un solo `docker compose up -d` levantas la BBDD en el puerto `5433` sin instalar nada en Windows
3. Con `docker compose down` lo apagas todo limpiamente
4. El `docker-compose.yml` del repositorio documenta exactamente cómo reproducir el entorno en cualquier máquina

**Presigned URL** (URL Prefirmada)  
Un enlace temporal y firmado que permite subir un archivo directamente a Cloudinary o S3 sin pasar por el servidor. Explicado con la analogía del aparcacoches en `sesion_02_storage_y_structured_outputs.md`.

**Storage Lifecycle / Política de ciclo de vida**  
Reglas automatizadas configuradas en el proveedor de nube (S3/Cloudinary) que trasladan o eliminan archivos según su antigüedad. En api-correccion-formativa-ia-galicia: pasan a Cold Storage a los 60 días y se eliminan (purga legal RGPD) al año exacto.

**Railway**  
Plataforma de hosting (alojamiento) donde se desplegará el backend en producción. Incluye PostgreSQL y Redis. Tiene plan gratuito suficiente para el MVP.

**Redis**  
Base de datos en memoria, muy rápida. En este proyecto actúa como broker de Celery: guarda la cola de tareas de corrección pendientes. Explicado en `sesion_01_asincronia_y_colas.md`.

**S3** (Amazon Simple Storage Service)  
Servicio de almacenamiento de archivos de Amazon Web Services (AWS). El estándar de la industria para guardar imágenes, vídeos y documentos a escala. En producción sustituirá a Cloudinary.

**Worker**  
Un proceso que ejecuta tareas en segundo plano. Cuando Celery recibe una tarea de corrección, un worker la ejecuta de forma independiente sin bloquear el servidor principal.

---

## 6. Frontend y PWA

**Canvas** (HTML5 Canvas)  
Elemento de HTML que permite dibujar, recortar y transformar gráficos e imágenes en la memoria local del navegador mediante JavaScript. En api-correccion-formativa-ia-galicia: la PWA utiliza el Canvas para redimensionar los exámenes a ~2048px ([D-020]) y recortar los 3 cm de la cabecera con el nombre del alumno ([D-022]) antes de subirlos a la nube.

**Manifest.json**  
Archivo de configuración que le dice al navegador cómo mostrar la PWA cuando se instala: nombre, icono, colores, orientación de pantalla.

**PWA / PWA del Profesor** (Progressive Web App — Aplicación Web Progresiva)  
Una aplicación web construida con tecnologías modernas (React + Vite) que se abre en el navegador pero se comporta y se puede instalar como una app nativa en el portátil, tablet o móvil del docente sin pasar por tiendas de aplicaciones. En api-correccion-formativa-ia-galicia es el panel frontal y centro de mando del profesor (*Human-in-the-Loop*): donde sube las fotos del examen o mural, visualiza la corrección con sus marcadores de color (rojos o grises de adaptación), ajusta la propuesta y aprueba las notas finales. Accessa localmente a cámara y funciona en red de forma ultra veloz.

**React**  
Librería de JavaScript para construir interfaces de usuario. Se trabaja con "componentes" (piezas reutilizables de pantalla). El frontend de la PWA estará construido con React.

**Service Worker**  
Un script que se ejecuta en segundo plano en el navegador. Permite que la PWA funcione sin conexión, gestiona la caché y recibe notificaciones push.

**SSE** (Server-Sent Events — Eventos Enviados por el Servidor)  
Mecanismo por el que el servidor envía actualizaciones al cliente en tiempo real sin que el cliente tenga que preguntar repetidamente. Se usa para notificar al profesor cuando la corrección está lista.

**Vite**  
Herramienta que compila y sirve el código React durante el desarrollo. Es muy rápido (actualiza la pantalla en milisegundos al guardar un archivo). Equivalente moderno a Create React App.

---

## 7. Control de versiones y repositorio

**Branch / Rama**  
Una línea de desarrollo paralela en Git. Permite trabajar en una funcionalidad nueva sin afectar al código principal. En este proyecto: `v0.1-sync-engine`, `v0.2-database`, etc.

**Commit**  
Un punto de guardado en el historial de Git. Cada commit tiene un mensaje que describe qué cambió. Ejemplo: `feat: add evaluate endpoint`.

**Git**  
Sistema de control de versiones. Guarda el historial completo de cambios del código, permite volver atrás y trabajar en paralelo con ramas. Los 4 comandos que usas en cada sesión de trabajo:

```bash
git status              # ¿qué archivos he cambiado?
git add .               # prepara todos los cambios para el commit
git commit -m "feat(hitl): implement approve endpoint" # crea el punto de guardado
git push origin main    # sube los commits a GitHub
```

**Convención de mensajes de commit en este proyecto (`Conventional Commits`):**
- `feat:` — nueva funcionalidad
- `fix:` — corrección de un bug
- `docs:` — cambios en documentación
- `refactor:` — código mejorado sin cambiar su función
- `test:` — tests añadidos o modificados

El historial de commits es parte de tu portfolio — cada `feat:` con su ADR referenciado demuestra madurez de ingeniería.

**GitHub**  
Plataforma web donde se aloja el repositorio Git del proyecto. Es donde los empleadores y reclutadores verán el código y el historial de trabajo.

**Blindaje de Privacidad y Carpeta `scratch/`**  
Estrategia de gobernanza del repositorio por la que se aísla de forma estricta el código e historial público profesional (`models/`, `routers/`, `decisiones.md`) frente a documentación confidencial de trabajo intermedio del desarrollador (guiones de presentaciones en vídeo, notas preparatorias de entrevistas, listas de contactos y planes relacionales de networking). Estos documentos privados residen exclusivamente dentro del directorio local `scratch/`, el cual está bloqueado en el `.gitignore` para garantizar que jamás asciendan a la nube pública de GitHub ni dejen rastro en los commits.

**.gitignore**  

Archivo que le dice a Git qué archivos ignorar y no incluir en el repositorio. Los archivos con claves de API (`.env`), dependencias (`venv/`) y cachés (`__pycache__/`) nunca deben subirse.

**Push**  
Subir los commits locales al repositorio remoto en GitHub.

**Repositorio**  
El proyecto completo gestionado por Git, incluyendo todos los archivos y su historial de cambios.

---

## 8. Herramientas de desarrollo con IA

**AGENTS.md**  
Archivo de texto en la raíz del proyecto que OpenCode lee automáticamente al arrancar. Contiene el contexto del proyecto (arquitectura, convenciones, reglas) para que el agente trabaje con información actualizada sin tener que explicárselo cada vez.

**Antigravity**  
El agente de IA integrado en VS Code (este). Se usa para arquitectura, decisiones de diseño, revisiones críticas y documentación. Consume cuota de Claude Sonnet.

**Diversificación de Tokens (Token Multiplexing)**  
Estrategia de finanzas operativas (*FinOps*) orientada a maximizar la productividad y esquivar límites de cuota gratuita sin sobrecostes. Consiste en combinar múltiples entornos de IA en paralelo (ej. Antigravity en VS Code para arquitectura global + Warp AI Agent en terminal independiente para comandos/DevOps + Groq LPU en el backend), repartiendo la carga de trabajo entre diversos motores y modelos.

**Gemini**  

Familia de modelos de lenguaje de Google. El modelo `gemini-2.5-flash` es el predeterminado en OpenCode por su cota gratuita generosa (1.500 peticiones/día).

**Groq**  
Proveedor de modelos de lenguaje con cuota gratuita muy generosa y velocidad de inferencia muy alta. Se usa en OpenCode para tareas de código complejo (`llama-3.3-70b-versatile`, `qwen3-32b`).

**OpenCode**  
Agente de IA que se ejecuta en la terminal de WSL. Lee y edita archivos directamente, ejecuta comandos, y trabaja dentro del mismo entorno donde corre Python/FastAPI. Se usa para código rutinario, boilerplate y edición de archivos.

**PonyTail**  
Conjunto de reglas que se añade al `AGENTS.md` para que OpenCode siga el principio de mínimo código: antes de escribir algo, comprueba si ya existe una solución más simple. Reduce el consumo de tokens en ~22%.

**WSL** (Windows Subsystem for Linux — Subsistema de Windows para Linux)  
Capa de compatibilidad que permite ejecutar un sistema Linux (Ubuntu) dentro de Windows. Todo el código Python/FastAPI del proyecto corre en WSL porque el ecosistema de herramientas de desarrollo es más estable en Linux.

---

## 9. Legal y normativo

**Adaptaciones Curriculares (ACS / ACNS / DEA)**  
Medidas de modificación o ajuste pedagógico reguladas por la legislación (LOMLOE, Decreto 229/2011 de Galicia) para garantizar la equidad educativa del alumnado. Pueden ser ordinarias o no significativas (ACNS, ej: dislexia, TDAH) sin alterar objetivos, o significativas (ACS) cuando modifican el currículo oficial. En api-correccion-formativa-ia-galicia se inyectan mediante el campo `adaptaciones_alumno` ([D-023]) para separar faltas ortográficas del cálculo penalizador de nota.

**AI Act** (Reglamento Europeo de Inteligencia Artificial)  
La primera ley de la Unión Europea que regula los sistemas de IA. Clasifica los sistemas por nivel de riesgo. api-correccion-formativa-ia-galicia entra en la categoría de alto riesgo (afecta a educación de menores y procesa variables de necesidades específicas), por lo que requiere Human-in-the-Loop y trazabilidad completa.

**DUA** (Diseño Universal de Aprendizaje)  
Enfoque pedagógico recogido por la LOMLOE y la normativa gallega que busca minimizar las barreras en el aprendizaje, ofreciendo múltiples formas de representación, expresión e implicación en la evaluación.

**HitL / Human-in-the-Loop** (Humano en el Bucle)  
Diseño en el que la IA propone pero el humano decide. En este proyecto: la IA genera un borrador de corrección, pero el profesor tiene que aprobarlo antes de que sea oficial. Es el escudo legal bajo el AI Act.

**Inmutabilidad probatoria**  
Propiedad por la cual un registro o evaluación ya aprobada (`GRADED`) queda bloqueada contra modificaciones o borrados posteriores (*append-only*). Garantiza la validez jurídica del historial ante inspecciones educativas, reclamaciones de exámenes o auditorías bajo el AI Act.

**LOMLOE** (Ley Orgánica de Modificación de la LOE — Ley de Educación)  
La ley educativa estatal actualmente vigente en España (2020). Define competencias, criterios de evaluación y estructura curricular. El decreto autonómico de la Xunta de Galicia la desarrolla a nivel regional para el sistema educativo gallego (bilingüe castellano/gallego).

**LOPDGDD** (Ley Orgánica de Protección de Datos y Garantía de los Derechos Digitales)  
La ley española que desarrolla el RGPD. Su artículo 7 regula el consentimiento y protección integral en el tratamiento de datos de menores. En api-correccion-formativa-ia-galicia es crítico porque la información sobre adaptaciones por dislexia, TDAH o TEA constituye un dato de salud del menor (especialmente protegido), motivo por el cual la IA jamás diagnostica y el dato solo se asocia al identificador seudonimizado `alumno_id` ([D-023]).

**NEAE / NEE** (Necesidades Específicas de Apoyo Educativo / Necesidades Educativas Especiales)  
Clasificación legal en España para el alumnado que requiere una atención educativa diferente a la ordinaria por presentar dificultades específicas de aprendizaje (DEA como dislexia), TDAH, altas capacidades o discapacidad (NEE). api-correccion-formativa-ia-galicia adapta su motor formativo para que estos perfiles sean evaluados con justicia sin penalizar errores derivados de su condición ([D-023]).

**RGPD** (Reglamento General de Protección de Datos)  
La ley europea de privacidad de datos. Obliga a proteger los datos personales, especialmente los de menores. En este proyecto: los exámenes se anonimizan antes de enviarse a la IA (campo `alumno_id`), y OpenAI/Anthropic tienen contratos de Zero Data Retention.

**Seudonimización / Pseudonimización**  
Tratamiento de datos personales de forma que no puedan atribuirse a un sujeto concreto sin utilizar información adicional que se custodia por separado. En el proyecto: en la nube solo guardamos el código `alumno_id` ("A-14"), mientras que la relación con el nombre e identidad real permanece en el ámbito privado y local del docente.

**Zero Data Retention** (Cero Retención de Datos)  
Acuerdo contractual con el proveedor de IA por el que los datos enviados al modelo no se guardan ni se usan para reentrenamiento. OpenAI y Anthropic ofrecen esta opción para uso empresarial/API.

---

## 10. Metodología y gestión

**ADR** (Architecture Decision Records — Registro de Decisiones de Arquitectura)  
Documento donde cada decisión técnica importante queda registrada con su contexto, las alternativas consideradas y el motivo de la elección. En este proyecto: `decisiones.md`.

**Comparative Judgement / Juicio Comparativo**  
Metodología pedagógica innovadora (ej. *No More Marking* en Reino Unido) donde se evalúa el razonamiento cualitativo global en lugar de contar puntos mecánicos aislados (`[D-024]`).

**Doble Circuito de Calificación (Materias vs. Competencias Clave)**  
Modelo operativo dual vigente en los IES gallegos (Decretos 156/157/2022) y reflejado en XADE/api-correccion-formativa-ia-galicia: 1) **Circuito de Materias:** Las asignaturas se califican y cierran en los boletines trimestrales y ordinarios con **números enteros del 1 al 10** derivados de las notas cotidianas numéricas de las pruebas evaluables. 2) **Circuito de Competencias Clave:** Las 8 competencias oficiales (*CCL, STEM, CD...*) se califican al final del curso de forma cualitativa (*IN, SU, BI, NT, SB*) mediante el **cruce e intersección matricial inter-materias** de todos los criterios evaluados en las diferentes asignaturas del alumno.

**Deuda Técnica (`Technical Debt` / Deuda Consciente)**  
Coste estratégico de ingeniería que se asume al aplazar o simplificar deliberadamente una implementación en la fase actual para priorizar la entrega rápida y limpia de un hito, con el compromiso explícito de refactorizarla o completarla en una iteración posterior. En api-correccion-formativa-ia-galicia, un ejemplo es no persistir aún los binarios de subida en la tabla `Submission` durante `[v0.3-001]` porque dicha lógica se rediseñará integralmente al introducir el recorte de cabecera pre-nube con `Pillow` en `[v0.3-002]` (*YAGNI*).

**Equipotencialidad Criterial (`Decreto 156/157/2022`)**  
Regla pedagógica general y por defecto por la que todos los Criterios de Evaluación (`criterio_id`) asociados a las competencias específicas de una materia tienen idéntico valor o peso en el cálculo de la nota final, salvo que el departamento establezca porcentajes diferenciados en su Programación Didáctica (`Capa 2`).

**Evaluación Competencial Cualitativa (`Decretos 156/157/2022 Galicia`)**  
Modelo evaluativo obligatorio en Galicia para ESO y Bachillerato centrado en el grado de adquisición de las competencias clave y específicas del currículo, expresado en grados cualitativos (*Insuficiente [IN], Suficiente [SU], Bien [BI], Notable [NT], Sobresaliente [SB]*) además o en lugar de la nota numérica simple (`[D-024]`).

**Feed Forward / Actionable Next Steps (Siguiente Paso Accionable y Seguimiento No Sumativo)**  
Estándar pedagógico anglosajón (modelo Hattie & Timperley en GCSE/A-Levels del Reino Unido) que soluciona el problema de la "IA cierta pero inútil". Exige que cada corrección formativa proporcione una acción única, concreta e inmediata que el alumno puede hacer hoy mismo para avanzar (`[D-024]`). Para no sobrecargar al docente con dobles correcciones, su cumplimiento se modela como un checklist formativo y de autoevaluación en base de datos (`estado_feed_forward: PENDIENTE | REALIZADO | VERIFICADO`) sin calificación sumativa (`[D-026]`).

**Fuente de Verdad por Plano (`Single Source of Truth by Plane`)**  
Principio de gobernanza (`[D-035]`) según el cual cada tipo de información técnica o de gestión reside en un único archivo maestro para evitar duplicidades, desfases o contradicciones entre código y documentación.

**Los 5 archivos clave del proyecto:**
- `decisiones.md` → Fuente de verdad para las decisiones arquitectónicas (`ADRs`).
- `AGENTS.md` → Fuente de verdad para el comportamiento operativo y reglas del asistente de IA.
- `README.md` → Fuente de verdad para la visibilidad técnica, arquitectura y endpoints del backend.
- `backlog.md` → Fuente de verdad para la planificación, historias de usuario y deuda técnica.
- `AUDITORIA.md` → Fuente de verdad para el estado de auditoría interna y el cumplimiento por pilares.

**Backlog**  
Lista priorizada de todo el trabajo pendiente del proyecto, organizado en historias de usuario. En este proyecto: `backlog.md`.

**Criterios de aceptación**  
Lista de condiciones concretas y verificables que deben cumplirse para considerar una historia de usuario terminada. Sin criterios claros, no hay forma de saber cuándo algo está "listo".

**Historia de usuario**  
Forma de describir una funcionalidad desde el punto de vista del usuario final. Formato: "Como [rol], quiero [acción], para [beneficio]". Es la unidad de trabajo del backlog.

**Milestone**  
Punto de referencia en el roadmap del proyecto. En este proyecto equivale a una versión (v0.1, v0.2...). Cada milestone agrupa las historias de usuario de esa versión.

**Modo Copiloto / Trabajo en Terminal (HitL Técnico)**  
Metodología de desarrollo en parejas por la que la Inteligencia Artificial asume el rol de arquitecta y generadora de andamiaje de código (`Punto 2: Qué hicieron los agentes`), mientras que la desarrolladora humana ejerce el liderazgo operativo ejecutando en su propia terminal (WSL/Warp) todos los comandos de validación, levantamiento de base de datos (`docker compose`), migraciones (`alembic upgrade head`) y commits (`Punto 3: Cómo validé yo`). Esto preserva la memoria muscular técnica, el control soberano del entorno y la autoría intelectual superior del portfolio (`[D-029]`).

**MVP** (Minimum Viable Product — Producto Mínimo Viable)  
La versión más pequeña del producto que ya aporta valor real. En este proyecto: v1.0 desplegada y funcionando.

**Ponderación Criterial vs. Instrumental**  
Mandato legal de la LOMLOE en Galicia según el cual la calificación y ponderación recae siempre sobre los **Criterios de Evaluación (`criterio_id`)** del currículo, y nunca sobre los instrumentos en sí mismos. Los instrumentos (exámenes, murales de cartulina o exposiciones en *Canva*) son únicamente el soporte o medio omni-canal de recogida de evidencias de aprendizaje.

**Protocolo Stop & Consult (Pausa Arquitectónica y Freno Conductual)**  
Norma de co-piloteo (`Regla 5 de AGENTS.md`) que prohibe terminantemente a los agentes de IA aplicar parches ad-hoc, fallbacks o modificaciones de archivos ante errores técnicos de API/código sin antes consultar. El agente debe detener su turno, entregar un diagnóstico técnico riguroso y presentar al menos dos opciones arquitectónicas contrastadas contra el principio YAGNI para tomar una decisión en equipo (`[D-029]`). Asimismo, separa de forma estricta las órdenes de revisión e inspección ("analiza", "piensa") de las órdenes de edición ("modifica", "aplica").

**Refinement / Refinamiento del Backlog (`Backlog Refinement`)**  
Actividad continua en la que se revisan, clarifican y desglosan las historias de usuario pendientes (`backlog.md`) antes de entrar en ejecución. Su objetivo es mantener el backlog relevante y manejable, asegurar que las tareas futuras tengan alcance acotado y criterios de aceptación verificables, y que cualquier impacto arquitectónico o de auditoría (`decisiones.md` / ADRs) se haya considerado antes de empezar a programar.

**Situación de Aprendizaje (SdA)**  
Propuesta metodológica o tarea reto contextualizada (real o simulada) que permite al alumnado movilizar saberes básicos para resolver un problema, siguiendo la trazabilidad `Reto → Saberes → Competencias Específicas → Criterios → Descriptores Operativos`. En api-correccion-formativa-ia-galicia actúa como el Contenedor Padre (`situacion_aprendizaje_id` en Capa 2) para agrupar todas las pruebas evaluables omni-canal del alumno en esa unidad y calcular el logro de sus competencias.

**Sprint Planning / Planificación de Sprint (`Sprint Planning`)**  
Evento de planificación en el que se seleccionan, de entre las historias ya refinadas, las tareas que se van a ejecutar en el próximo intervalo de trabajo (semana, sprint, bloque). Su objetivo es definir un objetivo claro de sprint, comprometer una cantidad realista de trabajo en función de la capacidad disponible y acordar cómo se va a abordar técnicamente ese trabajo, sin volver a abrir debates de refinamiento. Refinement prepara el backlog; Sprint Planning decide qué parte de ese backlog se ejecuta ahora.

**Soberanía del Acto Administrativo (`HitL`)**  
Principio fundamental del Derecho Público español y del *AI Act* que dictamina que la responsabilidad jurídica, formal y humana y el poder de decisión sobre una calificación oficial (*que constituye un acto administrativo con efectos en la promoción o titulación del alumno*) recae exclusiva e intransferiblemente en el docente o tribunal que firma el acta en XADE. Una IA o aplicación comercial jamás puede ser autora ni titular legal del acto administrativo; por ello, api-correccion-formativa-ia-galicia asiste y calcula, pero exige siempre la validación y firma humana final del profesor (*Human-in-the-Loop*).

**Smoke test**  

Prueba muy básica que verifica que lo más fundamental funciona antes de construir nada encima. En este proyecto: `v0.1-000` comprueba que la IA devuelve el JSON correcto antes de construir FastAPI.

**Trade-off (`Trade-off` / Compromiso Arquitectónico)**  
Principio universal de ingeniería y diseño de sistemas por el cual no existe una solución perfecta o gratuita, sino que para obtener una ventaja en una dimensión (como precisión, resiliencia o velocidad) se debe ceder o asumir un coste en otra (como latencia, consumo de tokens o complejidad de infraestructura). En nuestro proyecto se evalúan conscientemente en cada decisión: por ejemplo, asumir mayor consumo de tokens multimodales en la Versión 0.3 por ganar precisión pedagógica y marcadores x-y, o asumir la necesidad de contenedores extra en la Versión 0.1 con Celery y Redis por ganar resiliencia inmutable al 100% bajo el AI Act.

**XADE (`Xestión Administrativa da Educación`)**  
Aplicación informática oficial de la Xunta de Galicia (Consellería de Educación) para todos los centros docentes gallegos. Es donde las secretarías y equipos docentes matriculan al alumnado e introducen las notas numéricas por materia y cualitativas por competencias clave para cerrar actas e imprimir boletines en cada junta de evaluación. api-correccion-formativa-ia-galicia asiste y calcula el día a día para que el trasvase final de datos de corrección a XADE sea rápido, seguro y 100% auditable.

**YAGNI** (You Aren't Gonna Need It — No lo vas a necesitar)  
Principio de desarrollo: no escribas código para funcionalidades que no necesitas ahora mismo. Evita sobre-ingeniería.

---

## 11. Seguridad y autenticación

**API key**  
Clave secreta que identifica y autentica a quien llama a una API. Las claves de OpenAI, Anthropic, Gemini y Groq son API keys. Nunca se suben al repositorio — van en el archivo `.env`.

**Bearer token**  
Tipo de token de autenticación que se envía en la cabecera HTTP de cada petición: `Authorization: Bearer <token>`. Los JWT se usan como Bearer tokens.

**Cifrado Simétrico vs. Seudonimización (Blindaje sin Clave Maestra)**  
Estrategia arquitectónica (`YAGNI`) por la cual se descarta el cifrado de columnas con clave maestra simétrica (`ENCRYPTION_KEY` / `Fernet`) para evitar el riesgo catastrófico de pérdida irrecoverable de datos ante un extravío o corrupción de la clave en `.env`. En su lugar, la privacidad y protección de los datos sensibles del alumnado (`[D-023]`) se resuelve de raíz mediante **Seudonimización Estricta (`HitL Client-Side`)**: en la base de datos de la nube solo se almacena un identificador anónimo (`alumno_id = "A-14"`), mientras que la tabla de equivalencias con la identidad real permanece exclusivamente en el cuaderno y XADE local de la profesora, haciendo que la base de datos sea intrínsecamente inocua sin depender de claves criptográficas frágiles.

**Client-Side Blackout Tool (`Herramienta de Tampón o Redacción Visual en Navegador`)**  
Segunda capa de verificación y redacción en PWA (`[D-034]`). Además del recorte automático superior (`[D-022]`), permite a la profesora difuminar o plantar recuadros negros manualmente con el dedo/ratón sobre la vista previa del Canvas antes de confirmar el envío a la nube si un alumno escribió su nombre fuera del encabezado. La destrucción de píxeles ocurre en el propio dispositivo del cliente, asegurando *Zero Data Retention*.

**Hacheo Unidireccional (`bcrypt` / Password Hashing)**  
Algoritmo criptográfico irreversible (de un solo sentido) utilizado en `backend/services/auth_service.py` para almacenar las contraseñas (`hashed_password`) en la tabla `profesores` (`[v0.2-002]`). A diferencia del cifrado simétrico, no requiere ni depende de ninguna clave maestra secreta en `.env` para funcionar; aplica un cálculo matemático complejo sobre la contraseña (`salt + hash`). Para validar un login, el motor aplica la misma fórmula al texto ingresado y compara los hashes resultantes, garantizando seguridad absoluta ante filtraciones y cero riesgo de pérdida por reinicios o migraciones de servidor.

**.env**  
Archivo de texto que contiene variables de entorno (claves de API, contraseñas, configuración sensible). Nunca se sube a GitHub — está en el `.gitignore`. El archivo `.env.example` muestra qué variables existen sin revelar sus valores.

**ENS (Esquema Nacional de Seguridad)**  

Regulamento y marco normativo obligatorio que fija los requisitos y políticas de ciberseguridad en la Administración Pública y en los sistemas que tratan datos institucionales o de ciudadanos (como XADE en Galicia). Debido a las rigurosas exigencias del ENS y de AMTEGA sobre la protección de datos de menores, se prohíbe la conexión o inyección externa por APIs privadas comerciales directamente en XADE, justificando que el trasvase desde api-correccion-formativa-ia-galicia se realice localmente mediante exportación de ficheros o scripts locales en el navegador del funcionario (`[D-025]`).

**Escáner Local Offline de PII (`Automated Offline PII Shield`)**  
Mecanismo secundario en servidor local (`Roadmap v0.8` en `[D-034]`) que procesa la imagen en memoria local con un micro-motor OCR/PII offline (*Tesseract / Microsoft Presidio*) antes de enviarla a la nube. Si detecta texto compatible con nombres propios del listado de la clase que hayan escapado del recorte superior, bloquea la subida con error 422 y protege al colegio de infracciones RGPD.

**JWT** (JSON Web Token — Token Web JSON)  
Token firmado digitalmente que el servidor entrega al docente tras el login. Tiene **3 partes separadas por puntos**, cada una codificada en Base64:
- **Header:** algoritmo de firma usado (`HS256`)
- **Payload:** datos del usuario (`profesor_id`, fecha de expiración)
- **Signature:** firma criptográfica generada con la `SECRET_KEY` del servidor — garantiza que el token no fue manipulado

**Flujo completo en api-correccion-formativa-ia-galicia:**
1. La profesora hace `POST /api/v1/auth/login` con su contraseña
2. El servidor verifica el hash `bcrypt` — si coincide, genera el JWT firmado con la `SECRET_KEY`
3. La profesora guarda el JWT en el navegador (localStorage o cookie)
4. Cada petición protegida incluye la cabecera: `Authorization: Bearer <JWT>`
5. El servidor verifica la firma con la `SECRET_KEY` — si es válida, sabe quién es sin consultar la BBDD

**Por qué importa ante la AESIA:**
- **Stateless:** el servidor no guarda sesiones en memoria — cumple el principio REST (`[D-031]`)
- **La `SECRET_KEY`** es lo que hace la firma inviolable — el servidor aborta al arrancar si está vacía o es el valor por defecto (`startup_validation()`)
- **Expiración automática:** el token caduca tras un tiempo definido — el docente debe hacer login de nuevo

**PII (`Personally Identifiable Information` / Información Personalmente Identificable)**  
Cualquier dato o rastro identificativo (como nombre completo, DNI, firma, correo electrónico o foto de rostro) que permita vincular directa o indirectamente un examen con una persona física. Su subida o cesión no anonimizada a servidores de IA en terceros países está estrictamente prohibida por el RGPD cuando se trata de menores de edad.

**Variables de entorno**  
Valores de configuración que se inyectan en el programa desde el sistema operativo o desde un archivo `.env`, sin escribirlos directamente en el código. Separa la configuración del código.

---

## 12. Negocio y modelo

**B2B** (Business to Business — De empresa a empresa)  
Modelo en el que el cliente es otra empresa, no un usuario individual. En api-correccion-formativa-ia-galicia: colegios o plataformas EdTech que contratan la API con una API key.

**B2C** (Business to Consumer — De empresa a consumidor)  
Modelo en el que el cliente es un usuario individual. En api-correccion-formativa-ia-galicia: profesores que se suscriben directamente a la PWA.

**EdTech** (Education Technology — Tecnología educativa)  
Sector de empresas que desarrollan productos tecnológicos para la educación. Son los potenciales clientes B2B de api-correccion-formativa-ia-galicia.

**Freemium**  
Modelo de negocio con una versión gratuita (con límites) y una versión de pago (sin límites o con funcionalidades extra).

**SaaS** (Software as a Service — Software como Servicio)  
Modelo en el que el software se ofrece como servicio por suscripción, sin que el usuario tenga que instalarlo. La PWA de api-correccion-formativa-ia-galicia es un SaaS.

---

*Glosario creado el 09/07/2026 — Antigravity para Alba Camiña García*  
*Documento vivo — se actualiza con cada término nuevo que aparezca en el proyecto*
