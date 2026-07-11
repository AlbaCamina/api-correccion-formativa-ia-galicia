# 📚 Sesión 1 — Asincronía y Colas de Tareas
**Proyecto:** QIA-Correction  
**Tipo:** Documento de estudio y asimilación  
**Nivel:** Conceptual — sin código  
**Fecha:** Julio 2026

---

**📖 Índice de sesiones de estudio**

| Sesión | Temas | Archivo |
|---|---|---|
| **← Sesión 1 (este documento)** | Síncrono vs. Asíncrono · Colas de tareas (Redis + Celery) | `sesion_01_asincronia_y_colas.md` |
| Sesión 2 | Object Storage · Structured Outputs · Presigned URLs | [`sesion_02_storage_y_structured_outputs.md`](./sesion_02_storage_y_structured_outputs.md) |

---

> [!NOTE]
> Este documento está escrito para ser leído sin prisa. No necesitas memorizar nada —
> necesitas entender la lógica. Cuando la lógica tenga sentido, el código será consecuencia natural.

---

## Concepto 1 — Síncrono vs. Asíncrono

### ¿Qué significa "síncrono"?

Síncrono significa que las cosas ocurren **en orden estricto, una detrás de otra**.
Nadie avanza hasta que el anterior ha terminado.

Imagina que eres la única profesora del departamento y tienes que entregar los exámenes corregidos a 90 alumnos. Si trabajas de forma **síncrona**:

> El alumno 1 entra, te entrega el examen. Tú te sientas a corregirlo delante de él.
> Tardas 12 minutos. Le das la nota. Sale. Entra el alumno 2.

El alumno 90 lleva **18 horas esperando en el pasillo**.

Esto es exactamente lo que hace tu servidor por defecto: atiende una petición, la procesa completamente, y solo entonces atiende la siguiente.

Si corregir un examen con IA tarda 15 segundos, y llegan 30 profesores a la vez, el último espera **7,5 minutos** de pie. Y durante ese tiempo, el servidor no puede hacer nada más — está bloqueado.

### ¿Qué significa "asíncrono"?

Asíncrono significa que el sistema **no espera** a que una tarea termine para atender la siguiente. Delega el trabajo pesado y sigue disponible.

Con el mismo escenario, pero trabajando de forma **asíncrona**:

> El alumno 1 entra, te entrega el examen. Tú le dices:
> *"Recibido. Te mando la nota por email cuando esté corregido. Siguiente."*
> Tardas 3 segundos en esa interacción. Entran los 90 alumnos en 5 minutos.
> Tú corriges los exámenes más tarde, a tu ritmo.
> Cada alumno recibe su nota en su email cuando está lista.

El servidor responde a todas las peticiones **de forma inmediata** con un *"recibido, estamos en ello"* — y procesa el trabajo pesado en segundo plano.

### La respuesta que da el servidor asíncrono

Cuando un profesor sube un examen, el servidor no responde con la corrección.
Responde con esto:

```
202 Accepted
{
  "submission_id": "abc-123",
  "status": "PENDING",
  "mensaje": "Examen recibido. Recibirás la corrección en breve."
}
```

El código `202` significa exactamente eso: *"He recibido tu petición y la estoy procesando, pero aún no tengo el resultado."*

Más tarde, cuando la corrección esté lista, el profesor puede consultar el estado:

```
GET /submissions/abc-123
→ { "status": "GRADED", "resultado": { ... } }
```

O el sistema le manda una notificación automática.

---

### 🔑 La idea clave

> **Síncrono:** el servidor está pendiente de ti hasta que termina.
> El usuario espera bloqueado.
>
> **Asíncrono:** el servidor te dice "anotado" y sigue con otros.
> El trabajo pesado ocurre en segundo plano.
> El usuario recibe el resultado cuando está listo.

---

### ✅ Prueba de comprensión 1

**Pregunta:** En el flujo de tu app, ¿en qué momento exacto crees que el sistema debe decirle al profesor "recibido"? ¿Y cuándo debe mostrarle los resultados?

**Respuesta correcta (guárdala como referencia):**

- El sistema dice **"recibido"** en el instante en que el profesor pulsa "enviar" y el archivo llega al servidor — antes incluso de que la IA empiece a trabajar. Esto ocurre en milisegundos.

- El sistema **muestra los resultados** cuando el worker ha terminado de procesar
  el examen con la IA, ha validado el JSON y lo ha guardado en la base de datos.
  Esto puede tardar entre 10 y 60 segundos, dependiendo de la IA y la carga.

Entre esos dos momentos, el profesor puede cerrar la pestaña, hacer otra cosa o esperar mirando un indicador de progreso. El servidor no le necesita para nada.

---

## Concepto 2 — Colas de Tareas y Workers

### El problema que aparece cuando la asincronía no es suficiente

La asincronía resuelve el problema del servidor bloqueado. Pero genera uno nuevo:
¿quién hace realmente el trabajo?

Si delegas la corrección de 90 exámenes pero sigues siendo tú la única que corrige, los exámenes se apilan en tu mesa y los últimos tardan días.

Necesitas dos cosas:
1. Un lugar donde se acumulen ordenadamente los trabajos pendientes → **la Cola**
2. Personas (o procesos) que vayan cogiendo trabajos de esa cola y los ejecuten → **los Workers**

### La analogía de la cafetería

Imagina una cafetería con mucha cola a la hora del recreo.

**Sin sistema de cola (caótico):**
> Todos los alumnos se agolpan en la barra. El único barista intenta atender a todos a la vez. Se equivoca, se estresa, algunos alumnos se van sin café.

**Con cola + varios baristas (organizado):**
> Los alumnos hacen cola ordenada. Hay 3 baristas.
> El primero libre coge al siguiente de la cola.
> Los pedidos se procesan en orden, sin caos, sin bloqueos.

Tu sistema funciona igual:

```
Profesor sube examen
       ↓
   COLA (Redis)
   ┌────────────────────────┐
   │ Examen 1 (pendiente)   │
   │ Examen 2 (pendiente)   │
   │ Examen 3 (pendiente)   │
   └────────────────────────┘
       ↓          ↓         ↓
  Worker 1    Worker 2   Worker 3
  (procesando)(procesando)(libre → coge el siguiente)
       ↓
  Resultado guardado en base de datos
       ↓
  Profesor notificado
```

### ¿Qué es Redis en este sistema?

**Redis** es la cola física. Es una base de datos ultra-rápida que vive en memoria (no en disco) y está diseñada para gestionar listas de tareas pendientes.

Piensa en Redis como **la pizarra de la sala de profesores** donde aparecen los exámenes pendientes de corregir. Cualquier corrector que quede libre mira la pizarra y coge el siguiente.

Redis es tan rápido porque no guarda en disco — guarda en RAM. El precio es que,si el servidor se reinicia sin configuración adicional, la pizarra se borra.
Para el MVP esto es aceptable; para producción real, se configura persistencia.

### ¿Qué es Celery en este sistema?

**Celery** es el sistema de workers — los "correctores" que cogen tareas de la cola y las ejecutan.

Celery es un programa Python que:
1. Está constantemente mirando la cola de Redis
2. Cuando aparece una tarea nueva, la coge
3. La ejecuta (en nuestro caso: envía la imagen a la IA, valida el JSON, guarda el resultado)
4. Marca la tarea como completada
5. Vuelve a mirar la cola

Puedes tener **varios workers** ejecutándose a la vez (varios "correctores").
Si tienes 3 workers y llegan 30 exámenes, los 3 trabajan en paralelo y el tiempo total se divide entre 3.

### El flujo completo de una corrección

```
1. Profesor sube foto del examen desde la PWA
           ↓
2. FastAPI recibe el archivo
   → Responde inmediatamente: 202 Accepted + submission_id
   → Guarda el archivo en Cloudinary
   → Crea un registro en la base de datos con estado PENDING
   → Manda la tarea a la cola de Redis
           ↓
3. Un worker de Celery coge la tarea de Redis
   → Cambia el estado a ANALYZING
   → Envía la imagen a la IA (GPT-4o Vision o Claude)
   → Recibe el JSON de respuesta
   → Valida que el JSON tiene todos los campos requeridos (Pydantic)
   → Guarda el resultado en la base de datos
   → Cambia el estado a REVIEW
           ↓
4. El panel web del profesor detecta el cambio de estado
   → Muestra el análisis completo con los marcadores visuales
   → El profesor revisa, ajusta si necesita, y aprueba
   → El estado cambia a GRADED
   → El ChangeLog registra quién tomó la decisión final
```

---

### 🔑 La idea clave

> **Redis** es el buzón donde se depositan los trabajos pendientes.
>
> **Celery** son los trabajadores que recogen del buzón y ejecutan el trabajo.
>
> Juntos permiten que el servidor principal siga libre para recibir nuevas peticiones mientras el trabajo pesado ocurre en segundo plano, en paralelo, sin límite de espera.

---

### ✅ Prueba de comprensión 2

**Pregunta:** Si en un momento dado hay 10 exámenes en la cola y solo 2 workers activos, ¿qué ocurre con los 8 exámenes restantes?

**Respuesta correcta:**

Los 8 exámenes restantes esperan en la cola de Redis, en orden. Cuando uno de los 2 workers termina su examen actual, coge automáticamente el siguiente de la cola.
No se pierden, no se corrompen, no necesitan que nadie los gestione manualmente.

La cola garantiza que todos los exámenes se procesarán — solo es cuestión de tiempo.
Si necesitas más velocidad, añades más workers (más "correctores"). No tienes que cambiar nada más del sistema.

---

### ✅ Prueba de comprensión 3

**Pregunta:** Si el servidor se apaga repentinamente por un corte de luz mientras hay 10 exámenes en Redis esperando ser procesados, y Redis no está configurado para guardar en disco (persistencia), ¿qué ocurre con esos exámenes al volver la luz?

**Respuesta correcta:**

Los 10 exámenes **se pierden**. Como Redis guarda los datos en memoria RAM (para ser ultra-rápido), un apagón borra la "pizarra". Al reiniciar, la cola de Redis estará vacía.

Por eso, en un entorno de producción real, Redis se configura con mecanismos de persistencia (como snapshots o AOF) para guardar la memoria en disco periódicamente, o se usa un broker de mensajes diseñado para no perder datos como RabbitMQ. Para un MVP, la pérdida de datos en caso de caída del servidor suele ser un riesgo aceptable a cambio de simplicidad.

---

### ✅ Prueba de comprensión 4

**Pregunta:** Un profesor sube un examen y la API le devuelve inmediatamente un código `202 Accepted` con el `submission_id`. El profesor, ansioso, recarga la página cada segundo para ver si ya está. ¿Esto bloquea a Celery o a los workers que están corrigiendo el examen?

**Respuesta correcta:**

**No bloquea a los workers de Celery.** Las peticiones que hace el profesor para comprobar el estado (ej. `GET /submissions/{id}`) van a **FastAPI** (la secretaría). FastAPI simplemente consulta la base de datos para ver el estado ("sigue en PENDING" o "ya está en REVIEW") y le responde en milisegundos.

Celery sigue trabajando en segundo plano sin enterarse de que el profesor está recargando la página. Esta es precisamente la ventaja de separar la web (FastAPI) del procesamiento (Celery).

---

## Resumen de la Sesión 1

| Concepto | En una frase |
|---|---|
| **Síncrono** | El servidor espera a terminar antes de atender al siguiente |
| **Asíncrono** | El servidor dice "recibido" y sigue disponible para otros |
| **202 Accepted** | El código HTTP que dice "anotado, trabajando en ello" |
| **Cola (Redis)** | La lista ordenada de trabajos pendientes |
| **Worker (Celery)** | El proceso que coge trabajos de la cola y los ejecuta |
| **Estado de Submission** | PENDING → ANALYZING → REVIEW → GRADED |

---

## ¿Por qué esto importa en tu proyecto?

Tu app tiene exactamente el problema que resuelve la asincronía:

- La IA tarda entre 10 y 60 segundos por examen
- Un profesor puede subir 30 exámenes de golpe
- Varios profesores pueden usar la app a la vez

Sin asincronía y sin cola: el servidor colapsaría en el primer uso real.

Con asincronía y Celery + Redis: el sistema escala sin cambiar arquitectura.
Si mañana tienes 100 profesores usando la app, simplemente añades más workers.

---

## Próxima sesión (Sesión 2)

Tres conceptos nuevos:

1. **Object Storage (S3 / Cloudinary)** — por qué las imágenes no van en PostgreSQL
2. **Structured Outputs** — cómo obligar a la IA a devolver exactamente el JSON que necesitas
3. **Presigned URLs** — cómo el navegador puede subir una foto directamente al almacenamiento sin pasar por tu servidor

---

*Sesión 1 completada — Julio 2026 | QIA-Correction con Antigravity*
