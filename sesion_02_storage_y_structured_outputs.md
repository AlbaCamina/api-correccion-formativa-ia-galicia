# 📚 Sesión 2 — Object Storage, Structured Outputs y Presigned URLs
**Proyecto:** QIA-Correction  
**Tipo:** Documento de estudio y asimilación  
**Nivel:** Conceptual — sin código  
**Fecha:** Julio 2026

---

**📖 Índice de sesiones de estudio**

| Sesión | Temas | Archivo |
|---|---|---|
| Sesión 1 | Síncrono vs. Asíncrono · Colas de tareas (Redis + Celery) | [`sesion_01_asincronia_y_colas.md`](./sesion_01_asincronia_y_colas.md) |
| **← Sesión 2 (este documento)** | Object Storage · Structured Outputs · Presigned URLs | `sesion_02_storage_y_structured_outputs.md` |

---

> [!NOTE]
> Este documento está escrito para ser leído sin prisa. No necesitas memorizar nada —
> necesitas entender la lógica. Cuando la lógica tenga sentido, el código será consecuencia natural.

---

## Concepto 3 — Object Storage: por qué las imágenes no van en PostgreSQL

### El problema de guardar archivos en una base de datos

Imagina que tienes una biblioteca. La biblioteca tiene dos sistemas:

1. **El catálogo** — un fichero ordenado con el título de cada libro, su autor, su ubicación en la estantería, la fecha de publicación. Está diseñado para buscar rápido: *"¿Tienes libros de García Lorca?"* → respuesta en segundos.

2. **Las estanterías** — donde viven los libros físicos. No están diseñadas para buscar por autor, sino para almacenar objetos grandes y recuperarlos por su ubicación.

**PostgreSQL es el catálogo.** Está optimizado para:
- Buscar rápido (`WHERE`, `JOIN`, índices)
- Guardar datos estructurados (texto, números, fechas, JSON)
- Garantizar que los datos son consistentes y no se corrompen

Si intentas guardar un libro entero en el catálogo — es decir, guardar una imagen de 5MB como un campo en PostgreSQL — el sistema no rompe, pero:
- Las consultas se vuelven lentas porque cada fila pesa megabytes
- La base de datos crece desproporcionadamente
- No puedes servir esa imagen directamente al navegador sin procesarla antes
- Hacer copias de seguridad se vuelve muy caro

**Las estanterías son el Object Storage.** Servicios como **Cloudinary** o **Amazon S3** están diseñados específicamente para:
- Guardar archivos de cualquier tamaño (imágenes, PDFs, vídeos, backups)
- Servirlos directamente al navegador mediante una URL pública
- Escalar a millones de archivos sin degradación de rendimiento
- Aplicar transformaciones automáticas (redimensionar imágenes, convertir formatos)

### Cómo funciona en QIA-Correction

```
La profesora sube la foto del examen
           ↓
El archivo llega al servidor FastAPI
           ↓
FastAPI lo envía a Cloudinary
Cloudinary devuelve una URL pública:
   https://res.cloudinary.com/qia/image/upload/abc123.jpg
           ↓
FastAPI guarda esa URL en PostgreSQL
   (campo imagen_url de la tabla submissions)
           ↓
Cuando el panel web quiere mostrar el examen:
   Carga la imagen directamente desde la URL de Cloudinary
   No pasa por FastAPI para nada
```

PostgreSQL solo guarda el texto `"https://res.cloudinary.com/qia/image/upload/abc123.jpg"` — 60 caracteres, no 5MB. Rápido, ligero, eficiente.

### Cloudinary vs. S3 — ¿cuál y cuándo?

| | Cloudinary | Amazon S3 |
|---|---|---|
| **Configuración** | Sencilla — funciona en minutos | Más compleja — políticas IAM, buckets, CORS |
| **Transformaciones** | Automáticas (resize, crop, optimize) desde la URL | Hay que programarlas manualmente o usar Lambda |
| **Tier gratuito** | 25GB + 25GB transferencia/mes | 5GB primer año (después de pago) |
| **Cuándo usar** | MVP y desarrollo | Producción a escala o si ya usas AWS |

**Para QIA-Correction:** Cloudinary en desarrollo (v0.3) → S3 en producción si el producto escala. Esta decisión ya está documentada en `decisiones.md`.

### 🔑 La idea clave

> **PostgreSQL guarda el mapa. Object Storage guarda el territorio.**
> 
> En la BBDD guardas la dirección (URL). En el Object Storage guardas el archivo.
> Nunca mezcles los dos.

---

### ✅ Prueba de comprensión 3

**Pregunta:** El panel web del profesor necesita mostrar la imagen del examen junto al análisis de la IA. ¿Desde dónde se carga la imagen — desde FastAPI o desde Cloudinary? ¿Y desde dónde se carga el análisis de la IA?

**Respuesta correcta:**

- La **imagen** se carga directamente desde **Cloudinary** — el navegador hace una petición a la URL de Cloudinary sin pasar por FastAPI. El servidor no interviene.

- El **análisis de la IA** (el JSON con nota, desglose por rúbrica, análisis cualitativo) se carga desde **FastAPI**, que lo recupera de **PostgreSQL** (`evaluaciones.resultado_ia`).

Dos fuentes distintas, dos tipos de datos distintos: archivos binarios → Object Storage; datos estructurados → PostgreSQL + FastAPI.

---

## Concepto 4 — Structured Outputs: cómo obligar a la IA a devolver exactamente lo que necesitas

### El problema con los modelos de lenguaje sin restricciones

Los LLMs (GPT-4o, Claude, Gemini) son generadores de texto probabilísticos. Su objetivo es producir la respuesta más probable dado el contexto. Sin restricciones, si les pides que devuelvan un JSON, pueden responder:

```
Claro, aquí tienes el análisis:

**Transcripción:**
El alumno escribió...

```json
{
  "transcription": "El alumno escribió..."
```

Ups, me he quedado a medias. ¿Quieres que continúe?
```

O devolver el JSON correcto el 90% de las veces y una respuesta en prosa el 10% restante. En una API de producción, ese 10% son errores 500 para el usuario.

### La solución: Structured Outputs

**Structured Outputs** es un mecanismo que permite decirle al modelo: *"la única respuesta válida es un JSON que siga exactamente este esquema"*. El modelo no puede salirse del esquema — si lo intenta, el sistema lo corrige internamente hasta que encaja.

Imagina que en lugar de pedirle a un empleado que escriba un informe "como mejor le parezca", le das un **formulario con campos fijos**:

```
┌─────────────────────────────────────┐
│ INFORME DE EVALUACIÓN               │
│                                     │
│ Transcripción: ________________     │
│                                     │
│ Criterio 1 — Puntuación: ___/10     │
│ Criterio 1 — Justificación: ____    │
│                                     │
│ Mejoras inmediatas:                 │
│   • ____________________________    │
│   • ____________________________    │
│                                     │
│ Fortalezas:                         │
│   • ____________________________    │
└─────────────────────────────────────┘
```

El empleado (el modelo) **rellena el formulario**. No puede escribir fuera de los campos. El resultado siempre tiene la misma estructura.

### Cómo se implementa técnicamente

Hay dos enfoques principales:

**Enfoque 1 — `response_format` con JSON Schema (OpenAI / compatible):**
Le pasas el esquema JSON directamente a la API. El modelo garantiza que el output encaja:

```python
# Pseudocódigo — lo implementaremos en v0.1-000
respuesta = cliente.chat.completions.create(
    model="gpt-4o",
    response_format={"type": "json_object", "schema": mi_esquema_pydantic},
    messages=[{"role": "user", "content": mi_prompt}]
)
```

**Enfoque 2 — Validación con Pydantic + reintento (el que usaremos en v0.1):**
Le pides al modelo que devuelva JSON en el prompt, y si el JSON no encaja con tu modelo Pydantic, reintenta una vez. Más flexible y funciona con cualquier proveedor (OpenAI, Anthropic, Gemini):

```python
# Pseudocódigo
try:
    json_raw = llamar_a_la_ia(prompt)
    evaluacion = EvaluacionIA.model_validate_json(json_raw)  # Pydantic valida
except ValidationError:
    # El JSON no encaja — reintentamos una vez con más instrucciones
    json_raw = llamar_a_la_ia(prompt + "\n\nIMPORTANTE: Devuelve SOLO el JSON, sin texto adicional.")
    evaluacion = EvaluacionIA.model_validate_json(json_raw)
```

### Por qué esto importa tanto en QIA-Correction

El contrato JSON del sistema (definido en BLOQUE 5 del plan) es:

```json
{
  "transcription": "...",
  "rubricBreakdown": [{ "category": "...", "score": 6, "maxScore": 10, "reasoning": "..." }],
  "visualMarkers": [{ "x": 120, "y": 450, "type": "GRAMMAR_ERROR", "comment": "..." }],
  "qualitativeAnalysis": {
    "strengths": ["..."],
    "improvementNeeds": { "immediate": ["..."], "mediumLongTerm": ["..."] },
    "teacherSummary": "..."
  }
}
```

Si la IA devuelve este JSON con algún campo faltante o mal tipado, el modelo Pydantic `EvaluacionIA` lanza un error `422 Unprocessable Entity` y el servidor no guarda un resultado incompleto en la base de datos. Pydantic actúa como el último guardián de calidad del dato antes de que llegue a la BBDD.

### 🔑 La idea clave

> Sin Structured Outputs, la IA es un empleado que a veces entrega el informe en el formato correcto
> y a veces escribe un poema.
>
> Con Structured Outputs + Pydantic, la IA es un empleado que rellena un formulario.
> Si un campo no está bien rellenado, el formulario no se acepta.
> El sistema rechaza el error antes de que llegue al usuario.

---

### ✅ Prueba de comprensión 4

**Pregunta:** La IA devuelve el siguiente JSON. ¿Qué pasa cuando Pydantic intenta validarlo?

```json
{
  "transcription": "El alumno describió correctamente el concepto de libertad...",
  "rubricBreakdown": [{ "category": "Argumentación", "score": "siete", "maxScore": 10 }],
  "qualitativeAnalysis": {
    "strengths": ["Buen uso del vocabulario filosófico"],
    "improvementNeeds": { "immediate": ["Faltan ejemplos"] },
    "teacherSummary": "Respuesta sólida con margen de mejora."
  }
}
```

**Respuesta correcta:**

Pydantic lanza un error de validación (`ValidationError`) por dos motivos:

1. **`score` es una cadena de texto (`"siete"`) en lugar de un número entero.** El modelo Pydantic espera `int`, no `str`.

2. **Falta el campo `visualMarkers`.** Es un campo requerido del contrato (array, puede estar vacío `[]` pero debe existir).

El servidor devuelve un error `422 Unprocessable Entity` y reintenta la llamada a la IA con instrucciones reforzadas. Si el segundo intento también falla, devuelve `500 Internal Server Error` con un mensaje claro en el log. El resultado corrupto **nunca llega a la base de datos**.

---

## Concepto 5 — Presigned URLs: el atajo que elimina al intermediario

### El problema del servidor como cuello de botella en la subida de archivos

Cuando una profesora sube la foto de un examen, el flujo más obvio sería:

```
Profesora (móvil)  →→→  FastAPI  →→→  Cloudinary
         [foto 5MB]         [procesa]      [guarda]
```

Esto tiene un problema grave: **FastAPI tiene que recibir 5MB, mantenerlos en memoria y reenviarlos a Cloudinary**. Si 50 profesoras suben fotos a la vez, el servidor está gestionando 250MB de archivos en memoria mientras hace otras cosas. El servidor se convierte en el cuello de botella.

### La solución: la URL firmada

Una **Presigned URL** (URL prefirmada) es un enlace temporal y único que permite a alguien subir un archivo **directamente a Cloudinary** sin pasar por tu servidor, pero solo durante un tiempo limitado (por ejemplo, 5 minutos) y solo para ese archivo específico.

La analogía perfecta es el **aparcacoches de un hotel**:

> Tú llegas al hotel con el coche. El aparcacoches no te sube el coche en su propio coche — te da una **tarjeta de acceso temporal** al parking. Tú aparcar el coche directamente. El aparcacoches no tiene que hacer el viaje.

En términos técnicos:

```
1. Profesora pulsa "Subir examen" en la PWA
            ↓
2. La PWA pregunta a FastAPI: "Dame permiso para subir una foto"
   FastAPI responde: "Aquí tienes una URL firmada válida 5 minutos:
   https://cloudinary.com/upload?token=xyz123&expires=1720000000"
            ↓
3. La PWA sube la foto DIRECTAMENTE a Cloudinary usando esa URL
   FastAPI no ve ni un byte del archivo
            ↓
4. Cloudinary confirma: "Subida completada, URL pública: .../abc.jpg"
            ↓
5. La PWA notifica a FastAPI: "Ya está subida, aquí la URL"
   FastAPI guarda la URL en PostgreSQL
```

### ¿Por qué esto importa en el MVP?

En v0.3, cuando implementemos la subida de imágenes, tenemos dos opciones:

| Opción | Cómo funciona | Cuándo usar |
|---|---|---|
| **Sin presigned URL** | Archivo pasa por FastAPI | MVP v0.3 — más simple de implementar |
| **Con presigned URL** | Archivo va directo a Cloudinary | Producción o cuando el volumen de imágenes satura el servidor |

Para v0.3 del MVP, subiremos el archivo a través del servidor (más simple). Las presigned URLs las implementaremos cuando sea necesario escalar.

> [!NOTE]
> Estudias esto ahora porque en v0.3 verás el código de subida y entenderás la limitación. En ese momento tendrás el criterio para decidir si añadir presigned URLs o no. El conocimiento previo evita que hagas decisiones a ciegas.

### 🔑 La idea clave

> **Sin presigned URL:** el archivo viaja Profesora → FastAPI → Cloudinary.
> El servidor es el cartero que lleva todos los paquetes.
>
> **Con presigned URL:** el archivo viaja Profesora → Cloudinary directamente.
> El servidor solo firma el permiso de acceso.
> El cartero desaparece del viaje.

---

### ✅ Prueba de comprensión 5

**Pregunta:** Una presigned URL caduca a los 5 minutos. Una profesora genera la URL, se distrae respondiendo un email y 8 minutos después intenta subir el examen con esa URL. ¿Qué ocurre?

**Respuesta correcta:**

Cloudinary rechaza la subida con un error de autorización (normalmente `403 Forbidden` o `401 Unauthorized`). La URL ha expirado y el token de firma ya no es válido.

La PWA detecta el error y debe pedir al servidor una nueva URL firmada antes de reintentar la subida. El archivo del examen no se pierde — sigue en el dispositivo de la profesora. Solo necesita repetir el proceso de subida con un nuevo permiso.

Esta caducidad es una **característica de seguridad, no un bug**: evita que alguien intercepte la URL y la use para subir archivos arbitrarios a tu almacenamiento horas después.

---

## Resumen de la Sesión 2

| Concepto | En una frase |
|---|---|
| **Object Storage** | PostgreSQL guarda la dirección; Cloudinary/S3 guarda el archivo |
| **Cloudinary** | Object Storage gestionado con transformaciones automáticas — ideal para MVP |
| **Structured Outputs** | Forzar al LLM a rellenar un formulario JSON en lugar de escribir libremente |
| **Pydantic como guardián** | Si el JSON de la IA no encaja con el contrato, el servidor rechaza el dato antes de guardarlo |
| **Presigned URL** | Permiso temporal para que el cliente suba directamente al almacenamiento sin pasar por el servidor |

---

## ¿Por qué esto importa en tu proyecto?

| Concepto | Cuándo lo usas en QIA-Correction |
|---|---|
| **Object Storage** | v0.3 — cuando el profesor sube la foto del examen |
| **Structured Outputs** | v0.1-000 — **ahora mismo**, en el smoke test del contrato JSON |
| **Presigned URLs** | v0.3 o producción — cuando el volumen de imágenes lo justifique |

El más urgente es **Structured Outputs** — es el prerequisito directo de la primera línea de código del proyecto.

---

## Próxima sesión: primera línea de código

Con los conceptos de sesión 1 y sesión 2 asimilados, el siguiente paso es la **v0.1-000**: el smoke test del contrato JSON con el LLM.

No hay más sesiones teóricas previstas antes del código. A partir de ahora, los conceptos nuevos (autenticación JWT, Docker, despliegue) se explican en el momento en que los necesitas, dentro del contexto del código real.

---

*Sesión 2 completada — Julio 2026 | QIA-Correction con Antigravity*
