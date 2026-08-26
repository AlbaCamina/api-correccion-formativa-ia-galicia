# 📖 Glosario — API de Corrección Formativa con IA (`api-correccion-formativa-ia-galicia`)
**Proyecto:** API de Corrección Formativa con IA (`api-correccion-formativa-ia-galicia`)  
**Responsable:** Alba Camiña García  
**Inicio:** Julio 2026

> [!NOTE]
> Documento vivo. Cada vez que aparezca un término nuevo en el proyecto, se añade aquí con su explicación. Los términos están organizados por categoría y ordenados alfabéticamente dentro de cada una.

---

## 1. Conceptos generales de desarrollo web

**Breaking Change**  
Cambio que rompe la compatibilidad hacia atrás. Ejemplo arquitectónico (`[D-041]`): hacer obligatorio el campo `etapa` en `EvaluationRequest`, de manera que los clientes antiguos que no lo envíen recibirán un error `422 Unprocessable Entity`.

**CORS** (Cross-Origin Resource Sharing — Intercambio de Recursos de Origen Cruzado)  
Mecanismo de seguridad de los navegadores web que restringe las peticiones HTTP realizadas desde un dominio o puerto (ej. `http://localhost:5173` en Vite) hacia otro diferente (`http://127.0.0.1:8000` en FastAPI). Por especificación oficial, cuando se permite el envío de credenciales o tokens Bearer (`allow_credentials=True`), está prohibido usar un comodín (`allow_origins=["*"]`) por riesgo de seguridad; se exige declarar explícitamente los orígenes confiables.

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

| Versión | Endpoint | Verbo | Función | Estado |
|---|---|---|---|---|
| v0.1 | `/api/v1/evaluate` | `POST` | Corrección síncrona con texto plano | ✅ Implementado |
| v0.2 | `/api/v1/auth/register` | `POST` | Registro de profesora | ✅ Implementado |
| v0.2 | `/api/v1/auth/login` | `POST` | Login → devuelve JWT | ✅ Implementado |
| v0.2 | `/api/v1/auth/login-json` | `POST` | Login en formato JSON puro (alternativo a form-data) | ✅ Implementado |
| v0.2 | `/api/v1/auth/me` | `GET` | Perfil de la profesora autenticada | ✅ Implementado |
| v0.2 | `/api/v1/rubricas` | `POST` | Crear una rúbrica | ✅ Implementado |
| v0.2 | `/api/v1/rubricas` | `GET` | Listar todas las rúbricas de la profesora | ✅ Implementado |
| v0.2 | `/api/v1/rubricas/{id}` | `GET` | Consultar una rúbrica concreta | ✅ Implementado |
| v0.2 | `/api/v1/rubricas/{id}` | `PUT` | Editar una rúbrica completa | ✅ Implementado |
| v0.2 | `/api/v1/rubricas/{id}` | `DELETE` | Eliminar una rúbrica | ✅ Implementado |
| v0.2 | `/api/v1/evaluate` | `POST` | Corrección con BBDD + marco normativo | ✅ Implementado |
| v0.2 | `/api/v1/marcos` | `GET` | Listar marcos normativos disponibles | ✅ Implementado |
| v0.3 | `/api/v1/submissions/upload` | `POST` | Subida de imagen/PDF del examen | ✅ Implementado |
| v0.3 | `/api/v1/submissions/{id}/feed-forward/realizado` | `PATCH` | Alumno marca el feed-forward como realizado | ✅ Implementado |
| v0.3 | `/api/v1/submissions/{id}/feed-forward/verificado` | `PATCH` | Profesora verifica el feed-forward del alumno | ✅ Implementado |
| v0.3 | `/api/v1/evaluaciones/{id}/approve` | `PATCH` | Aprobación HitL docente (`REVIEW → GRADED`) | 🔜 Roadmap |
| v0.4 | `/api/v1/submissions` | `GET` | Lista paginada de entregas del docente | 🔜 Roadmap |
| v0.4 | `/api/v1/submissions/{id}/events` | `GET` (SSE) | Stream de estado en tiempo real | 🔜 Roadmap |
| v1.0 | `/api/v1/submissions/{id}/changelog` | `GET` | Historial inmutable de auditoría AI Act | 🔜 Roadmap |

**Fallo silencioso (Silent Failure)**  
Un error en el sistema que no interrumpe la ejecución ni muestra un mensaje de error visible, pero que corrompe el estado o produce resultados incorrectos. Ejemplo en código: si la API no validara correctamente una respuesta nula y la IA asignase un "NA" sin avisar.

**Fallback**  
Plan B o mecanismo de respaldo automático que se activa cuando el sistema principal falla en tiempo de ejecución. Un fallback entre proveedores LLM consistiría en: si la llamada a OpenAI falla, el sistema lo detecta automáticamente y reintenta con Groq (o viceversa), sin intervención humana.

En api-correccion-formativa-ia-galicia este patrón fue considerado pero **descartado por YAGNI** al implementar la v0.3 (`[D-051]`): añadir un fallback real entre OpenAI (Vision) y Groq no es trivial, porque Groq no tiene *Structured Outputs* nativos para esquemas JSON complejos — exactamente el problema que originó la migración a OpenAI. Un fallback hacia Groq en visión reproduciría el error 400 que se quería evitar. En su lugar se optó por *Workload Routing* estático (decisión de proveedor fija por tipo de carga) y 2 reintentos al mismo proveedor como resiliencia suficiente para el MVP.

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
| `pillow` | Librería | *(v0.3 — PoC)* Librería de procesado de imagen en Python. Usada en `scratch/pillow_crop_test.py` para validar el algoritmo de recorte de cabecera (ratio 0.20) antes de portarlo a JavaScript/Canvas. El recorte real en producción ocurre en el cliente (PWA), no en el backend (`[D-022]`, `[D-034]`) |
| `python-dotenv` | Librería | Carga variables de entorno del archivo `.env` |
| `pytesseract` | Librería | *(c0.8)* OCR offline para el escáner de PII pre-nube (`[D-034]`) |
| `react` | Librería | Construye la interfaz de usuario de la PWA del docente |

**Mojibake**  
Texto ilegible o corrupto resultante de decodificar datos de texto utilizando una codificación de caracteres incorrecta (como interpretar UTF-8 como ISO-8859-1). Ejemplo: caracteres extraños en `backlog.md` antes de forzar explícitamente el `encoding="utf-8"` en el script de reparación.

**Nativo / Integración Nativa (`Native / Built-in`)**  
Capacidad o funcionalidad que viene incorporada de fábrica en el núcleo de una herramienta o tecnología, sin necesidad de instalar librerías de terceros, añadir capas intermedias o usar parches artesanales. En nuestra arquitectura priorizamos soluciones nativas para mantener un código limpio, rápido y con mínimas dependencias (`YAGNI`): por ejemplo, la generación de documentación Swagger en `/docs` nativa de FastAPI, y la gestión del pool de conexiones nativo en SQLAlchemy. En cuanto a la validación del contrato `EvaluacionIA`, la solución nativa varía según el proveedor: con OpenAI se usa `Structured Outputs` con `.parse()` (el modelo garantiza el JSON antes de enviarlo); con Groq o Claude se usa `response_format={"type": "json_object"}` + `model_validate_json()` de Pydantic en el cliente.

**Parseo / Parsear (`Parsing` / `.parse()`)**  
Proceso informático de analizar, desgranar y convertir una cadena de datos en bruto (como un texto plano o una respuesta JSON por red) en una estructura de datos tipada, navegable y comprensible para el lenguaje de programación (como un objeto o instancia Pydantic en Python). En api-correccion-formativa-ia-galicia el mecanismo concreto depende del proveedor configurado en `LLM_PROVIDER`:
- **`openai`:** `client.beta.chat.completions.parse()` — el modelo garantiza JSON válido antes de enviarlo; `.parsed` devuelve ya una instancia `EvaluacionIA`.
- **`groq` (y futuro `claude`):** `client.chat.completions.create()` con `response_format={"type": "json_object"}` — el modelo devuelve un string JSON que `EvaluacionIA.model_validate_json()` valida en el cliente.

El **contrato `EvaluacionIA` y la validación Pydantic son siempre necesarios** con cualquier proveedor — solo cambia *quién* garantiza el formato: la API de OpenAI en el primer caso, Pydantic en el cliente en el segundo.

**PEP 8 (`Python Enhancement Proposal 8`)**  
Guía de estilo oficial para la escritura de código en el lenguaje Python. Define normas ampliamente aceptadas de legibilidad, organización y formato, como la agrupación de importaciones en bloques (librería estándar, paquetes de terceros y módulos locales separados por líneas en blanco), el uso de dos líneas en blanco antes de funciones y clases de nivel superior, la indentación de 4 espacios y convenciones de nombres como `snake_case` para funciones/variables y `PascalCase` para clases y modelos. En este proyecto, la aplicación sistemática de PEP 8 refuerza la modularidad plana y el tipado estricto, manteniendo un backend claro, mantenible y alineado con los estándares profesionales de la comunidad Python. En particular, se ha reforzado la agrupación correcta de importaciones y el espaciado vertical en archivos como `submission.py`.

**Pipeline** (Cadena de Procesamiento o Tubería de Datos)  
Secuencia ordenada y automatizada de pasos donde la salida (*output*) de un proceso se convierte directamente en la entrada (*input*) del siguiente paso, similar a una cadena de montaje industrial. En api-correccion-formativa-ia-galicia se analiza en la Versión 0.3 (`sesion_03_ocr_vs_multimodal_vision.md`) comparando un *Pipeline en 2 pasos* (Foto $\rightarrow$ OCR $\rightarrow$ LLM $\rightarrow$ JSON) frente a un *Pipeline Unificado Multimodal en 1 paso* (Foto $\rightarrow$ Vision LLM $\rightarrow$ JSON con marcadores espaciales x,y).

**Polling (Consulta Periódica)**  
Técnica cliente-servidor en la que la aplicación (PWA) realiza peticiones HTTP repetidas a intervalos regulares (ej. cada 3 segundos a `GET /api/v1/submissions/{id}`) para verificar si una tarea en segundo plano ha cambiado de estado (`ANALYZING → REVIEW`). Es sencilla pero genera tráfico redundante si la tarea tarda tiempo. Es el mecanismo alternativo/complementario a Server-Sent Events (SSE).

**Server-Sent Events (SSE — Eventos Enviados por el Servidor)**  
Mecanismo de comunicación en tiempo real en una sola dirección (servidor $\rightarrow$ cliente) basado en el protocolo HTTP (`text/event-stream`). Permite que el backend notifique automáticamente a la PWA del docente en cuanto la IA termina la evaluación en segundo plano (`STATUS_UPDATE: REVIEW`), sin necesidad de recargar la página ni realizar peticiones repetidas (*polling*). Si el cliente cierra el navegador, el servidor detecta el cierre del canal y destruye el stream de forma limpia mientras la tarea de fondo continúa su ejecución en BBDD.


**Scaffolding** (Andamiaje o Estructura Inicial de Código)  
Generación automática o manual del esqueleto básico de un proyecto antes de empezar a escribir la lógica interna de negocio. Consiste en crear la jerarquía de carpetas principales, archivos de configuración (como `package.json`, `.env.example`, `main.py` o `docker-compose.yml`) y plantillas estructurales vacías. Proporciona los cimientos ordenados sobre los que evoluciona el código.

**Stateless vs. Stateful** (Sin Estado vs. con Estado / Transaccional)  
Un sistema es **Stateless** cuando el servidor no conserva memoria ni registro de las peticiones previas (como nuestra API v0.1: evaluaba un texto y olvidaba al usuario instantáneamente). Un sistema es **Stateful o Transaccional** cuando mantiene un estado coherente y persistente en el tiempo (como nuestra API v0.2: autentica al docente con JWT, verifica la propiedad de la rúbrica en base de datos, almacena la entrega en la tabla `Submission` y audita cada acción en un `ChangeLog` inmutable).

**REST** (Representational State Transfer — Transferencia de Estado Representacional) **/ Arquitectura REST (`RESTful`)**  
Estilo arquitectónico que define cómo deben comunicarse los sistemas en internet mediante HTTP. No es un protocolo ni una librería — es un conjunto de principios de diseño que, si se cumplen, la API se denomina "RESTful". Los principios clave que aplica api-correccion-formativa-ia-galicia son:
- **Cliente-Servidor:** React (PWA) y FastAPI son independientes y se comunican solo por HTTP.
- **Sin estado (`Stateless`):** Cada petición lleva toda la información necesaria en la cabecera JWT — el servidor no recuerda sesiones entre peticiones.
- **Interfaz Uniforme:** Las URLs nombran *recursos* y los verbos HTTP nombran *acciones* (`POST /rubricas` crea, `GET /rubricas` lista, `DELETE /rubricas/{id}` elimina). Una API no REST pondría el verbo en la URL: `POST /deleteRubrica`.
- **Sistema en Capas:** El docente llama a FastAPI; FastAPI llama a Groq y PostgreSQL internamente sin que la PWA lo sepa.
- **Recursos Identificables:** Cada entidad tiene su propia URL única (`/api/v1/evaluaciones/f47ac10b` identifica una sola evaluación).

**Swagger / OpenAPI**  
Dos conceptos relacionados pero distintos que trabajan juntos:
- **OpenAPI** es el **estándar** — un documento JSON/YAML generado automáticamente que describe toda la API: qué endpoints existen, qué datos aceptan y qué devuelven. FastAPI lo genera solo leyendo los decoradores `@router.post(...)` y los modelos Pydantic, sin que tengas que escribir nada extra.
- **Swagger UI** es la **interfaz visual** — una página web interactiva que lee ese documento OpenAPI y lo convierte en formularios usables.

**Cómo funciona en la práctica:** con el servidor arrancado, abres `http://127.0.0.1:8000/docs` en el navegador y ves todos los endpoints listados. Para cada uno puedes hacer clic, rellenar los campos del formulario y pulsar **"Execute"** para enviar una petición real y ver la respuesta del servidor al instante — sin escribir ningún comando ni abrir herramientas externas como Postman.

**Ejemplo con api-correccion-formativa-ia-galicia:** abres `/docs`, haces clic en `POST /api/v1/auth/login`, introduces un email y contraseña, pulsas Execute y ves el JWT devuelto en pantalla. Luego puedes copiar ese token y usarlo en el botón **"Authorize"** (candado arriba a la derecha) para probar los endpoints protegidos.

---

## 2. Python y backend

**Alembic**  
Herramienta oficial de migraciones transaccionales para SQLAlchemy. Funciona como un "Git para la estructura de tu base de datos": en lugar de crear o modificar tablas a mano con comandos SQL sueltos (lo que causaría caos entre entornos), Alembic genera archivos de revisión temporales en Python (`alembic revision -m "nombre"`) dentro de `alembic/versions/` que describen exactamente cómo subir (`upgrade`) o retroceder (`downgrade`) el esquema. Al ejecutar `alembic upgrade head`, el motor aplica las revisiones en orden estricto, garantizando que la estructura de la base de datos sea siempre auditable, reproducible y 100% idéntica entre tu WSL local, tu Docker y el servidor de producción (`[D-030]`).

**BackgroundTasks (Tareas en Segundo Plano de FastAPI)**  
Herramienta nativa de FastAPI que permite desencadenar funciones asíncronas de ejecución prolongada inmediatamente después de enviar la respuesta HTTP al cliente. En nuestra arquitectura (`[D-048]`), al recibir una entrega de examen, el endpoint responde de inmediato con HTTP `202 Accepted` (`status: ANALYZING`) y delega la llamada pesada a OpenAI Vision (`vision_service` + `llm_client`) a una `BackgroundTask`. Esto garantiza latencias mínimas (<500ms) sin necesidad de infraestructura compleja como Celery/Redis en la fase MVP. Si el cliente/docente cierra la ventana del navegador o apaga el dispositivo, la tarea en segundo plano continúa ejecutándose hasta guardar el resultado final en la base de datos (`status: REVIEW`).



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

**Clase (Class)**  
Plantilla para crear objetos en programación orientada a objetos que define propiedades (atributos) y comportamientos (métodos). Ejemplo de código: `class EvaluacionIA(BaseModel):` en Pydantic define la estructura de validación.

**Diccionario (Dictionary)**  
Estructura de datos en Python que guarda pares de clave-valor (`{ "etapa": "BACH" }`). Aunque es útil para mockear datos, el tipado estricto (`Regla 3 de AGENTS.md`) dicta preferir modelos Pydantic antes que diccionarios genéricos para evitar fallos de integridad.

**Event Loop & Corrutina (`async / await`)**  
El **Event Loop** (Bucle de Eventos de `asyncio`) es el motor que permite al servidor Uvicorn gestionar cientos de peticiones concurrentes en un solo hilo de procesador. Una **Corrutina** (`async def`) cede el control al bucle cuando encuentra una operación de entrada/salida precedida por `await` (como una llamada HTTP a Groq o consulta a base de datos), permitiendo que el servidor atienda a otros profesores mientras la red responde (`I/O-Bound`). Si se usa código síncrono bloqueante como `time.sleep()`, todo el bucle se paraliza.

**Inyección de Dependencias** (`Dependency Injection` — `Depends()`)  
Patrón de diseño central en FastAPI por el cual una función o endpoint no instancia ni busca directamente sus recursos externos (como una conexión a base de datos `get_db` o la validación de un usuario `get_current_profesor`), sino que el framework se los suministra automáticamente en la firma de la función. Este desacoplamiento permite inyectar dependencias simuladas o transaccionales en memoria (`sqlite:///:memory:`) durante los tests (`dependency_overrides`) sin modificar el código de producción.

**Linter**  
Herramienta de análisis de código estático que marca errores de sintaxis, estilo o malas prácticas antes de la ejecución. Ejemplo: detectar incumplimientos del PEP 8 o importaciones no usadas en `main.py` antes de commitear.

**Mock**  
Objeto o función falsa que simula el comportamiento de un componente real (frecuentemente externo) para su uso en pruebas aisladas (*Unit Tests*). Ejemplo arquitectónico: en `test_evaluation_router.py`, el `llm_client.py` actúa en modo MOCK devolviendo una respuesta prefijada (`{"calificacion_cualitativa": "NA"}`) sin gastar cuota de API real en los tests.

**Modelo (Model)**  
Representación de una entidad de negocio en el código. En el proyecto existen dos tipos: Modelos de BBDD con SQLAlchemy (`models/evaluation.py` para persistir en PostgreSQL) y Modelos de validación con Pydantic (`EvaluationRequest` para asegurar el tipado de los datos entrantes).

**Objeto (Object)**  
Una instancia concreta creada a partir de una clase. Ejemplo: `submission = Submission(id="123")` es un objeto que representa la entrega específica de un alumno en memoria, antes de ser enviada con `db.add(submission)`.

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
Cambio controlado en la estructura de la base de datos (añadir una tabla, un campo, cambiar un tipo). Alembic las gestiona y guarda el historial. Ejemplo arquitectónico: añadir la columna `estado_feed_forward` en la versión `[v0.2]`, lo cual requirió generar una nueva revisión de Alembic (`alembic upgrade head`) para evitar una pérdida total o destrucción de datos de las tablas existentes.

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

**Context Overflow (Saturación de contexto) y "Lost in the Middle" (Perdido en el medio)**  
Fenómeno y limitación arquitectónica de las redes neuronales actuales (Transformers). Ocurre cuando la *Ventana de contexto* se llena con miles de tokens de información. El mecanismo de atención de la IA (*Attention Mechanism*) tiende a priorizar la información que está al principio y al final, "olvidando" temporalmente lo del medio. Para mitigar esto, se utilizan tres estrategias principales:

1. **Prompt Anchoring (Anclaje de Prompt):** Repetir las reglas críticas justo al final del prompt.
2. **XML Tagging (Delimitadores Semánticos):** Envolver bloques de contexto entre etiquetas XML.
3. **Context Reset (Limpieza de Sesión):** Cerrar el chat cuando la memoria se llena e iniciar uno nuevo con un resumen.

**Contrato JSON (`[D-024]` / `EvaluacionIA`)**  
Acuerdo estricto de estructura y tipado definido con Pydantic v2 que transforma a los motores de Inteligencia Artificial (por naturaleza generadores probabilísticos de texto libre) en componentes deterministas de software. Al exigir la validación estricta (`Structured Outputs` / `.parse()`), se prohíbe al LLM emitir saludos, texto libre o formatos alucinados, garantizando que el backend reciba invariablemente campos tipados (calificaciones, marcadores x-y, desglose de rúbricas y `confidence_score`) listos para persistirse en PostgreSQL y mostrarse en la PWA del profesor.

**FinOps (Análisis Práctico de Coste Multimodal)**  
Evaluación financiera del consumo de tokens. Evaluar una foto de un examen manuscrito comprimida a 2048px en la PWA (`[D-020]`) consume una media de **~1.850 tokens de entrada** (~850 visuales + ~1.000 de rúbrica/prompt) y genera **~600 tokens de salida estructurada JSON Pydantic (`[D-024]`)**. En términos financieros reales:
- En fase de desarrollo con **Groq LPU (`[D-028]`)**, el coste por examen es de **0,00 €**.
- En producción usando **`GPT-4o-mini`**, corregir los exámenes diarios de un grupo de 30 alumnos cuesta **menos de 2 céntimos de euro (`~$0,019 USD / 0,018 €`)**. Esto prueba que el sistema es extremadamente rentable y sostenible.

**Generador Asistido de Rúbricas (Copiloto Pre-Corrección)**  
Funcionalidad de asistencia de api-correccion-formativa-ia-galicia (`Capa 4` relacional) por la que el docente solo necesita subir o describir el enunciado de una prueba o tarea evaluable. El motor LLM cruza automáticamente la normativa general (`Capa 1`), la programación del departamento (`Capa 2`) y el acuerdo transversal del centro (`Capa 3`) para generar una propuesta de rúbrica en 4 niveles de logro (*Insuficiente, Suficiente/Bien, Notable y Sobresaliente*). El profesor la valida con un clic en su PWA, reduciendo un 90% del tiempo burocrático de diseño de baremos. La rúbrica genera una nota numérica estricta para la tarea/examen (0-10), vinculando internamente cada criterio cuantitativo con las competencias clave que se evaluarán de forma cualitativa a final de curso.

**GPT-4o**  
Modelo de lenguaje de OpenAI. A diferencia del antiguo GPT-4 (donde existía una variante separada llamada GPT-4V o GPT-4 Vision para procesar imágenes), **GPT-4o es multimodal de fábrica**: acepta texto, imagen y audio en el mismo modelo sin necesidad de especificar ninguna variante. Esto permite enviarle directamente la foto del examen para que lo lea y evalúe contra la rúbrica.

**Jerarquía Normativa en 5 Capas Relacionales (`JSONB`)**  
Modelo arquitectónico multinivel de api-correccion-formativa-ia-galicia que desacopla y combina sin ambigüedad la legislación pública (`Capa 1: Decreto Xunta`), la programación anual del departamento (`Capa 2: Saberes y Criterios`), las normas comunes del colegio (`Capa 3: PEC/CCP`), la rúbrica de la prueba asistida (`Capa 4: El Profesor`) y las adaptaciones individuales de equidad (`Capa 5: NEAE/NEE en JSONB`).

**LLM** (Large Language Model — Modelo de Lenguaje Grande)  
Modelo de inteligencia artificial entrenado con enormes cantidades de texto. Es la IA que corrige los exámenes en este proyecto (GPT-4o o Claude).

**Modo Dual de Rúbrica (`COMBINADO` vs `AUDITORIA_CURRICULAR`)**  
Parámetro arquitectónico de interacción pedagógica (`[D-027]`, `modo_evaluacion`) que resuelve la tensión entre los criterios oficiales de la Xunta y las rúbricas ad-hoc de los docentes sin sobreingeniería en el backend. En modo `COMBINADO`, la IA fusiona los saberes de la ley con la rúbrica de la profesora para calificar entregas diarias con agilidad. En modo `AUDITORIA_CURRICULAR`, la IA corrige la tarea y adicionalmente orienta al docente contrastando su rúbrica contra los Decretos 156/157/2022, advirtiendo en `teacherSummary` de posibles omisiones competenciales.

**Multimodal / Omni-canal**  
Un modelo de IA que procesa texto, imagen y estructuras combinadas de forma simultánea (ej. GPT-4o o Claude 3.5 Sonnet). En api-correccion-formativa-ia-galicia esto permite evaluar **cualquier tipo de prueba evaluable**: no solo fotos de exámenes manuscritos o murales de cartulina de aula, sino también pruebas o entregas realizadas a ordenador (*Canva*, *Google Slides*, redacciones en Word/Docs, hojas de cálculo o cuestionarios online). En el alcance del MVP, el docente exporta o captura estas pruebas en formato digital (PDF o PNG) y las sube al sistema para que la IA las evalúe visualmente igual que un examen en papel. La importación automática y directa mediante conexión por API con plataformas externas (Google Classroom o Moodle) queda contemplada como mejora para futuras versiones post-MVP.

**OCR** (Optical Character Recognition — Reconocimiento Óptico de Caracteres)  
Tecnología integrada en la IA multimodal que extrae y convierte la caligrafía manuscrita de la foto del examen o el texto gráfico de un mural/cartulina en datos legibles para evaluarlos contra la rúbrica.

**Prompt**  
El texto de instrucciones que se envía al modelo de IA. Se divide en dos partes con roles distintos:

- **`system prompt` (instrucción de rol):** Define quién es la IA y cómo debe comportarse en todas sus respuestas. En este proyecto: *"Eres un evaluador formativo experto en Filosofía de Bachillerato del sistema educativo gallego (Decreto 157/2022, Xunta de Galicia). Devuelves ÚNICAMENTE JSON estructurado con el esquema EvaluacionIA. Jamás diagnosticas condiciones médicas ni educativas."* — establece el rol, el idioma, las restricciones legales y el contrato de salida.
- **`user prompt` (la tarea concreta):** Contiene los datos variables de cada corrección: la respuesta del alumno, la rúbrica de la profesora, el marco normativo y las adaptaciones NEAE. Cambia en cada petición.

El `prompt_builder.py` construye dinámicamente el `user prompt` combinando estos datos. El `system prompt` permanece constante en todas las correcciones.

**Prueba evaluable (Instrumento de evaluación)**  
Cualquier evidencia de aprendizaje del alumno sometida a corrección formativa. En api-correccion-formativa-ia-galicia abarca los 3 formatos del aula moderna: papel manuscrito (foto), creación plástica/visual (foto de mural o cartulina) y entregas digitales (redacciones online o exportaciones PDF/PNG de presentaciones de Canva).

**Simetría Lingüística (Bilingüismo co-oficial / Espejo lingüístico)**  
Directriz imperativa de diseño pedagógico (`[D-036]`, `Regla 7` en `SYSTEM_PROMPT`) en sistemas educativos de comunidades con lengua co-oficial (como Galicia). Ordena al motor LLM detectar de forma automática el idioma vehicular (gallego normativo o castellano) en el que esté redactada la respuesta o prueba evaluable del alumno, y formular el 100% de los campos cualitativos de retorno (`reasoning`, `teacherSummary` y `siguiente_paso_accionable`) exactamente en ese mismo idioma. Evita que la IA responda por defecto en castellano ante entregas en gallego, sin exigir que la profesora seleccione interruptores manuales en la interfaz.

**Structured Outputs** (Salidas Estructuradas)  
Mecanismo que fuerza al modelo de IA a devolver siempre un JSON con un esquema fijo, en lugar de responder en texto libre. Explicado en detalle en `sesion_02_storage_y_structured_outputs.md`.

**Token** (en contexto de IA)  
La unidad mínima de texto que procesa un modelo de lenguaje. Aproximadamente `1 token ≈ 0,75 palabras` en español (o 4 caracteres en inglés). Los modelos cobran por tokens consumidos en ambas direcciones:

| Motor | Precio input | Precio output | Contexto máximo |
|---|---|---|---|
| `Groq llama-3.3-70b` | **Gratuito** (cota) | **Gratuito** (cota) | 128.000 tokens |
| `GPT-4o` | ~$2,50 / M tokens | ~$10 / M tokens | 128.000 tokens |
| `Claude Sonnet` | ~$3 / M tokens | ~$15 / M tokens | 200.000 tokens |

**En este proyecto:** Groq es el motor primario (`[D-028]`) precisamente porque su cota gratuita permite desarrollar y demostrar el sistema sin coste, con inferencia ultrarrápida.

**Ventana de Contexto (`Context Window`)**  
El límite máximo de tokens que el modelo puede leer de una vez (prompt + respuesta juntos). Si un examen escaneado con mucho texto supera ese límite, el modelo falla — por eso en `[D-020]` se comprime la imagen en la PWA antes de enviarla.

**Workload Routing (Enrutamiento de Cargas)**  
Estrategia arquitectónica (`[D-051]`) por la que el sistema decide dinámicamente qué proveedor de Inteligencia Artificial (ej. OpenAI vs. Groq) debe procesar una petición en función de la naturaleza de la carga de trabajo. En api-correccion-formativa-ia-galicia, las peticiones que contienen imágenes (Visión) se dirigen a OpenAI para aprovechar la fiabilidad de sus *Structured Outputs*, mientras que las peticiones de texto plano se enrutan a Groq para maximizar la velocidad y reducir el coste.

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
Una línea de desarrollo paralela en Git. Permite trabajar en una funcionalidad nueva o hacer pruebas sin romper el código principal. En este proyecto utilizamos ramas temporales (ej. `feature/nueva-funcion`) que, una vez terminadas y validadas, se fusionan (`merge`) con la rama `main` y se eliminan para mantener el repositorio limpio.

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

**Patrón Showcase (Showcase Pattern)**  
Estrategia de gobernanza de repositorio (`[D-062]`) diseñada para proteger la propiedad intelectual o el "secreto comercial" de un proyecto (como los prompts de IA y configuraciones exclusivas) mientras se exhibe públicamente toda la infraestructura, arquitectura y base de código. Se implementa utilizando el `.gitignore` para cegar a Git ante los archivos críticos (ej. `prompt_builder.py`, `llm_client.py`), permitiendo que el resto del sistema (modelos relacionales, migraciones de base de datos, frontend PWA) sea visible para auditores y reclutadores, demostrando excelencia técnica ("Build in Public") sin regalar el negocio.

**.gitignore**  

Archivo que le dice a Git qué archivos ignorar y no incluir en el repositorio. Los archivos con claves de API (`.env`), dependencias (`venv/`) y cachés (`__pycache__/`) nunca deben subirse.

**Push**  
Subir los commits locales al repositorio remoto en GitHub.

**Repositorio**  
El proyecto completo gestionado por Git, incluyendo todos los archivos y su historial de cambios.

**Scope (Ámbito del commit)**  
En la convención de `Conventional Commits` de este proyecto, es el texto entre paréntesis que indica qué parte del sistema se ha modificado, garantizando la trazabilidad. Ejemplo: `docs(audit)` indica una actualización en la documentación por auditoría; `test(api)` señala un cambio en los tests del backend.

---

## 8. Herramientas de desarrollo con IA

**AGENTS.md**  
Archivo de texto en la raíz del proyecto que los agentes de IA (como Antigravity, OpenCode o Cursor) leen automáticamente al arrancar para inyectarlo en su `System Prompt`. Contiene el contexto del proyecto (arquitectura, convenciones, reglas) para que el agente trabaje con información actualizada sin tener que explicárselo cada vez.

**Agentic Coding (Codificación Agentic)**  
Paradigma avanzado de desarrollo de software donde la Inteligencia Artificial no actúa como un mero autocompletado pasivo, sino como un agente autónomo. Un agente es capaz de leer múltiples archivos simultáneamente, razonar sobre la arquitectura del proyecto, ejecutar comandos en terminal y aplicar parches de código complejos de forma proactiva, actuando como un copiloto de alto nivel.

**AI-Augmented Engineering (Ingeniería Aumentada por IA)**  
Modelo de trabajo y perfil profesional de la nueva era del desarrollo. En lugar de escribir cada línea de código a mano, la desarrolladora (orquestadora) se apoya en agentes de IA para eliminar tareas repetitivas (*boilerplate*) y acelerar la implementación. El humano dirige la estrategia, valida las decisiones arquitectónicas, garantiza el cumplimiento normativo y aprueba el resultado final, multiplicando drásticamente su productividad.

**Antigravity**  
El agente de IA integrado en VS Code (este). Se usa para arquitectura, decisiones de diseño, revisiones críticas y documentación. Consume cuota de Claude Sonnet.

**Diversificación de Tokens (Token Multiplexing)**  
Estrategia de finanzas operativas (*FinOps*) orientada a maximizar la productividad y esquivar límites de cuota gratuita sin sobrecostes. Consiste en combinar múltiples entornos de IA en paralelo (ej. Antigravity en VS Code para arquitectura global + Warp AI Agent en terminal independiente para comandos/DevOps + Groq LPU en el backend), repartiendo la carga de trabajo entre diversos motores y modelos.

**Gemini**  

Familia de modelos de lenguaje de Google. El modelo `gemini-2.5-flash` es el predeterminado en OpenCode por su cota gratuita generosa (1.500 peticiones/día).

**Groq**  
Proveedor de modelos de lenguaje con cuota gratuita muy generosa y velocidad de inferencia muy alta. Se usa en OpenCode para tareas de código complejo (`llama-3.3-70b-versatile`, `qwen3-32b`).

**Jest / Vitest (Frameworks de Testing Frontend)**  
Herramientas de testing unitario para JavaScript/TypeScript. **Jest** es el estándar clásico del ecosistema React (creado por Meta). **Vitest** es su alternativa moderna optimizada para proyectos con Vite, con sintaxis idéntica pero arranque mucho más rápido. En api-correccion-formativa-ia-galicia: los tests de la función `cropHeader()` (`[v0.3-001]`) se escribirán en Vitest por su integración nativa con el stack Vite + React de la PWA. Los tests de backend (Python) usan pytest; los tests de frontend (JS) usan Vitest — cada stack tiene su herramienta propia.

**OpenCode**  
Agente de IA que se ejecuta en la terminal de WSL. Lee y edita archivos directamente, ejecuta comandos, y trabaja dentro del mismo entorno donde corre Python/FastAPI. Se usa para código rutinario, boilerplate y edición de archivos.

**PonyTail**  
Conjunto de reglas que se añade al `AGENTS.md` para que OpenCode siga el principio de mínimo código: antes de escribir algo, comprueba si ya existe una solución más simple. Reduce el consumo de tokens en ~22%.

**State-of-the-Art (SOTA)**  
Término técnico que define el nivel más alto y avanzado de desarrollo alcanzado en un momento particular en cualquier campo (la "tecnología punta"). En el contexto del proyecto, usar herramientas como Antigravity o modelos como GPT-4o-mini demuestra adopción de flujos de trabajo SOTA en lugar de prácticas de desarrollo tradicionales y obsoletas.

**WSL** (Windows Subsystem for Linux — Subsistema de Windows para Linux)  
Capa de compatibilidad que permite ejecutar un sistema Linux (Ubuntu) dentro de Windows. Todo el código Python/FastAPI del proyecto corre en WSL porque el ecosistema de herramientas de desarrollo es más estable en Linux.

---

## 9. Legal y normativo

**Adaptaciones Curriculares (ACS / ACNS / DEA)**  
Medidas de modificación o ajuste pedagógico reguladas por la legislación (LOMLOE, Decreto 229/2011 de Galicia) para garantizar la equidad educativa del alumnado. Pueden ser ordinarias o no significativas (ACNS, ej: dislexia, TDAH) sin alterar objetivos, o significativas (ACS) cuando modifican el currículo oficial. En api-correccion-formativa-ia-galicia se inyectan mediante el campo `adaptaciones_alumno` ([D-023]) para separar faltas ortográficas del cálculo penalizador de nota.

**AI Act** (Reglamento Europeo de Inteligencia Artificial)  
La primera ley de la Unión Europea que regula los sistemas de IA. Clasifica los sistemas por nivel de riesgo. api-correccion-formativa-ia-galicia entra en la categoría de alto riesgo (afecta a educación de menores y procesa variables de necesidades específicas), por lo que requiere Human-in-the-Loop y trazabilidad completa.

**Compliance (Cumplimiento Normativo)**  
Es la disciplina que garantiza que una empresa o software opera respetando estrictamente el marco legal y regulatorio de su sector. En ingeniería de software, aplicar *Compliance* significa que el código está diseñado para cumplir la ley por defecto (por ejemplo, implementar la técnica *Zero Data Retention* para cumplir con el RGPD y la *AI Act*, o codificar fórmulas matemáticas que respeten la LOMLOE).

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

**Legal Ops (Legal Operations / Operaciones Legales)**  
Campo interdisciplinar híbrido entre el derecho, la tecnología y la ingeniería de procesos. Su objetivo es aplicar metodologías del desarrollo de software (estandarización, flujos medibles, automatización y métricas) a los departamentos o problemas legales. Busca transformar los requisitos normativos en sistemas controlados, medibles y escalables dentro de la operativa, garantizando gobernanza técnica sin frenar el crecimiento o despliegue del proyecto.

**NEAE / NEE** (Necesidades Específicas de Apoyo Educativo / Necesidades Educativas Especiales)  
Clasificación legal en España para el alumnado que requiere una atención educativa diferente a la ordinaria por presentar dificultades específicas de aprendizaje (DEA como dislexia), TDAH, altas capacidades o discapacidad (NEE). api-correccion-formativa-ia-galicia adapta su motor formativo para que estos perfiles sean evaluados con justicia sin penalizar errores derivados de su condición ([D-023]).

**Privacy by Design** (Privacidad desde el Diseño)  
Enfoque de ingeniería de software que exige integrar la protección de datos desde la fase inicial de arquitectura del sistema, y no como un parche a posteriori (mandato del Art. 25 del RGPD). En este proyecto se materializa en medidas proactivas como la anonimización local en el navegador del docente (antes del envío a la nube) y la creación de plantillas físicas de examen con fronteras de recorte (`[v0.5-007]`) para evitar que el nombre del alumno se envíe a la IA.


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

**Competencia clave**  
Capacidad o destreza fundamental (ej. CCL, STEM) que se evalúa a lo largo del curso en todas las asignaturas. Según la LOMLOE se expresan en términos cualitativos y definen el Perfil de salida del alumno.

**Criterio de evaluación**  
Referente único y oficial de calificación según la LOMLOE. Evalúa el desempeño específico del alumno en una prueba o materia y es la base ineludible sobre la que se construye cualquier rúbrica o ponderación (`[D-040]`).

**Descriptor operativo**  
Concreción de la competencia clave y punto de unión o anclaje normativo con los criterios de evaluación de cada materia específica.

**Distinción LEY vs. CONFIGURACIÓN DE CENTRO**  
Principio rector de calificación (`[D-040]`) que exige separar estrictamente las obligaciones legales impuestas por los Decretos (ej. escalas 1-10 o referentes criteriales) de las decisiones pedagógicas internas de cada departamento escolar (ej. si se usan decimales, qué peso tiene cada criterio o si se hace media ponderada). Previene que el agente LLM invente reglas o presente configuraciones locales como mandatos autonómicos.

**Comparative Judgement / Juicio Comparativo**  
Metodología pedagógica innovadora (ej. *No More Marking* en Reino Unido) donde se evalúa el razonamiento cualitativo global en lugar de contar puntos mecánicos aislados (`[D-024]`).

**Doble Circuito de Calificación (Materias vs. Competencias Clave)**  
Modelo operativo dual vigente en los IES gallegos (Decretos 156/157/2022) y reflejado en XADE/api-correccion-formativa-ia-galicia: 1) **Circuito de Materias:** Las asignaturas se califican y cierran en los boletines trimestrales y ordinarios con **números enteros del 1 al 10** derivados de las notas cotidianas numéricas de las pruebas evaluables. 2) **Circuito de Competencias Clave:** Las 8 competencias oficiales (*CCL, STEM, CD...*) se califican al final del curso de forma cualitativa (*IN, SU, BE, NT, SB*) mediante el **cruce e intersección matricial inter-materias** de todos los criterios evaluados en las diferentes asignaturas del alumno.

**Deuda Técnica (`Technical Debt` / Deuda Consciente)**  
Coste estratégico de ingeniería que se asume al aplazar o simplificar deliberadamente una implementación en la fase actual para priorizar la entrega rápida y limpia de un hito, con el compromiso explícito de refactorizarla o completarla en una iteración posterior. En api-correccion-formativa-ia-galicia, un ejemplo es no persistir aún los binarios de subida en la tabla `Submission` durante `[v0.3-001]` porque dicha lógica se rediseñará integralmente al introducir la función `cropHeader()` en `frontend/src/utils/imageCrop.js` (`[v0.3-002]`) — el recorte ocurre en el cliente, nunca en el servidor Python (*YAGNI*, `[D-022]`, `[D-034]`).

**Equipotencialidad Criterial (`Decreto 156/157/2022`)**  
Regla pedagógica general y por defecto por la que todos los Criterios de Evaluación (`criterio_id`) asociados a las competencias específicas de una materia tienen idéntico valor o peso en el cálculo de la nota final, salvo que el departamento establezca porcentajes diferenciados en su Programación Didáctica (`Capa 2`).

**Etapa (ESO/BACH)**  
Nivel educativo que determina legalmente la escala cualitativa aplicable (`[D-041]`). En ESO es el dato oficial fuerte (`IN, SU, BE, NT, SB`), mientras que en Bachillerato la calificación oficial es numérica entera y el campo `calificacion_cualitativa` es `null` — no existe escala cualitativa oficial en BACH (`[D-049]`).

**Evaluación Competencial Cualitativa (`Decretos 156/157/2022 Galicia`)**  
Modelo evaluativo obligatorio en Galicia para ESO y Bachillerato centrado en el grado de adquisición de las competencias clave y específicas del currículo, expresado en grados cualitativos (*Insuficiente [IN], Suficiente [SU], Bien [BE], Notable [NT], Sobresaliente [SB]*) además o en lugar de la nota numérica simple (`[D-024]`).

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

**Audit Trail (Trazabilidad e Historial de Auditoría en GitHub)**  
Registro temporal, inmutable y verificable de todas las actividades de ingeniería, inspección técnica y decisiones tomadas a lo largo de un proyecto. En api-correccion-formativa-ia-galicia se manifiesta tanto en el código (`ChangeLog` en BBDD para cumplir con el *AI Act*) como en la gestión institucional del repositorio (`[D-035]`): cerrar una Issue formal de auditoría hoy (`[QA/Audit] Verificación Transversal v0.0 a v0.2.7 y Matriz AUDITORIA.md`) deja una huella probatoria en la pestaña `Closed` de GitHub ante mentores y evaluadores de que el equipo revisó y validó el sistema antes de iniciar el código de un nuevo hito.

**Backlog**  
Lista priorizada de todo el trabajo pendiente del proyecto, organizado en historias de usuario. En este proyecto: `backlog.md`.

**Criterios de aceptación**  
Lista de condiciones concretas y verificables que deben cumplirse para considerar una historia de usuario terminada. Sin criterios claros, no hay forma de saber cuándo algo está "listo".

**Epic Issue (Épica como Issue / Modelo de Épica)**  
Metodología de organización ágil y de repositorio donde cada gran bloque funcional o iteración de versión (`Versión 0.1`, `Milestone v0.2.5`, `Versión 0.3`) se abre en GitHub como una única gran **Issue madre** que contiene en su cuerpo el checklist de todas sus historias de usuario (`- [ ]`). Este modelo simplifica radicalmente la gestión para equipos ágiles HitL, evitando la dispersión en decenas de micro-issues y mostrando el progreso del hito de forma centralizada.

**Gobernanza (Governance)**  
Conjunto de normas, prácticas y convenciones que aseguran que el proyecto se desarrolle de manera estructurada, auditable y segura. Ejemplo en el proyecto: la decisión `[D-035]` y las reglas estrictas de `AGENTS.md` (como el "Stop & Consult") que blindan el repositorio aislando la revisión de la implementación y manteniendo actualizados los documentos maestros (`decisiones.md`, `backlog.md`).

**Historia de usuario**  
Forma de describir una funcionalidad desde el punto de vista del usuario final. Formato: "Como [rol], quiero [acción], para [beneficio]". Es la unidad de trabajo del backlog.

**Issue (Tarea / Incidencia en GitHub)**  
Unidad de seguimiento, trabajo o reporte en GitHub. En nuestra arquitectura y jerarquía, una Issue representa una **tarea ejecutada por el equipo**: puede ser una tarea de desarrollo de software (`#8 [Milestone v0.2.5] Migraciones y HitL`), una tarea de inspección y gobernanza (`#9 [Auditoría de Gobernanza] Matriz AUDITORIA.md`) o un reporte de bug. Las Issues operan dentro de los Milestones y se marcan con casillas interactivas (`- [x]`) hasta cerrarse (`Closed`).

**Milestone (Hito / Contenedor de Versión en GitHub)**  
Punto de referencia y contenedor jerárquico superior en el roadmap del proyecto. En GitHub Projects y en api-correccion-formativa-ia-galicia equivale a una versión o entregable de software (`v0.1 Motor Síncrono`, `v0.2 Base de Datos`, `v0.2.5 Consolidación HitL`). Un Milestone agrupa las Issues correspondientes a esa versión y permanece abierto (`Open`) hasta que todas las tareas y auditorías de ese bloque se han completado.

**Media ponderada**  
Método de cálculo determinista implementado en el backend (`[D-043]`) donde la nota de la prueba es el resultado de normalizar cada criterio evaluado y multiplicarlo por su peso departamental, sumando un 100%. Garantiza que la aritmética quede fuera del alcance probabilístico del modelo de lenguaje.

**Nivel de logro**  
Escala de calidad (frecuentemente 1 a 4) empleada en la rúbrica de centro/departamento para categorizar el desempeño del alumno en cada criterio de evaluación. Es una decisión de configuración de centro, no una imposición del decreto.

**Perfil de salida**  
Grado final esperado de adquisición de las competencias clave que el alumno debe haber logrado al término de su etapa educativa básica para asegurar su desarrollo personal y social.

**Separation of Concerns (Separación de Responsabilidades en Gobernanza `[D-035]`)**  
Principio fundamental de ingeniería que dicta que cada aspecto, problema o capa de un sistema debe gestionarse en un módulo o actividad independiente. En el plano de gobernanza del proyecto, separa de manera estricta las actividades de **Inspección y Auditoría Técnica** (ej. contrastar código existente contra normativas y generar `AUDITORIA.md`) de las actividades de **Implementación y Programación de Código** (ej. escribir endpoints y migraciones). Al abrir y cerrar tareas (`Issues`) separadas para cada responsabilidad, se garantiza que la calidad y el blindaje legal no se diluyan en la rutina del picado de código.

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

**Batching (Procesamiento por Lotes / Agrupación de Tareas)**  
Técnica de optimización utilizada tanto en arquitectura de software como en gestión de productividad:
- **En backend y bases de datos**: Consiste en agrupar múltiples peticiones, inserciones o llamadas I/O pequeñas en un único lote de procesamiento (ej. inserciones masivas en SQL o evaluación en lote de folios de un examen) para reducir la sobrecarga de red (*overhead*), el número de transacciones abiertas y optimizar el rendimiento.
- **En metodología y gestión del tiempo**: Práctica de agrupar tareas homogéneas (como responder comentarios de LinkedIn, revisar Pull Requests o redactar documentación) en bloques de tiempo fijos y delimitados del día, evitando la fragmentación de la atención por interrupciones continuas y garantizando un ritmo de trabajo sostenible.

**Atomic Commits (Commits Atómicos y Granularidad de Commits)**  
Práctica fundamental de control de versiones por la cual cada commit en Git representa una única unidad lógica de trabajo completa, independiente y con sentido propio (ej. la implementación de un endpoint asíncrono o la resolución de un fallo). Evita tanto los *mega-commits* que mezclan características inconexas como los *micro-commits* ruidosos que ensucian el historial con cambios insignificantes. Las pequeñas adiciones de soporte o glosario se empaquetan de forma natural dentro del commit funcional correspondiente.

**Agile Product Backlog Management (Gestión Ágil del Backlog de Producto)**  
Práctica de metodologías ágiles (Scrum/Kanban) consistente en recopilar, priorizar y categorizar continuamente todas las historias de usuario, funcionalidades deseables, refactorizaciones y deuda técnica en un documento o lista viva (*Product Backlog*). Permite aplicar estrictamente el principio YAGNI y controlar el alcance (*Scope Creep*) en el sprint actual: en lugar de implementar ideas tentadoras al vuelo (*"ya que estoy..."*), se registran ordenadamente en el backlog asignadas a iteraciones o versiones futuras (`v0.5`, `v0.8`, `Roadmap`), protegiendo el foco presente sin perder ideas de valor.

**Scope Creep (Crecimiento Incontrolado del Alcance / Desviación del Alcance)**  
Fenómeno en gestión de proyectos de software por el cual los requisitos y funcionalidades de un proyecto aumentan de manera continua, sutil e incontrolada durante el desarrollo (*"ya que estoy, añado esto también"*), sin reajustar los plazos, el presupuesto o los recursos. Si no se frena mediante el principio YAGNI y una gestión rigurosa del backlog (*Product Backlog Management*), el Scope Creep provoca retrasos sistemáticos, agotamiento (*burnout*) y el abandono del proyecto antes de llegar a producción.

**Scaffolding (Andamiaje Cognitivo / Andamio Mental)**  
Concepto procedente de la psicología educativa (Vygotsky / Bruner) e integrado en la ingeniería de software: consiste en la creación de estructuras de soporte temporales o guías deliberadas (como registros de decisiones de arquitectura ADRs, listas de comprobación o reglas de orquestación en `AGENTS.md`) que permiten a un desarrollador abordar tareas complejas y tomar decisiones de diseño rigurosas mientras desarrolla y consolida su dominio técnico.

**Architectural Integrity (Integridad Arquitectónica / Coherencia del Sistema)**  
Grado de fidelidad y consistencia con el que la arquitectura de un sistema de software respeta sus principios de diseño originales (como YAGNI, el flujo Human-in-the-Loop o la Privacidad por Diseño) a lo largo del tiempo. Previene que el código se degrade con parches improvisados a medida que el proyecto crece o evoluciona entre distintas versiones.

**Desacuerdo Controlado (Adversarial Multi-LLM Review)**  
Metodología de auditoría de código y diseño creada por Nicolás Rocchia (Pelatech / `disensor.dev`) basada en utilizar dos asistentes de IA de proveedores distintos de forma explícitamente adversarial: un modelo A genera el plan o la implementación, y un modelo B (de otro proveedor) ataca buscando agujeros de seguridad, concurrencia o edge cases. La revisión nunca se cierra por consenso automático, sino por verificación explícita de evidencia o por transferencia del hallazgo como residuo/deuda al desarrollador humano (*Human-in-the-Loop*).

**Declaración de Residuo (Residue Declaration / Audit Residue)**  
Registro versionado, explícito y auditable de aquellas incertidumbres, ambigüedades o casos de borde de una evaluación/revisión que la IA no puede o no debe resolver de forma autónoma. En lugar de forzar una decisión automatizada ficticia o mostrar un aprobado en piloto automático, el sistema encapsula estos puntos en un "residuo" formal que se transfiere a la firma y responsabilidad consciente del profesional humano (*Human-in-the-Loop*).

**Prueba de los 6 Meses (6-Month Maintainability Rule)**  
Principio de gobernanza y mantenibilidad de software recomendado por Fernando (Quantia): establece que toda decisión de arquitectura, mensaje de commit e historial de issue debe documentarse con tal nivel de claridad y contexto que cualquier desarrollador —o tu propio "yo del futuro"— seis meses después comprenda exactamente la razón de ser del código y mantenga el 100% de la fidelidad a la filosofía del proyecto sin degradarlo.

**Métricas Cosméticas (Vanity Metrics / Badges Cosméticos)**  
Indicadores de rendimiento o cobertura que lucen positivos en un panel de control (como un badge verde de 100% de revisión o métricas de aprobados masivos sin aserciones profundas), pero que enmascaran fallos de lógica, alucinaciones o falta de responsabilidad real en la toma de decisiones.

**Code Freeze (Congelación de Código)**  





Periodo de bloqueo temporal en el que no está permitido añadir código nuevo al repositorio ni iniciar nuevas funcionalidades, con el objetivo de garantizar la estabilidad del sistema antes de un evento crítico (demo, auditoría, lanzamiento, reunión de revisión). Solo están permitidas correcciones de errores graves y actualizaciones de documentación. En este proyecto: el code freeze arranca el sábado 25/07/2026 y se mantiene hasta después de la revisión técnica del lunes 27/07.

**CI/CD (Continuous Integration / Continuous Deployment — Integración y Despliegue Continuos)**  
Práctica de ingeniería de software que automatiza la verificación y publicación del código. Cada vez que se suben cambios al repositorio en GitHub:
- **CI (Integración Continua)**: Un robot automatizado en la nube clona el proyecto, instala dependencias, levanta la base de datos de prueba en Docker, aplica las migraciones de Alembic (`alembic upgrade head`) y ejecuta la suite de pruebas (`pytest`). Si algún test falla, el cambio se rechaza automáticamente y bloquea la integración.
- **CD (Despliegue Continuo)**: Si todas las pruebas dan verde, el sistema actualiza automáticamente el servidor en producción sin requerir intervención manual.

**Definition of Done / DoD (Definición de Hecho)**  

Conjunto de criterios mínimos que una historia de usuario, tarea o funcionalidad debe cumplir para considerarse **verdaderamente terminada** — no solo "funciona en mi máquina". En api-correccion-formativa-ia-galicia el DoD está formalizado como los **4 pilares de `[D-035]`**: Diseño (ADR en `decisiones.md`), Implementación (código en `main`), Evidencia (`pytest` en verde) y Documentación (`README.md` + `backlog.md` sincronizados). En la Epic Issue de GitHub, los checkboxes representan el DoD público de la épica — se marcan solo cuando el código existe, los tests pasan y la documentación está actualizada.

**Estrategia Dual de Testing (Dual Testing Strategy)**  
Estrategia de arquitectura de pruebas (`[D-056]`) que combina dos capas complementarias de testing:
- **Capa 1 (Unitarios TDD)**: Ejecución ultra-rápida (<4s) utilizando SQLite en memoria RAM (`sqlite:///:memory:`) para el desarrollo diario, permitiendo refactorizar e iterar sin necesidad de depender de contenedores ni contaminar los datos locales del desarrollador.
- **Capa 2 (Integración CI/CD)**: Ejecución automatizada en la v0.5 (`[v0.5-007]`) utilizando un esquema/contenedor vaciado de PostgreSQL 16 Alpine en Docker. Esta capa ejecuta las migraciones reales de Alembic (`alembic upgrade head`) para validar la sintaxis DDL y el comportamiento estricto de tipos de datos avanzados (`JSONB`).

**GitHub Actions**  
Plataforma de automatización y CI/CD integrada directamente en GitHub. Mediante archivos de configuración YAML (ubicados en `.github/workflows/`), permite definir flujos de trabajo (*workflows*) que se disparan ante eventos del repositorio (como un `git push` o un `Pull Request`), ejecutando tests automatizados en contenedores Docker y desplegando la API sin intervención manual.

**Proof of Concept / PoC (Prueba de Concepto)**  


Implementación mínima, exploratoria y desechable cuyo único objetivo es validar la viabilidad técnica o matemática de una idea **antes** de comprometer esfuerzo de arquitectura o código de producción. Un PoC no es un servicio definitivo ni forma parte del backend. En este proyecto: `scratch/pillow_crop_test.py` fue un PoC del algoritmo de recorte (ratio 0.20, 794×1123px → 224+899px) para confirmar la matemática antes de portarla a JavaScript/Canvas en el frontend PWA (`[v0.3-001]`). El script vive en `scratch/` (ignorado por git) precisamente por su naturaleza exploratoria transitoria.

**Self-Review Gate (Auto-Revisión Pre-Entrega)**  
Checkpoint de calidad de comunicación formalizado como `Regla 7 de AGENTS.md`. Exige que el agente, antes de entregar cualquier salida extensa (+150 palabras) o documento destinado a otro agente o tercero, ejecute una segunda pasada completa de revisión verificando: frases inconclusas, fechas/IDs/referencias erróneas, contradicciones con `decisiones.md` y residuos del razonamiento intermedio. Complementa al Protocolo Stop & Consult (`[D-029]`, Regla 5): mientras D-029 frena antes de parchear código, el Self-Review Gate frena antes de entregar texto. Motivado por la detección real del error "794×898px" (correcto: 899px) en la Issue #14 durante la sesión del 24/07/2026.



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

**Trust, but verify (Confía, pero verifica)**  
Regla de oro fundamental en ciberseguridad, auditoría e ingeniería con Inteligencia Artificial. Consiste en el principio de no asumir nunca que un proceso automatizado (como un despliegue CI/CD, una integración de git, o la respuesta de un Agente IA autónomo) es correcto por defecto sin someterlo a comprobación empírica. Implica validar siempre mediante revisión de código, inspección del árbol de archivos o pruebas de caja blanca para garantizar la integridad y soberanía de los datos antes de pasar a producción.

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

**Por qué importa ante la Auditoría:**
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
Modelo de negocio en el que el software se ofrece como servicio (generalmente por suscripción o pago por uso) alojado en la nube, sin que el cliente tenga que instalarlo ni mantener la infraestructura. En estrategias *Build in Public*, obliga a proteger el repositorio (mediante licencia Propietaria o AGPLv3 "SaaS defensivo") para evitar que competidores clonen la plataforma y la comercialicen libremente. La PWA de api-correccion-formativa-ia-galicia se proyecta como un SaaS donde tú controlas la infraestructura y los colegios acceden al servicio.

**GPL (General Public License) / Copyleft Fuerte**  
Tipo de licencia de software libre de naturaleza "vírica". Obliga legalmente a que cualquier software que utilice o se enlace con un componente GPL sea distribuido, a su vez, bajo la misma licencia abierta. Su uso está estrictamente prohibido en el ecosistema de este proyecto (`Zero-GPL`) para proteger la viabilidad comercial y el modelo cerrado del SaaS.

**AGPL (Affero General Public License)**  
Variante aún más estricta de la GPL diseñada específicamente para aplicaciones web y servicios en la nube (SaaS). Exige que cualquier persona que ofrezca el software como un servicio a través de una red (sin siquiera distribuirlo físicamente) debe facilitar el código fuente completo a los usuarios de dicho servicio. Suele usarse por empresas comerciales como licencia "SaaS defensiva" para obligar a competidores a pagar por licencias privadas.

**LGPL (Lesser General Public License)**  
Variante de la GPL más "débil" que permite enlazar dinámicamente el código en aplicaciones propietarias sin obligar a abrir el código fuente del programa principal. Aunque técnicamente es segura para uso comercial, en este proyecto se audita manualmente o se evita por extrema precaución.

**Licencias Permisivas (MIT, Apache 2.0, BSD, ISC)**  
Familias de licencias de código abierto que permiten a los desarrolladores usar, modificar, distribuir y comercializar el software, incluso en productos cerrados o propietarios, sin obligarles a liberar su propio código fuente. Son las únicas dependencias autorizadas por defecto en este proyecto.

**CLA (Contributor License Agreement)**  
Acuerdo de Licencia de Colaborador. Documento legal que un desarrollador externo debe aceptar al enviar código (*Pull Request*) a un repositorio. Garantiza que el creador transfiere los derechos comerciales y de propiedad intelectual a la titular principal, blindando legalmente el repositorio frente a futuras demandas por derechos de autor.
**Pytest**  
Framework de automatización de pruebas para el lenguaje Python. Permite escribir pequeños programas (tests o pruebas unitarias) que comprueban automáticamente si el resto del código del proyecto funciona correctamente. En este proyecto se utiliza ejecutando `pytest -v` para certificar que ningún cambio arquitectónico rompa las reglas de negocio, garantizando siempre que los tests estén "en verde" (pasados) antes de cerrar una funcionalidad.

**Swagger (Swagger UI)**  
Interfaz web autogenerada e interactiva que permite visualizar, documentar y probar directamente los endpoints (rutas) de una API sin necesidad de escribir código. En FastAPI, Swagger viene integrado por defecto y se accede normalmente añadiendo `/docs` al final de la dirección local (ej. `http://localhost:8000/docs`). Facilita enormes ventajas para presentar el funcionamiento real del sistema a evaluadores o clientes de forma gráfica.

**LPU (Language Processing Unit)**  
Unidad de Procesamiento de Lenguaje. Es un tipo de microchip especializado diseñado por la empresa Groq exclusivamente para la inferencia (ejecución) de Modelos de Lenguaje Grande (LLMs) como Llama 3. A diferencia de las GPUs (Tarjetas Gráficas) que procesan cosas en paralelo, las LPUs están optimizadas para el procesamiento secuencial rapidísimo de texto, lo que permite alcanzar velocidades de respuesta de más de 800 tokens por segundo (casi instantáneo), siendo ideales para sistemas que requieren corrección formativa en tiempo real.

**GPU (Graphics Processing Unit)**  
Unidad de Procesamiento Gráfico (comúnmente conocida como Tarjeta Gráfica, como las de NVIDIA). Tradicionalmente diseñadas para videojuegos y renderizado 3D por su increíble capacidad para realizar miles de cálculos matemáticos en paralelo al mismo tiempo. Han sido el estándar para entrenar y ejecutar Inteligencia Artificial (como ChatGPT), pero presentan cuellos de botella al generar texto secuencial, siendo menos eficientes para inferencia conversacional que chips especializados como las LPUs.

**RAG (Retrieval-Augmented Generation)**  
Técnica que consiste en "recuperar" información externa y pasársela a un modelo de IA para que genere una respuesta basada en esos datos exactos, evitando alucinaciones o invenciones.  
*En el mercado:* Se suele usar RAG Semántico (bases de datos vectoriales que buscan textos "parecidos", lo que puede introducir ruido).  
*En api-correccion-formativa-ia-galicia:* Implementamos **RAG Determinista o Relacional**. En lugar de búsquedas semánticas borrosas, recuperamos la rúbrica exacta del docente y el marco legal LOMLOE mediante consultas SQL precisas a nuestra base de datos PostgreSQL (`rubrica_id`, `marco_id`). Estos datos estructurados se inyectan dinámicamente en el *prompt* de Groq, forzando a la IA a evaluar al alumno basándose al 100% en la legalidad y los criterios vigentes sin margen de error en la recuperación del contexto.

**Base de Datos Vectorial (Vector Database)**  
Tipo especializado de base de datos (como ChromaDB, Pinecone o Weaviate) diseñada para almacenar datos como "vectores matemáticos" (embeddings). En lugar de buscar palabras exactas o IDs como hace PostgreSQL, busca "conceptos matemáticos parecidos" en un espacio multidimensional. Son la pieza central del RAG Semántico tradicional, muy útiles para chatbots que buscan en miles de PDFs, pero menos precisas que una base de datos relacional (SQL) cuando necesitas inyectar un contrato o ley exacta sin riesgo de desviación.

**MCP (Model Context Protocol)**  
Estándar abierto de arquitectura de comunicación diseñado para conectar modelos de Inteligencia Artificial (LLMs y Agentes) con herramientas externas, fuentes de datos y APIs de forma segura, mediante esquemas estandarizados en JSON-RPC. Funciona como un "enchufe universal": en lugar de crear conectores ad-hoc para cada servicio, un servidor MCP expone datos o funciones (como consultar rúbricas o validar notas) a cualquier cliente de IA manteniendo tipos estrictos y aislamiento de seguridad.

**TrOCR (Transformer OCR)**  
Modelo de reconocimiento óptico de caracteres desarrollado por Microsoft basado en arquitectura Transformer end-to-end (`VisionEncoderDecoder`). A diferencia de los motores OCR clásicos (como Tesseract, basado en LSTM), TrOCR está específicamente entrenado sobre conjuntos de datos de **escritura manuscrita real** (`microsoft/trocr-base-handwritten`), lo que lo hace superior para reconocer caligrafía irregular, tachones y letra variable típica de exámenes escolares de ESO y Bachillerato. Su rol en este proyecto se limita a la **Capa 1 de Defensa PII pre-nube** (`[Roadmap-002]`): detectar texto manuscrito en cabeceras de folios (nombre del alumno, firma) antes de enviar la imagen a la nube, complementando a Tesseract (que cubre texto impreso). TrOCR **no sustituye al motor de evaluación pedagógica** (Groq Vision), ya que no genera `visualMarkers (x,y)` ni comprensión semántica del contenido.

**PaddleOCR**  
Motor de OCR de deep learning desarrollado por Baidu, especializado en detección de texto, reconocimiento, orientación y estructura documental (tablas, columnas) sobre documentos corporativos impresos (facturas, contratos, planos). Ejecutable en local (CPU/GPU/ONNX Runtime) sin dependencia de APIs externas. En este proyecto, su rol potencial es como **escáner PII de Capa 1** para detectar texto impreso en cabeceras de folios (nombres tipografiados, DNIs) antes de la subida a Cloudinary o Groq Vision, siendo menos adecuado que TrOCR para caligrafía escolar manuscrita irregular.

---

## 13. Marca Personal y Comunicación Digital

**Ghostwriting (Redacción Delegada)**
Técnica de escritura en la que una persona o herramienta ayuda a redactar contenido que otra publica en su propio nombre. En el contexto de LinkedIn y marca personal: usar una IA como asistente para articular ideas propias en publicaciones, manteniendo siempre la voz y la veracidad de la autora. No es deshonesto si el contenido refleja experiencias y pensamientos reales.

**Hook (Gancho de Apertura)**
La primera línea o frase de una publicación en LinkedIn, diseñada para captar la atención del lector antes de que pulse "ver más". Es el elemento más crítico de un post: si el hook no engancha, el algoritmo de LinkedIn penaliza el contenido con menor alcance. Los tipos más efectivos incluyen: problema inesperado, tensión técnica, número concreto, historia personal, afirmación contracorriente o pregunta directa.

**CTA (Call to Action — Llamada a la Acción)**
Frase o elemento al final de un post que invita al lector a realizar una acción concreta: responder una pregunta, guardar el post, conectar con el autor o compartir su experiencia. Sin CTA, la mayoría de los lectores consumen el contenido y siguen sin interactuar. Tipos comunes: pregunta abierta, invitación a conectar, recomendación de guardar el post, o solicitud de experiencia del lector.

**Build in Public (Construir en Público)**
Estrategia de marca personal y transparencia donde un desarrollador o equipo documenta y comparte públicamente el proceso de construcción de su proyecto (decisiones, errores, aprendizajes, hitos) en tiempo real a través de redes sociales como LinkedIn. Genera comunidad, credibilidad y visibilidad sin necesitar un producto terminado.

**Marca Personal (Personal Branding)**
La percepción que otros tienen de un profesional basada en su presencia, reputación y contenido en línea. En el sector tecnológico, una marca personal sólida en LinkedIn (con publicaciones técnicas y portfolio visible en GitHub) genera más oportunidades de empleo que un CV tradicional. Se construye con consistencia, autenticidad y especialización temática.

**Engagement (Interacción)**
Métrica que mide la calidad de la interacción de una audiencia con el contenido publicado: likes, comentarios, compartidos y visualizaciones. En LinkedIn, el algoritmo amplifica el alcance de publicaciones con alto engagement en las primeras horas, haciendo que las interacciones tempranas sean cruciales.

**Algoritmo de LinkedIn**
Sistema automatizado que decide qué publicaciones ve cada usuario en su feed. Prioriza contenido que genera engagement temprano (primeros 60-90 minutos), publicaciones de contactos de primer y segundo grado, y posts que retienen al usuario en la plataforma (sin URLs externas en el cuerpo del post). Penaliza publicaciones muy cortas sin sustancia o posts con muchos hashtags irrelevantes.

**Impresiones (Impressions)**  
Número total de veces que una publicación es proyectada en la pantalla del dispositivo (móvil o PC) de un usuario mientras navega por su feed de noticias. Si un mismo usuario visualiza la publicación dos veces en momentos diferentes, contabiliza como dos impresiones.

**Miembros Alcanzados (Reach / Unique Members)**  
Número de usuarios reales e individuales que han visualizado la publicación en su pantalla al menos una vez. Representa el indicador de alcance único real, diferenciándose de las impresiones acumuladas.

**Alcance fuera de red (Out-of-Network Reach)**  
Proporción de usuarios alcanzados por una publicación que no forman parte de los contactos directos (1er grado) ni seguidores del autor. Un porcentaje elevado de alcance fuera de red indica que el algoritmo de la plataforma ha recomendado activamente el contenido debido a interacciones de alta autoridad (comentarios de perfiles sénior o relevantes en el sector).

**Consumo Pasivo (Lurking / Silent Engagement)**  
Fenómeno de comportamiento en redes profesionales donde aproximadamente el 90% de los usuarios (especialmente perfiles directivos, reclutadores e ingenieros sénior) consumen, leen y evalúan el contenido técnico sin realizar interacciones explícitas (likes o comentarios), influyendo de forma silenciosa en la reputación y posicionamiento del desarrollador.

**React**  
Librería de JavaScript (mantenida por Meta) para construir interfaces de usuario de forma declarativa y eficiente. Su filosofía se basa en dividir la interfaz en múltiples "Componentes" independientes y gestionar las actualizaciones de pantalla mediante un Virtual DOM, minimizando las recargas y mejorando el rendimiento.

**Vite**  
Herramienta de empaquetado (Bundler) y servidor de desarrollo moderno para proyectos web. Destaca por su extrema velocidad de arranque y actualización de módulos en caliente (*Hot Module Replacement*), logrando que cualquier cambio en el código se refleje instantáneamente en el navegador sin recargar la página.

**PWA (Progressive Web App)**  
Aplicación web que utiliza capacidades web modernas (como Service Workers y un `manifest.json`) para ofrecer una experiencia similar a una aplicación móvil nativa. Permite ser instalada directamente desde el navegador en la pantalla de inicio del teléfono, eludiendo las tiendas de aplicaciones tradicionales (App Store / Google Play).

**Service Worker**  
Script (archivo de código) que el navegador ejecuta en un hilo en segundo plano, separado de la página web principal. Actúa como un proxy de red, permitiendo interceptar peticiones, gestionar el almacenamiento en caché para funcionar sin conexión a internet y recibir notificaciones push.

**Canvas API**  
Interfaz de programación nativa de HTML5 que proporciona un medio para dibujar gráficos 2D dinámicamente mediante JavaScript. En este proyecto (`[D-034]`), se emplea como barrera de privacidad (*Client-Side Blackout Tool*) para que el usuario pueda tachar o manipular los píxeles de una fotografía localmente en la memoria de su navegador antes de transmitirla a los servidores.

**Componente (UI)**  
En arquitecturas como React, es una pieza de código independiente, aislada y reutilizable que representa una parte visual de la interfaz (ej: un botón, un menú lateral o un formulario). Los componentes encapsulan su propia estructura (HTML), estilo (CSS) y lógica (JavaScript).

**Virtual DOM**  
Representación en memoria (una copia ligera) del DOM (Document Object Model) real del navegador. Cuando los datos de una aplicación cambian, React primero actualiza este DOM virtual, calcula la diferencia exacta (*diffing*) con la versión anterior, y luego aplica únicamente esos cambios específicos en la pantalla real, logrando transiciones extremadamente rápidas.

**Script**  
Archivo de texto que contiene una secuencia de comandos o instrucciones escritas en un lenguaje de programación (como JavaScript o Python) que un motor de ejecución o navegador interpreta y ejecuta paso a paso.

**Empaquetador (Bundler)**  
Herramienta de desarrollo (como Vite o Webpack) que toma cientos de archivos individuales de código fuente (JavaScript, CSS, imágenes) y sus dependencias, y los combina, minimiza y optimiza en unos pocos archivos estáticos listos para ser servidos de forma eficiente en un entorno de producción.

**Servidor (Server)**  
Programa informático (o máquina física/virtual que lo ejecuta) diseñado para escuchar peticiones a través de una red, procesarlas y devolver una respuesta. En desarrollo Frontend, el "servidor de desarrollo" (ej: el que levanta Vite) aloja la página web localmente para que el programador pueda ver los cambios en tiempo real en `http://localhost`.

**Linter (ej. ESLint)**  
Herramienta de análisis estático de código que escanea el texto del programa en busca de errores de sintaxis, vulnerabilidades o violaciones de las convenciones de estilo del equipo. Actúa como un corrector ortográfico y gramatical para programadores. En el ecosistema React, ESLint es el estándar absoluto de la industria.

**Gestor de Paquetes / Package Manager (ej. npm)**  
Herramienta (como `npm`, `yarn` o `pnpm`) que automatiza la instalación, actualización y gestión de las librerías de terceros (dependencias) de las que depende un proyecto. En Node.js, `npm` (Node Package Manager) lee el archivo `package.json` y descarga todo lo necesario en la carpeta `node_modules`.

**Vanilla CSS**  
Escribir hojas de estilo en cascada de forma nativa y pura, apoyándose directamente en los estándares de la web (W3C), sin utilizar librerías o *frameworks* de terceros (como Tailwind CSS o Bootstrap) para abstraer el diseño.

**Glassmorphism**  
Tendencia estética en el diseño de interfaces de usuario (UI) que emula el aspecto del cristal esmerilado translúcido. Técnicamente se consigue aplicando desenfoques de fondo (con la propiedad `backdrop-filter: blur()`) sobre elementos semitransparentes, generando sensación de profundidad y jerarquía visual.

**Hot Module Replacement (HMR)**  
Mecanismo de las herramientas de empaquetado modernas (como Vite) que permite reemplazar, añadir o eliminar módulos de código en el navegador web en tiempo real, mientras la aplicación se está ejecutando, sin necesidad de recargar la página completa ni perder el estado actual de la sesión.

**Interfaz (de Usuario / UI)**  
Espacio de interacción, visual y táctil, mediante el cual un usuario humano se comunica con un sistema informático o software (en nuestro proyecto, la PWA visible en el navegador).

**Framework (Marco de Trabajo)**  
Entorno que proporciona una estructura de código predefinida y un conjunto de reglas estandarizadas para desarrollar software más rápido (ej: React en el frontend, FastAPI en el backend). A diferencia de una simple librería, un framework suele dictar la arquitectura general de la aplicación (*inversión de control*).

**Propiedades CSS (Variables / Custom Properties)**  
Entidades definidas por el desarrollador en hojas de estilo (ej: `--bg-primary`) que contienen valores específicos (como un código de color) y pueden reutilizarse en todo el documento. Son el pilar técnico para implementar "Sistemas de Diseño" y "Modos Oscuros" de forma eficiente y centralizada.

**Plugin**  
Módulo o extensión de software que se añade a un programa principal (como Vite o el navegador) para dotarlo de una función específica adicional sin necesidad de alterar su código base. Por ejemplo, `vite-plugin-pwa` inyecta automáticamente toda la lógica de aplicaciones progresivas en Vite.

**Certificado (SSL/HTTPS Autofirmado)**  
Archivo criptográfico digital que vincula una clave segura a la identidad de un servidor, permitiendo que la conexión entre el navegador y el sistema esté encriptada (HTTPS). En entornos de desarrollo local, se "autofirman" (el propio desarrollador los genera, como hace `@vitejs/plugin-basic-ssl`), lo que provoca que el navegador emita una advertencia por no estar avalados por una entidad certificadora pública externa, aunque la conexión sigue estando 100% cifrada.

**PII (Personally Identifiable Information)**  
Información de Identificación Personal. En el contexto del RGPD (GDPR) y la educación, abarca cualquier dato que pueda usarse para distinguir o rastrear la identidad de un individuo (nombres, DNI, rostros, firmas). En este proyecto, la eliminación de PII en origen (*Client-Side Redaction*) es obligatoria antes de procesar exámenes con IA.

**Metodologías Agile (Ej. Scrum, Kanban)**  
Conjunto de marcos de trabajo para el desarrollo de software basados en la adaptabilidad, la entrega continua y el desarrollo iterativo. Fomentan respuestas rápidas a los cambios (pivotes) por encima de seguir un plan rígido. En Agile, el historial de un *backlog* no se borra ni se reescribe para "ocultar" los cambios de rumbo, sino que se documenta (cancelando o aplazando tickets) para mantener la trazabilidad de las decisiones del equipo a lo largo del tiempo.

**Client-Side Redaction (Censura en el Cliente)**  
Técnica de ciberseguridad y privacidad donde la ocultación o eliminación de datos sensibles (PII) se realiza directamente en el dispositivo del usuario (el navegador web o app), antes de que la información sea transmitida a cualquier servidor externo. Garantiza que la información sensible nunca viaja por la red.

**Zero Data Retention (Retención de Datos Cero)**  
Política estricta de cumplimiento normativo (fundamental en IA y manejo de datos médicos/menores) que asegura que un sistema no almacena ni guarda en disco ningún dato procesado una vez finalizada la transacción o inferencia. En nuestra arquitectura, se aplica combinando *Client-Side Redaction* con un procesamiento efímero en RAM por parte del LLM.

**Canvas API (HTML5)**  
Interfaz de programación de los navegadores web modernos que proporciona un medio para dibujar gráficos, manipular fotografías o renderizar animaciones usando JavaScript y el elemento HTML `<canvas>`. En nuestro proyecto, es la barrera cripto-visual que permite tachar/censurar los nombres de los alumnos en el cliente sin que lleguen al backend (Zero Data Retention).

**DOM (Document Object Model)**  
Interfaz de programación estándar (API) que los navegadores web utilizan para representar un documento HTML. Transforma el código HTML estático en una estructura de árbol en vivo (nodos) donde cada etiqueta (como un `<div>` o un `<h1>`) es un objeto que puede ser modificado matemáticamente usando JavaScript.

**Virtual DOM**  
Representación en memoria (ligera y rápida) del Document Object Model (DOM) real de una página web. Frameworks como React utilizan el Virtual DOM para calcular eficientemente qué partes exactas de la interfaz han cambiado, actualizando en la pantalla real únicamente esas piezas (componentes) en lugar de recargar toda la página entera.

**Vitest (y JSDOM)**  
Framework de pruebas unitarias ultrarrápido creado para el ecosistema Vite. Permite verificar que el código frontend funciona sin necesidad de arrancar la aplicación completa. Para poder simular que el código se ejecuta en un navegador real, Vitest se apoya en **JSDOM**, una librería de Node que emula matemáticamente objetos como `window` o `document`.

**Vendor Prefix (Prefijos de proveedor CSS)**  
Extensiones de sintaxis (como `-webkit-`, `-moz-` o `-ms-`) que los navegadores web añaden a las propiedades CSS que aún están en fase experimental o no han sido estandarizadas formalmente por la W3C. La buena práctica dicta usarlas como respaldo y acompañarlas de la propiedad estándar equivalente.

**Condición de Carrera (Race Condition)**  
Un tipo de error o vulnerabilidad en sistemas concurrentes o asíncronos que ocurre cuando el comportamiento del software depende de la secuencia o el tiempo en que se ejecutan los eventos. En React, ocurre típicamente cuando intentamos manipular un elemento del DOM (como inyectar un vídeo) *antes* de que el motor de renderizado haya terminado de dibujarlo en la pantalla.

**React Hooks (`useEffect` / `useRef`)**  
Funciones especiales introducidas en React 16.8 que permiten "engancharse" al estado y al ciclo de vida de los componentes funcionales. `useRef` permite mantener una referencia directa a un elemento físico del DOM (como la etiqueta `<video>`), mientras que `useEffect` permite ejecutar código "después" de que React haya renderizado la pantalla, siendo el lugar seguro y correcto para interactuar con APIs externas o hardware.

**Fallback (Graceful Degradation)**  
Estrategia de diseño de software (Degradación Elegante) que asegura que un sistema siga funcionando, aunque sea con capacidades limitadas o una interfaz más básica, cuando falla una característica principal o el dispositivo no la soporta. Por ejemplo: intentar abrir la "cámara trasera" del móvil y, si falla porque estamos en un PC, hacer un *fallback* encendiendo la cámara web frontal.

**WebRTC / MediaDevices API (`getUserMedia`)**  
Interfaz de programación nativa de los navegadores web modernos que permite a las aplicaciones acceder al hardware multimedia del dispositivo (micrófono, cámara web o pantalla compartida) tras obtener el consentimiento explícito del usuario. Por motivos de seguridad y privacidad, los navegadores bloquean terminantemente esta API si la página no se sirve bajo protocolo seguro HTTPS o desde `localhost`.

---

*Términos y definiciones establecidos por Alba Camiña García. Redacción asistida por Antigravity (IA Copilot).*  
*Documento vivo — se actualiza con cada término nuevo que aparezca en el proyecto*  
*Actualizado el 10/08/2026 — Añadidos TrOCR y PaddleOCR como candidatos Capa 1 PII pre-nube (`[Roadmap-002]`), contrastados con la decisión de Groq Vision para v0.3.*  
*Actualizado el 11/08/2026 — Añadido Workload Routing al glosario tras el pivote D-051.*  
*Actualizado el 12/08/2026 — Añadidos conceptos de IA moderna: AI-Augmented Engineering, Agentic Coding y SOTA.*  
*Actualizado el 21/08/2026 — Añadidos conceptos de analítica de posicionamiento técnico: Impresiones, Miembros Alcanzados, Alcance fuera de red y Consumo Pasivo (Lurking).*
*Actualizado el 19/08/2026 — Añadida sección 13 (Marca Personal y Comunicación Digital) con conceptos de ghostwriting, hook, CTA, Build in Public, engagement y algoritmo de LinkedIn.*
*Actualizado el 25/08/2026 — Añadidos conceptos de gobernanza legal: Compliance y Legal Ops.*
*Actualizado el 26/08/2026 — Añadidos conceptos de la etapa SOTA: Trust, but verify, Patrón Showcase y el Síndrome del Impostor en IA.*
