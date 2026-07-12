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

**Debug / Debugging**  
Proceso de encontrar y corregir errores en el código. Literalmente "quitar los bichos".

**Deploy / Despliegue**  
Publicar el código en un servidor accesible desde internet. Antes solo funciona en tu máquina local; tras el deploy, cualquiera puede usarlo.

**Endpoint**  
Una URL concreta de la API a la que se puede hacer una petición. Ejemplo: `POST /api/v1/evaluate` es el endpoint que recibe el examen y devuelve la corrección.

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
- `422 Unprocessable Entity` — los datos no pasan validación

**HTTPS** (HyperText Transfer Protocol Secure — Protocolo HTTP Seguro)  
Versión segura y cifrada de HTTP (el candado en el navegador). Es un requisito estricto en dispositivos móviles para permitir instalar una PWA y para autorizar el acceso a la cámara o micrófono.
- `500 Internal Server Error` — algo falló en el servidor

**JSON** (JavaScript Object Notation — Notación de Objetos de JavaScript)  
Formato estándar para intercambiar datos entre sistemas. Parece un diccionario de Python con llaves y valores. Es el formato que devuelve la IA con la corrección del examen.

**Refactor**  
Reescribir código para que sea más limpio o eficiente sin cambiar lo que hace. Como reordenar una habitación sin tirar nada.

**README**  
Archivo de texto en la raíz del repositorio que explica qué es el proyecto, cómo instalarlo y cómo usarlo. Es lo primero que ve cualquier persona que visita el repositorio en GitHub.

**Stack tecnológico**  
El conjunto de tecnologías que usa un proyecto. En QIA-Correction: Python + FastAPI + PostgreSQL + React + Vite + Redis + Celery.

**Swagger / OpenAPI**  
Estándar para describir y documentar APIs REST. FastAPI lo integra nativamente: al arrancar el servidor, genera automáticamente una interfaz web interactiva en la ruta `/docs` que permite probar todos los endpoints desde el navegador sin escribir código ni instalar herramientas.

---

## 2. Python y backend

**Alembic**  
Herramienta de migraciones para SQLAlchemy. Guarda un historial de todos los cambios que has hecho en la estructura de la base de datos, como un control de versiones para las tablas.

**FastAPI**  
El framework (marco de trabajo) de Python con el que se construye la API. Es moderno, muy rápido y genera documentación automática. Equivalente a Fastify pero en Python.

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
Conjunto de conexiones a la base de datos que se reutilizan en lugar de abrirse y cerrarse con cada petición. Mejora el rendimiento bajo carga.

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

**Seed**  
Datos iniciales que se insertan en la base de datos al crearla para que no esté vacía. En este proyecto: al menos un marco de evaluación de Bachillerato o ESO según el decreto autonómico de la Xunta de Galicia.

**UUID** (Universally Unique Identifier — Identificador Único Universal)  
Un código alfanumérico generado automáticamente que identifica un registro de forma única en todo el sistema. Ejemplo: `a3f8c2d1-4b5e-...`. Se usa como ID de submissions para evitar IDs secuenciales predecibles.

---

## 4. Inteligencia Artificial

**Claude**  
Modelo de lenguaje de la empresa Anthropic. Alternativa a GPT-4o. Se considera especialmente bueno para tareas de razonamiento y escritura estructurada.

**Confidence Score** (Índice de Confianza IA)  
Medida numérica devuelta por el modelo (`0.0` a `1.0`) que indica la certeza o fiabilidad de la interpretación y lectura de un examen. En QIA-Correction (`[D-024]`), si la confianza es `< 0.75` (caligrafía confusa, borrones), el sistema emite una alerta visual para que la profesora revise con especial atención prioritaria.

**Generador Asistido de Rúbricas (Copiloto Pre-Corrección)**  
Funcionalidad de asistencia de QIA-Correction (`Capa 4` relacional) por la que el docente solo necesita subir o describir el enunciado de una prueba o tarea evaluable. El motor LLM cruza automáticamente la normativa general (`Capa 1`), la programación del departamento (`Capa 2`) y el acuerdo transversal del centro (`Capa 3`) para generar una propuesta de rúbrica en 4 niveles de logro (*Insuficiente, Suficiente/Bien, Notable y Sobresaliente*). El profesor la valida con un clic en su PWA, reduciendo un 90% del tiempo burocrático de diseño de baremos.

**GPT-4o** / **GPT-4o Vision**  
Modelo de lenguaje de OpenAI. La variante Vision acepta imágenes además de texto, lo que permite enviarle la foto del examen para que lo lea y evalúe.

**Jerarquía Normativa en 5 Capas Relacionales (`JSONB`)**  
Modelo arquitectónico multinivel de QIA-Correction que desacopla y combina sin ambigüedad la legislación pública (`Capa 1: Decreto Xunta`), la programación anual del departamento (`Capa 2: Saberes y Criterios`), las normas comunes del colegio (`Capa 3: PEC/CCP`), la rúbrica de la prueba asistida (`Capa 4: El Profesor`) y las adaptaciones individuales de equidad (`Capa 5: NEAE/NEE en JSONB`).

**LLM** (Large Language Model — Modelo de Lenguaje Grande)  
Modelo de inteligencia artificial entrenado con enormes cantidades de texto. Es la IA que corrige los exámenes en este proyecto (GPT-4o o Claude).

**Multimodal / Omni-canal**  
Un modelo de IA que procesa texto, imagen y estructuras combinadas de forma simultánea (ej. GPT-4o o Claude 3.5 Sonnet). En QIA-Correction esto permite evaluar **cualquier tipo de prueba evaluable**: no solo fotos de exámenes manuscritos, sino murales de cartulina de aula, redacciones en campos de texto online (`Form Text`) y PDFs o capturas de presentaciones hechas a ordenador (como *Canva* o *Google Slides*).

**OCR** (Optical Character Recognition — Reconocimiento Óptico de Caracteres)  
Tecnología integrada en la IA multimodal que extrae y convierte la caligrafía manuscrita de la foto del examen o el texto gráfico de un mural/cartulina en datos legibles para evaluarlos contra la rúbrica.

**Prueba evaluable (Instrumento de evaluación)**  
Cualquier evidencia de aprendizaje del alumno sometida a corrección formativa. En QIA-Correction abarca los 3 formatos del aula moderna: papel manuscrito (foto), creación plástica/visual (foto de mural o cartulina) y entregas digitales (redacciones online o exportaciones PDF/PNG de presentaciones de Canva).

**Prompt**  
El texto de instrucciones que se le da al modelo de IA para que sepa cómo comportarse. En este proyecto, el prompt le dice a la IA que actúe como "evaluador formativo experto en educación secundaria de Galicia" y le especifica el formato JSON que debe devolver.

**Structured Outputs** (Salidas Estructuradas)  
Mecanismo que fuerza al modelo de IA a devolver siempre un JSON con un esquema fijo, en lugar de responder en texto libre. Explicado en detalle en `sesion_02_storage_y_structured_outputs.md`.

**Token** (en contexto de IA)  
La unidad mínima de texto que procesa un modelo de lenguaje. Aproximadamente 1 token = 0,75 palabras en español. Los modelos de IA cobran por tokens consumidos (tanto los del prompt como los de la respuesta).

---

## 5. Almacenamiento e infraestructura

**Broker**  
En el contexto de colas de tareas: el intermediario que recibe las tareas pendientes y las distribuye a los workers. En este proyecto Redis actúa como broker de Celery.

**Celery**  
Librería de Python para ejecutar tareas en segundo plano (de forma asíncrona). Cuando un profesor sube un examen, Celery encola la tarea de corrección para que el servidor no se quede bloqueado esperando. Explicado en `sesion_01_asincronia_y_colas.md`.

**Cold Storage / Almacenamiento en frío**  
Almacenamiento en la nube de muy bajo coste diseñado para archivar archivos que rara vez se consultan pero deben conservarse por imperativo legal (como los exámenes ante posibles reclamaciones). Equivalente digital a un archivo de cajas en un sótano. AWS Glacier y Cloudinary Archive son ejemplos.

**Cloudinary**  
Servicio de almacenamiento y gestión de imágenes en la nube. Las fotos de los exámenes se guardan aquí, no en la base de datos. Tiene capa gratuita generosa. Explicado en `sesion_02_storage_y_structured_outputs.md`.

**Docker** / **Docker Compose**  
Docker permite empaquetar una aplicación con todo lo que necesita para funcionar en un "contenedor" aislado. Docker Compose orquesta varios contenedores a la vez (por ejemplo: la app de FastAPI + PostgreSQL + Redis arrancando juntos con un solo comando).

**Presigned URL** (URL Prefirmada)  
Un enlace temporal y firmado que permite subir un archivo directamente a Cloudinary o S3 sin pasar por el servidor. Explicado con la analogía del aparcacoches en `sesion_02_storage_y_structured_outputs.md`.

**Storage Lifecycle / Política de ciclo de vida**  
Reglas automatizadas configuradas en el proveedor de nube (S3/Cloudinary) que trasladan o eliminan archivos según su antigüedad. En QIA-Correction: pasan a Cold Storage a los 60 días y se eliminan (purga legal RGPD) al año exacto.

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
Elemento de HTML que permite dibujar, recortar y transformar gráficos e imágenes en la memoria local del navegador mediante JavaScript. En QIA-Correction: la PWA utiliza el Canvas para redimensionar los exámenes a ~2048px ([D-020]) y recortar los 3 cm de la cabecera con el nombre del alumno ([D-022]) antes de subirlos a la nube.

**Manifest.json**  
Archivo de configuración que le dice al navegador cómo mostrar la PWA cuando se instala: nombre, icono, colores, orientación de pantalla.

**PWA / PWA del Profesor** (Progressive Web App — Aplicación Web Progresiva)  
Una aplicación web construida con tecnologías modernas (React + Vite) que se abre en el navegador pero se comporta y se puede instalar como una app nativa en el portátil, tablet o móvil del docente sin pasar por tiendas de aplicaciones. En QIA-Correction es el panel frontal y centro de mando del profesor (*Human-in-the-Loop*): donde sube las fotos del examen o mural, visualiza la corrección con sus marcadores de color (rojos o grises de adaptación), ajusta la propuesta y aprueba las notas finales. Accessa localmente a cámara y funciona en red de forma ultra veloz.

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
Sistema de control de versiones. Guarda el historial completo de cambios del código, permite volver atrás y trabajar en paralelo con ramas.

**GitHub**  
Plataforma web donde se aloja el repositorio Git del proyecto. Es donde los empleadores y reclutadores verán el código y el historial de trabajo.

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
Medidas de modificación o ajuste pedagógico reguladas por la legislación (LOMLOE, Decreto 229/2011 de Galicia) para garantizar la equidad educativa del alumnado. Pueden ser ordinarias o no significativas (ACNS, ej: dislexia, TDAH) sin alterar objetivos, o significativas (ACS) cuando modifican el currículo oficial. En QIA-Correction se inyectan mediante el campo `adaptaciones_alumno` ([D-023]) para separar faltas ortográficas del cálculo penalizador de nota.

**AI Act** (Reglamento Europeo de Inteligencia Artificial)  
La primera ley de la Unión Europea que regula los sistemas de IA. Clasifica los sistemas por nivel de riesgo. QIA-Correction entra en la categoría de alto riesgo (afecta a educación de menores y procesa variables de necesidades específicas), por lo que requiere Human-in-the-Loop y trazabilidad completa.

**DUA** (Diseño Universal de Aprendizaje)  
Enfoque pedagógico recogido por la LOMLOE y la normativa gallega que busca minimizar las barreras en el aprendizaje, ofreciendo múltiples formas de representación, expresión e implicación en la evaluación.

**HitL / Human-in-the-Loop** (Humano en el Bucle)  
Diseño en el que la IA propone pero el humano decide. En este proyecto: la IA genera un borrador de corrección, pero el profesor tiene que aprobarlo antes de que sea oficial. Es el escudo legal bajo el AI Act.

**Inmutabilidad probatoria**  
Propiedad por la cual un registro o evaluación ya aprobada (`GRADED`) queda bloqueada contra modificaciones o borrados posteriores (*append-only*). Garantiza la validez jurídica del historial ante inspecciones educativas, reclamaciones de exámenes o auditorías bajo el AI Act.

**LOMLOE** (Ley Orgánica de Modificación de la LOE — Ley de Educación)  
La ley educativa estatal actualmente vigente en España (2020). Define competencias, criterios de evaluación y estructura curricular. El decreto autonómico de la Xunta de Galicia la desarrolla a nivel regional para el sistema educativo gallego (bilingüe castellano/gallego).

**LOPDGDD** (Ley Orgánica de Protección de Datos y Garantía de los Derechos Digitales)  
La ley española que desarrolla el RGPD. Su artículo 7 regula el consentimiento y protección integral en el tratamiento de datos de menores. En QIA-Correction es crítico porque la información sobre adaptaciones por dislexia, TDAH o TEA constituye un dato de salud del menor (especialmente protegido), motivo por el cual la IA jamás diagnostica y el dato solo se asocia al identificador seudonimizado `alumno_id` ([D-023]).

**NEAE / NEE** (Necesidades Específicas de Apoyo Educativo / Necesidades Educativas Especiales)  
Clasificación legal en España para el alumnado que requiere una atención educativa diferente a la ordinaria por presentar dificultades específicas de aprendizaje (DEA como dislexia), TDAH, altas capacidades o discapacidad (NEE). QIA-Correction adapta su motor formativo para que estos perfiles sean evaluados con justicia sin penalizar errores derivados de su condición ([D-023]).

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
Modelo operativo dual vigente en los IES gallegos (Decretos 156/157/2022) y reflejado en XADE/QIA-Correction: 1) **Circuito de Materias:** Las asignaturas se califican y cierran en los boletines trimestrales y ordinarios con **números enteros del 1 al 10** derivados de las notas cotidianas numéricas de las pruebas evaluables. 2) **Circuito de Competencias Clave:** Las 8 competencias oficiales (*CCL, STEM, CD...*) se califican al final del curso de forma cualitativa (*IN, SU, BI, NT, SB*) mediante el **cruce e intersección matricial inter-materias** de todos los criterios evaluados en las diferentes asignaturas del alumno.

**Equipotencialidad Criterial (`Decreto 156/157/2022`)**  
Regla pedagógica general y por defecto por la que todos los Criterios de Evaluación (`criterio_id`) asociados a las competencias específicas de una materia tienen idéntico valor o peso en el cálculo de la nota final, salvo que el departamento establezca porcentajes diferenciados en su Programación Didáctica (`Capa 2`).

**Evaluación Competencial Cualitativa (`Decretos 156/157/2022 Galicia`)**  
Modelo evaluativo obligatorio en Galicia para ESO y Bachillerato centrado en el grado de adquisición de las competencias clave y específicas del currículo, expresado en grados cualitativos (*Insuficiente [IN], Suficiente [SU], Bien [BI], Notable [NT], Sobresaliente [SB]*) además o en lugar de la nota numérica simple (`[D-024]`).

**Feed Forward / Actionable Next Steps (Siguiente Paso Accionable y Seguimiento No Sumativo)**  
Estándar pedagógico anglosajón (modelo Hattie & Timperley en GCSE/A-Levels del Reino Unido) que soluciona el problema de la "IA cierta pero inútil". Exige que cada corrección formativa proporcione una acción única, concreta e inmediata que el alumno puede hacer hoy mismo para avanzar (`[D-024]`). Para no sobrecargar al docente con dobles correcciones, su cumplimiento se modela como un checklist formativo y de autoevaluación en base de datos (`estado_feed_forward: PENDIENTE | REALIZADO | VERIFICADO`) sin calificación sumativa (`[D-026]`).

**Backlog**  
Lista priorizada de todo el trabajo pendiente del proyecto, organizado en historias de usuario. En este proyecto: `backlog.md`.

**Criterios de aceptación**  
Lista de condiciones concretas y verificables que deben cumplirse para considerar una historia de usuario terminada. Sin criterios claros, no hay forma de saber cuándo algo está "listo".

**Historia de usuario**  
Forma de describir una funcionalidad desde el punto de vista del usuario final. Formato: "Como [rol], quiero [acción], para [beneficio]". Es la unidad de trabajo del backlog.

**Milestone**  
Punto de referencia en el roadmap del proyecto. En este proyecto equivale a una versión (v0.1, v0.2...). Cada milestone agrupa las historias de usuario de esa versión.

**MVP** (Minimum Viable Product — Producto Mínimo Viable)  
La versión más pequeña del producto que ya aporta valor real. En este proyecto: v1.0 desplegada y funcionando.

**Ponderación Criterial vs. Instrumental**  
Mandato legal de la LOMLOE en Galicia según el cual la calificación y ponderación recae siempre sobre los **Criterios de Evaluación (`criterio_id`)** del currículo, y nunca sobre los instrumentos en sí mismos. Los instrumentos (exámenes, murales de cartulina o exposiciones en *Canva*) son únicamente el soporte o medio omni-canal de recogida de evidencias de aprendizaje.

**Situación de Aprendizaje (SdA)**  
Propuesta metodológica o tarea reto contextualizada (real o simulada) que permite al alumnado movilizar saberes básicos para resolver un problema, siguiendo la trazabilidad `Reto → Saberes → Competencias Específicas → Criterios → Descriptores Operativos`. En QIA-Correction actúa como el Contenedor Padre (`situacion_aprendizaje_id` en Capa 2) para agrupar todas las pruebas evaluables omni-canal del alumno en esa unidad y calcular el logro de sus competencias.

**Soberanía del Acto Administrativo (`HitL`)**  
Principio fundamental del Derecho Público español y del *AI Act* que dictamina que la responsabilidad jurídica, formal y humana y el poder de decisión sobre una calificación oficial (*que constituye un acto administrativo con efectos en la promoción o titulación del alumno*) recae exclusiva e intransferiblemente en el docente o tribunal que firma el acta en XADE. Una IA o aplicación comercial jamás puede ser autora ni titular legal del acto administrativo; por ello, QIA-Correction asiste y calcula, pero exige siempre la validación y firma humana final del profesor (*Human-in-the-Loop*).

**Smoke test**  
Prueba muy básica que verifica que lo más fundamental funciona antes de construir nada encima. En este proyecto: `v0.1-000` comprueba que la IA devuelve el JSON correcto antes de construir FastAPI.

**XADE (`Xestión Administrativa da Educación`)**  
Aplicación informática oficial de la Xunta de Galicia (Consellería de Educación) para todos los centros docentes gallegos. Es donde las secretarías y equipos docentes matriculan al alumnado e introducen las notas numéricas por materia y cualitativas por competencias clave para cerrar actas e imprimir boletines en cada junta de evaluación. QIA-Correction asiste y calcula el día a día para que el trasvase final de datos de corrección a XADE sea rápido, seguro y 100% auditable.

**YAGNI** (You Aren't Gonna Need It — No lo vas a necesitar)  
Principio de desarrollo: no escribas código para funcionalidades que no necesitas ahora mismo. Evita sobre-ingeniería.

---

## 11. Seguridad y autenticación

**API key**  
Clave secreta que identifica y autentica a quien llama a una API. Las claves de OpenAI, Anthropic, Gemini y Groq son API keys. Nunca se suben al repositorio — van en el archivo `.env`.

**Bearer token**  
Tipo de token de autenticación que se envía en la cabecera HTTP de cada petición: `Authorization: Bearer <token>`. Los JWT se usan como Bearer tokens.

**.env**  
Archivo de texto que contiene variables de entorno (claves de API, contraseñas, configuración sensible). Nunca se sube a GitHub — está en el `.gitignore`. El archivo `.env.example` muestra qué variables existen sin revelar sus valores.

**ENS (Esquema Nacional de Seguridad)**  
Regulamento y marco normativo obligatorio que fija los requisitos y políticas de ciberseguridad en la Administración Pública y en los sistemas que tratan datos institucionales o de ciudadanos (como XADE en Galicia). Debido a las rigurosas exigencias del ENS y de AMTEGA sobre la protección de datos de menores, se prohíbe la conexión o inyección externa por APIs privadas comerciales directamente en XADE, justificando que el trasvase desde QIA-Correction se realice localmente mediante exportación de ficheros o scripts locales en el navegador del funcionario (`[D-025]`).

**JWT** (JSON Web Token — Token Web JSON)  
Un token firmado digitalmente que el servidor entrega al usuario al hacer login. El usuario lo incluye en cada petición posterior para demostrar que está autenticado, sin que el servidor tenga que consultar la base de datos en cada petición.

**Variables de entorno**  
Valores de configuración que se inyectan en el programa desde el sistema operativo o desde un archivo `.env`, sin escribirlos directamente en el código. Separa la configuración del código.

---

## 12. Negocio y modelo

**B2B** (Business to Business — De empresa a empresa)  
Modelo en el que el cliente es otra empresa, no un usuario individual. En QIA-Correction: colegios o plataformas EdTech que contratan la API con una API key.

**B2C** (Business to Consumer — De empresa a consumidor)  
Modelo en el que el cliente es un usuario individual. En QIA-Correction: profesores que se suscriben directamente a la PWA.

**EdTech** (Education Technology — Tecnología educativa)  
Sector de empresas que desarrollan productos tecnológicos para la educación. Son los potenciales clientes B2B de QIA-Correction.

**Freemium**  
Modelo de negocio con una versión gratuita (con límites) y una versión de pago (sin límites o con funcionalidades extra).

**SaaS** (Software as a Service — Software como Servicio)  
Modelo en el que el software se ofrece como servicio por suscripción, sin que el usuario tenga que instalarlo. La PWA de QIA-Correction es un SaaS.

---

*Glosario creado el 09/07/2026 — Antigravity para Alba Camiña García*  
*Documento vivo — se actualiza con cada término nuevo que aparezca en el proyecto*
