# 🗺️ Plan de Trabajo — API de Corrección Formativa con IA
**Proyecto:** API de Corrección Formativa con IA (`api-correccion-formativa-ia-galicia`)  
**Perfil:** Programadora Junior Full-Stack — Alba Camiña García  
**Fecha de inicio:** Julio 2026  
**Estado:** Fase 0 — Diseño y preparación

---

> [!IMPORTANT]
> Este documento recoge todos los temas abiertos de la conversación de referencia y los organiza en un orden lógico de ejecución. Cada bloque tiene una sesión de trabajo asignada con Antigravity.

---

## 📝 Descripción del Proyecto

**API de Corrección Formativa con IA (`api-correccion-formativa-ia-galicia`)** es un motor de evaluación formativa multinivel y API educativa diseñada para asistir al docente que opera bajo el rigor pedagógico de los Decretos gallegos y del modelo finlandés (*Feed Forward* + Evaluación competencial cualitativa), el estándar de equidad y adaptaciones curriculares de la LOMLOE, y el máximo blindaje de privacidad técnica europea al nivel del *Datenschutz* alemán (Seudonimización pre-nube + *Human-in-the-Loop*). El sistema permite procesar **cualquier tipo de prueba evaluable** —desde fotos de exámenes manuscritos y murales o cartulinas de aula, hasta redacciones en texto digital o capturas/PDFs de presentaciones (ej. Canva o diapositivas)— para que modelos multimodales evalúen el contenido contra rúbricas docentes y normativas dinámicas (`JSONB`), devolviendo un análisis cualitativo estructurado con acciones inmediatas de mejora para el alumno.

El valor diferencial de la herramienta frente a otras opciones del mercado se basa en cuatro pilares pedagógicos:
- **Análisis formativo priorizado**: No solo da una nota, sino que clasifica las necesidades de mejora del alumno por nivel de urgencia (inmediata vs. a medio/largo plazo).
- **Feedback visual exacto**: Genera marcadores visuales con coordenadas exactas sobre la imagen del examen para que el profesor localice los errores al instante.
- **Desacoplamiento normativo**: La ley educativa se inyecta como una variable independiente desde la base de datos, lo que la hace inmune a cambios legislativos y adaptable a cualquier Comunidad Autónoma.
- **Equidad e inclusión (NEAE/DUA)**: Detecta y reporta faltas ortográficas o lingüísticas, pero excluye automáticamente su penalización en el cálculo de nota si el estudiante cuenta con adaptaciones configuradas por el docente (dislexia, TDAH, TEA) [D-023].

Por diseño y para cumplir con la **EU AI Act** y el **RGPD** al tratar datos de menores, la herramienta utiliza un modelo *Human-in-the-Loop*: la IA actúa exclusivamente como asistente (copiloto) que propone un borrador de corrección, recayendo siempre la aprobación y decisión final en el profesor.

### 🌍 Respaldo y Benchmarking Internacional (`[D-022]`, `[D-023]`, `[D-024]`)
El diseño y la viabilidad de **QIA-Correction** están directamente avalados por las prácticas y normativas de los ecosistemas educativos más rigurosos de Europa y el mundo:
- **Alemania (Privacidad por diseño / *Datenschutz*):** Al igual que herramientas punteras en colegios alemanes como *Fobizz*, nuestro sistema opera bajo una "cámara de exclusión pre-nube" que recorta cabeceras y seudonimiza los datos locales antes de cualquier subida, cumpliendo con las estrictas directrices de la *KMK* y los delegados de protección de datos de los *Länder*.
- **Países Nórdicos — Finlandia y Suecia (Evaluación cualitativa y equidad):** Siguiendo el modelo pedagógico de *Abitti* y *FeedbackFruits*, la IA se autoriza como copiloto formativo para liberar tiempo administrativo y dedicarlo a la tutoría individual humana con alumnos NEAE, priorizando calificaciones cualitativas competenciales congruentes con los Decretos 156/157/2022 de la Xunta de Galicia.
- **Reino Unido y EE.UU. (Acción inmediata y certeza):** Integración obligatoria de *Actionable Next Steps* (*Feed Forward* del modelo Hattie) y un *Confidence Score* que alerta visualmente cuando la caligrafía o respuesta requiere revisión humana prioritaria.

> [!IMPORTANT]
> **La combinación es imbatible:** usamos la legalidad y los criterios competenciales cualitativos de Galicia como cimiento (`marcos_evaluacion` en `JSONB`), e inyectamos las técnicas pedagógicas más avanzadas de Reino Unido y USA (*Next Steps* y *Confidence Score*) como superpoder del motor de IA. Es un producto redondísimo para presentar tanto en la AESIA como en cualquier instituto o entrevista de ingeniería EdTech.

### 📢 Argumentario Comercial y Ventajas Clave para el Profesorado (Marketing B2C/B2B)
El éxito de adopción de **QIA-Correction** por parte de docentes, orientadores y jefes de estudio se sustenta en cinco promesas de valor directas que resuelven sus dolores diarios reales:
1. **Ahorro masivo para humanizar la enseñanza:** QIA-Correction no sustituye al profesor ni quita autoridad; actúa como un copiloto que elimina hasta el 70% del tiempo burocrático de corrección mecánica en grupos de 30 alumnos. El docente recupera sus tardes y fines de semana para invertir ese tiempo en atención humana y tutoría directa con los estudiantes que más lo necesitan.
2. **El fin de la "caja negra" y del feedback inútil:** A diferencia de las correcciones genéricas ("mejorar redacción"), cada alumno recibe un **Siguiente Paso Accionable (*Feed Forward*)** que le dice exactamente qué acción única y realizable debe hacer hoy para progresar. Además, el docente visualiza un *Confidence Score* que le advierte cuándo una caligrafía confusa o respuesta ambigua requiere su inspección manual prioritaria.
3. **100% A prueba de inspección y normativa autonómica:** Todas las correcciones cualitativas se cruzan de forma nativa con los criterios y competencias de los **Decretos 156/2022 y 157/2022** y la **Orden de 26 de mayo de 2023 de la Xunta de Galicia**, además de garantizar la inclusión educativa de alumnos NEAE/NEE según la LOMLOE (`Decreto 229/2011`) sin que el docente tenga que hacer cálculos paralelos ni arriesgarse a penalizar por error a un alumno con dislexia.
4. **Privacidad blindada al nivel del *Datenschutz* alemán:** El profesorado y el centro pueden estar tranquilos: ninguna imagen con el nombre y apellidos del alumno llega a internet ni a los servidores de la nube o las empresas de IA. El recorte y la seudonimización pre-nube (`[D-022]`) garantizan un cumplimiento impecable del RGPD y de la LOPDGDD.
5. **Omni-canal y 100% Multimodal:** Un único motor para todo el aula. Corrige con el mismo rigor y en la misma interfaz los exámenes de papel fotografiados, los murales o cartulinas infográficas colgados en la pared y las entregas digitales o presentaciones en *Canva* o *Google Slides*.

---


## 🎯 Estrategia Personal y Objetivo Real

> [!CAUTION]
> **El objetivo principal a corto plazo NO es montar una empresa B2C, sino maximizar la empleabilidad.**

Dada la situación actual (subsidio de desempleo incompatible con el alta en autónomos), la comercialización temprana de la plataforma como SaaS individual supondría un riesgo financiero injustificado. Por tanto, la estrategia central del proyecto es la **construcción de un portfolio técnico de alto nivel**.

El valor real de QIA-Correction radica en demostrar a futuras empresas empleadoras que la desarrolladora domina:
1. **Arquitectura avanzada:** Uso de asincronía y colas de tareas (Celery + Redis) para evitar cuellos de botella.
2. **Integraciones complejas:** Modelos LLM multimodales (OpenAI/Anthropic) y OCR.
3. **Visión de negocio y legal:** Diseño de base de datos preparada para escalar y arquitectura *Human-in-the-Loop* que cumple con la normativa europea de Inteligencia Artificial (AI Act).

**Hoja de ruta estratégica:**
1. **Fase Ninja (Desarrollo):** Construir la Versión 1.0 manteniendo el subsidio. No hay alta de autónomos. Es formación práctica.
2. **Fase Demo:** Desplegar el proyecto de forma gratuita para usarlo como carta de presentación ante empresas, el contacto de la AESIA y en entrevistas técnicas.
3. **Fase Comercialización (Solo si aplica):** Si el proyecto genera una tracción orgánica masiva o un interés B2B (licenciamiento a colegios/EdTech), se procederá entonces al alta de autónomos y se pausará el subsidio, acudiendo a las vías de financiación.

### 💰 Financiación y Subvenciones (Solo en Fase de Comercialización)

En el momento en que se decida pausar el subsidio y darse de alta como autónoma para comercializar el producto, el perfil de la desarrolladora (mujer, >45 años, proyecto tecnológico IA) es altamente bonificable en España (2026):

- **Subsidio y Autónomos (Incompatibilidad):** El subsidio por cargas familiares es **incompatible** con el alta de autónomos (se suspende automáticamente, aunque se puede reanudar si el negocio cesa). *Nota: La compatibilidad de 270 días de trabajo por cuenta propia solo aplica al paro normal (prestación contributiva), no a este subsidio.*
- **Xunta de Galicia / Emprego e Igualdade — Ayudas Inicio de Actividad (>45 años mujeres):** Al darse de alta como autónoma en Galicia (A Coruña), se accede a la **Cuota Cero gallega** y a las subvenciones directas a fondo perdido de la línea *Emprego Autónomo* de la Xunta, que oscilan entre **4.000€ y 7.000€ a fondo perdido** (cuantía prioritaria máxima por ser mujer mayor de 45 años y desempleada empadronada en Galicia).
- **IGAPE (Instituto Galego de Promoción Económica) / Galicia Emprende:** Ayudas directas y líneas de préstamo bonificadas y participativas de la Xunta para proyectos de innovación y empresas de base tecnológica en Galicia.
- **ENISA Emprendedoras Digitales:** Préstamos participativos sin avales bancarios ni garantías personales (de 25.000€ a 1.500.000€), creados por el Ministerio de Economía específicamente para startups tecnológicas o digitales lideradas por mujeres de cualquier edad.
- **Activa Startups (EOI / Transformación Digital - Galicia):** Subvenciones a fondo perdido de hasta 40.000€ para el desarrollo o adopción de soluciones de Inteligencia Artificial en colaboración con PYMES gallegas.
- **GAIN (Axencia Galega de Innovación) y Programa NEOTEC (CDTI):** Subvenciones de hasta el 70% a fondo perdido enfocadas en la creación y consolidación de empresas de base tecnológica (EBT) y proyectos de IA en Galicia.

### 🤝 Incubación y Redes de Apoyo (Compatibles con Subsidio - Fase Desarrollo)

Mientras se programa en la sombra sin alta de autónomos (Fase Ninja), se puede y debe aplicar a programas de incubación y apoyo que no exigen ser empresa:

- **Red de Polos de Emprendemento e Apoio ao Emprego de Galicia (Xunta):** Red pública y gratuita por toda Galicia (centro en A Coruña y provincia) que no exige alta mercantil. Asignan tutores gratuitos para validar el modelo de negocio, te asisten en toda la tramitación de las ayudas directas de la Xunta (4.000€-7.000€) y ofrecen seguimiento personalizado.
- **Ciudad de las TIC / Ecosistema TIC de A Coruña y contacto AESIA:** A Coruña es la sede nacional de la **AESIA** (Agencia Española de Supervisión de la Inteligencia Artificial) y el hub tecnológico *Ciudad de las TIC* (clúster TIC de Galicia y viveros tecnológicos de la UDC y Xunta). Desarrollar y presentar la versión funcional desde A Coruña te sitúa en el centro neurálgico e institucional de la IA en España.
- **Programa Explorer (Banco Santander / CISE - Sede UDC A Coruña):** Programa formativo de pre-incubación de 12 semanas sin alta mercantil, con mentorías presenciales o virtuales desde A Coruña y acceso a red de contactos/inversores.
- **Programa Talento 45+ (Cámara de Comercio de A Coruña + SEPE):** Orientación, formación y planes de viabilidad a medida sin coste para mayores de 45 en A Coruña.
- **Generación SAVIA (Fundación Endesa):** Red nacional enfocada en la empleabilidad y emprendimiento del talento sénior (>45 y >50 años).
- **Fundación Mujeres / PAEM Galicia + Microcréditos MicroBank:** Asesoría gratuita y convenios bancarios en Galicia para acceder a micropréstamos de hasta 30.000€ sin avales personales ni garantías patrimoniales.
- **Innovación Abierta (DesafIA / Galicia Innova):** Concursos y retos para soluciones de Inteligencia Artificial aplicadas, aportando visibilidad, contactos y capital semilla sin riesgo personal.

---

## BLOQUE 0 — Lo que está decidido (No reabrir)

Estos puntos ya tienen consenso y no deben consumir más tiempo de análisis. Cada decisión está justificada en detalle en [`decisiones.md`](./decisiones.md).

| Decisión | Opción elegida | Motivo |
|---|---|---|
| Comunidad autónoma objetivo | **Galicia** (`seed` principal) | Coherencia con sede (A Coruña/AESIA) y testeo con docentes de la Xunta |
| Corrección manual vs IA | **Human-in-the-Loop** | Escudo legal bajo AI Act |
| Primer tipo de examen | **Texto plano (respuesta corta)** | Sin OCR en MVP |
| La normativa es | **Una variable (campo JSON en BBDD)** | Inmunidad a cambios legislativos |
| Alcance MVP | **1 asignatura, criterios genéricos** | Evitar sobreingeniería |
| **Modelo de negocio** | **B2C + B2B dual** | Misma API, dos canales: profesores directos y plataformas que contratan el motor |
| **Estrategia móvil MVP** | **PWA (Progressive Web App)** | Acceso a cámara sin app nativa; app nativa = Versión 2.0 |
| **Adaptaciones NEAE/NEE** | **Variable inyectada en prompt (`JSONB`)** | Excluye penalización por dislexia/TDAH sin ocultar el error detectado ([D-023]) |
| **Stack tecnológico** | **Python/FastAPI + React/Vite** | Ver Bloque 1 |

### Modelo de negocio dual explicado

```
B2C — Canal directo al profesor
   Profesora → descarga la PWA → escanea el examen → ve el análisis
   Modelo: freemium / suscripción mensual individual

B2B — Canal institucional / integración
   Colegio / plataforma EdTech → consume la API con su API key
   Modelo: licencia por volumen de correcciones / por centro
```

> [!NOTE]
> El diseño API-first hace esto natural: la PWA (B2C) y el cliente B2B consumen exactamente la misma API. No hay que construir dos sistemas — solo dos formas de acceder al mismo motor.

### Arquitectura de producto (visión oficial)

```
📱 PWA móvil — Capa 1 (B2C)
   Profesor escanea el examen con la cámara del móvil
            ↓
🔌 API Backend — Capa 2 (núcleo compartido B2C + B2B)
   Recibe imagen → procesa con IA → valida JSON con Pydantic
   Gestiona cola de tareas asíncrona (Celery + Redis)
   Normativa andaluza + rúbrica docente en PostgreSQL
            ↓
🖥️ Panel web — Capa 3 (B2C)     /     🏢 Integración — Capa 3 (B2B)
   Imagen + análisis en paralelo        JSON estructurado vía API key
   Marcadores visuales sobre errores    para plataformas externas
   Botón aprobación profesor (HitL)
```

---

## BLOQUE 0B — Estudio de Mercado (Análisis con datos reales, julio 2026)

> [!WARNING]
> Este análisis se basa en búsqueda web actualizada. El mercado EdTech de corrección con IA **ya existe y está activo en España**. La decisión de continuar con el proyecto debe tomarse con los ojos abiertos.

### 🌍 Panorama Global — Los grandes jugadores

| Herramienta | Especialidad | Mercado principal | Limitación clave |
|---|---|---|---|
| **Gradescope** (Turnitin) | STEM, exámenes manuscritos, rúbricas | Universidades anglosajonas | No adaptado a currículos europeos |
| **EssayGrader.ai** | Ensayos, rúbricas personalizadas, feedback | K-12 anglosajonos | Sin soporte LOMLOE ni legislación española |
| **Brisk Teaching** | Feedback en Google Docs en tiempo real | Anglosajón | Solo texto, no imagen |
| **Co-Grader** | Corrección asistida, Human-in-the-Loop | Universidades | Sin OCR de escritura manual |
| **MagicSchool AI** | Suite generalista (+60 herramientas) | Global | No localizado a normativa autonómica |

### 🇪🇸 Panorama España — Competidores directos (2025-2026)

| Herramienta | Qué hace | Fortaleza | Debilidad |
|---|---|---|---|
| **Examino** | Escanea manuscritos con QR (sin app), OCR de esquemas y fórmulas, genera comentarios | Muy fuerte en OCR, multidisciplinar | Sin análisis formativo por urgencia |
| **SmartGrade** | Rúbricas automáticas, integración con Google Classroom/Moodle | Integración LMS sólida | Enfocado en nota, no en análisis formativo |
| **Correctium** | Corrección por imagen/PDF, privacidad por defecto, informes de rendimiento | Anonimato sin datos personales | Sin OCR de escritura manuscrita propia |
| **correctorSofía** | OCR revisable + rúbricas del profesor + validación final | Human-in-the-Loop explícito | Producto menos maduro |
| **Maitic** | Corrección de redacciones manuscritas, marca errores sobre la imagen | Visualización de errores en imagen | Solo redacciones, no exámenes estructurados |
| **TutuTor.ai** | Genera exámenes y rúbricas por CC.AA. (LOMLOE) | Adaptado a currículo autonómico | Generación, no corrección |

### ⚖️ Qué existe y qué no existe todavía

**LO QUE YA EXISTE** (no reinventes esto):
- OCR de escritura manuscrita básica ✅
- Corrección por rúbrica con validación del profesor ✅
- Integración con LMS (Google Classroom, Moodle) ✅
- Informes de rendimiento por clase ✅
- Anonimización básica ✅

**LO QUE NO EXISTE en el mercado español:**
- Análisis cualitativo formativo **con niveles de urgencia** (inmediata vs. medio plazo) ❌
- **Marcadores visuales sobre la imagen** indicando exactamente dónde está cada error ❌
- **Desacoplamiento normativa/rúbrica docente** (la ley como variable JSON independiente) ❌
- Adaptación profunda a la normativa **por comunidad autónoma** (no solo LOMLOE genérica) ❌
- API abierta B2B para que terceros integren el motor ❌

### 📊 Conclusión

> [!IMPORTANT]
> **El proyecto tiene viabilidad real.** La propuesta de valor debe centrarse en: **análisis formativo por urgencia + marcadores visuales + normativa autonómica como variable**. Eso es lo que no existe.

---

## BLOQUE 1 — Stack Tecnológico ✅ CERRADO

| Capa | Tecnología | Equivalente conocido |
|---|---|---|
| **Backend / API** | Python + FastAPI | Como Fastify pero en Python |
| **Validación de datos** | Pydantic | Equivalente directo a Zod |
| **Base de datos** | PostgreSQL + SQLAlchemy | Igual que en QUANTIA |
| **Frontend / PWA** | React + Vite | Vite ya lo dominas; React es nuevo |
| **Cola de tareas** | Celery + Redis | Sin equivalente en QUANTIA — Bloque 2 |
| **Almacenamiento imágenes** | Cloudinary (MVP) → S3 (producción) | Sin equivalente — Bloque 2 |

---

## BLOQUE 2 — Conceptos Técnicos a Interiorizar (Sesiones 1-2)

### 2.1 — Síncrono vs. Asíncrono ✅ Explicado en Sesión 1
### 2.2 — Colas de Tareas y Workers (Celery + Redis) ✅ Explicado en Sesión 1
### 2.3 — Object Storage S3 / Cloudinary ✅ Explicado en Sesión 2
### 2.4 — Structured Outputs / Salidas Estructuradas ✅ Explicado en Sesión 2
### 2.5 — Presigned URLs ✅ Explicado en Sesión 2

---

## BLOQUE 3 — La Reunión con el Contacto de la AESIA (Sesión 3)

**Perfil del contacto:** Ingeniero en IA en AESIA (A Coruña). Ex Data Engineer (Hadoop, Spark, Python, AWS, Azure). Docente y artista.

### Las 3 preguntas que debes llevar preparadas

**Pregunta 1 — Pipeline:**
> "¿Me recomiendas un modelo multimodal que haga OCR + evaluación a la vez (GPT-4o Vision), o separar los dos pasos?"

**Pregunta 2 — Asincronía:**
> "¿Celery + Redis es suficiente para el MVP o hay una alternativa más sencilla para empezar?"

**Pregunta 3 — Regulación AI Act:**
> "Si la herramienta actúa como copiloto (el profesor tiene la última palabra), ¿qué nivel de anonimización exige la AESIA antes de enviar la imagen a OpenAI tratándose de datos de menores?"

---

## BLOQUE 4 — Aspectos Legales y Regulatorios (Sesión 4)

- RGPD y datos de menores — campo `alumno_id` seudonimizado, recorte local de cabeceras [Regla 9] y custodia en Cold Storage [D-021]
- AI Act — sistema de Alto Riesgo, Human-in-the-Loop como escudo [D-002]
- Zero Data Retention con OpenAI/Anthropic
- ChangeLog de auditoría mínimo requerido

---

## BLOQUE 5 — Diseño de Arquitectura y Base de Datos (Sesiones 5-6)

### Tablas principales
- `Profesor` — Usuario del sistema
- `Examen` — Prueba evaluable
- `Pregunta` — Ítem (TEST, DESARROLLO, PRESENTACIÓN)
- `Marco_Evaluacion` — Normativa andaluza como JSONB
- `Rubrica_Docente` — Criterios del profesor
- `Submission` — Entrega (PENDING → ANALYZING → REVIEW → GRADED) con campos `alumno_id` y `archivos_urls` (JSONB multi-folio)
- `Evaluacion` — JSON completo de resultado IA
- `ChangeLog` — Auditoría

### JSON de salida (contrato con la IA)
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

---

## BLOQUE 6 — Servicios a Contratar (Sesión 7)

| Servicio | Proveedor MVP | Coste |
|---|---|---|
| Motor IA / LLM | Anthropic (Claude) o OpenAI (GPT-4o) | ~2-5€/mes en pruebas |
| Object Storage | Cloudinary Free Tier | Gratis en desarrollo |
| Hosting servidor | Railway o Render | 5€/mes o gratis |
| Base de datos | Railway (incluido) o Docker local | Gratis en desarrollo |

---

## BLOQUE 7 — Programa de Versiones (Sesión 8)

| Versión | Qué hace | Objetivo |
|---|---|---|
| **0.1** | API recibe texto plano, rúbrica hardcoded, devuelve JSON | Validar que la IA estructura bien |
| **0.2** | PostgreSQL + ORM, normativa como JSONB, rúbrica editable | Normativa como variable dinámica |
| **0.3** | Subida de imágenes, modelo multimodal, OCR real | Primer examen corregido desde foto |
| **0.4** | Celery + Redis, estados de Submission, notificación al cliente | 5 exámenes simultáneos sin colapso |
| **0.5** | Panel dual React, marcadores visuales, botón HitL | Producto demostrable a un profesor |
| **1.0** | Anonimización, ChangeLog, README Compliance, desplegado | Portfolio — Fase Demo (presentar a empresas y AESIA) |

---

## BLOQUE 8 — Portfolio y GitHub

> [!IMPORTANT]
> El repositorio en GitHub se abre **al arrancar el código (v0.1)**, no al terminar. Un historial de commits desde el día uno es parte de la narrativa de portfolio — demuestra proceso, no solo resultado final.

- **Apertura del repo:** al iniciar v0.1 — repo público desde el primer commit
- README profesional con arquitectura, motivación y capturas
- Sección `## AI Development Methodology` — aparece desde **v0.1** (ver desarrollo completo abajo)
- Sección `## Compliance & EU AI Act Readiness` — aparece solo en **v1.0** (RGPD, AI Act, seudonimización [Regla 9], retención legal en Cold Storage [D-021] y HitL [D-002] ya implementados)
- Commits semánticos: `feat:`, `fix:`, `refactor:`, `docs:`
- Ramas por versión: `v0.1-sync-engine`, `v0.2-database`, etc.

### 🧠 Marco narrativo: cómo presentar el desarrollo asistido por IA

> [!IMPORTANT]
> El riesgo no es haber usado agentes de IA. El riesgo es no poder explicar lo que hay detrás. La narrativa correcta no es defensiva — es técnicamente precisa.

**Posición correcta:**
> *"Diseñé la arquitectura y los contratos del sistema. Usé agentes de IA como herramienta de implementación, igual que otros developers usan frameworks o generadores de código. Cada decisión de diseño es mía y puedo defenderla."*

**Los 4 elementos que debe contener la sección `## AI Development Methodology` en el README:**

| Elemento | Qué documenta | Ejemplo concreto en este proyecto |
|---|---|---|
| **Qué diseñé yo** | Decisiones de arquitectura, contratos, reglas de negocio | Estructura HitL, contrato JSON de salida de la IA, desacoplamiento de normativa como JSONB, pipeline asíncrono |
| **Qué ejecutaron los agentes** | Implementación de lo diseñado | Código Python de los endpoints, modelos Pydantic, tests unitarios |
| **Cómo validé** | Proceso de revisión y control | Criterios de aceptación del backlog, smoke test del contrato JSON (v0.1-000), tests automáticos |
| **Qué aprendí** | Reflexión técnica honesta | Limitaciones del LLM en la generación de JSON estructurado, gestión de cuota, flujo de trabajo con agentes |

**Lenguaje a usar vs. evitar:**

| ❌ Evitar | ✅ Usar en su lugar |
|---|---|
| *"La IA lo hizo todo"* | *"Los agentes implementaron la arquitectura que yo diseñé"* |
| *"Usé IA para acelerar"* | *"Trabajo con un stack de desarrollo orquestado con agentes"* |
| *"El código fue revisado manualmente"* | *"Cada decisión de diseño tiene criterios de aceptación documentados en el backlog"* |
| *"No sé si esto es correcto pero lo generó la IA"* | [No decir esto jamás — si no puedes defenderlo, no lo subas] |

---

## BLOQUE 9 — Tooling de Desarrollo ✅ CONFIGURADO (08/07/2026)

### Entorno de ejecución
- **Sistema operativo:** Windows 11 + WSL (Ubuntu) — todo el código Python/FastAPI corre en WSL
- **Editor:** VS Code con workspace apuntando a `C:\Users\34636\Desktop\qia-correction`

### Agentes de IA disponibles

| Herramienta | Dónde vive | Modelos disponibles | Rol en el proyecto |
|---|---|---|---|
| **Antigravity** | VS Code (Windows) | Claude Sonnet | Arquitectura, decisiones complejas, revisiones críticas, documentación |
| **OpenCode** | Terminal WSL | Ver tabla inferior | Código rutinario, estructura de archivos, boilerplate, edición en terminal |

### Modelos disponibles en OpenCode

| Proveedor | Modelo | Quota | Cuándo usarlo |
|---|---|---|---|
| Google | `gemini-2.5-flash` ⭐ **default** | 1.500 req/día gratis | Tareas rápidas, edición, refactors simples |
| Groq | `llama-3.3-70b-versatile` | Generosa, gratis | Código Python complejo, debugging |
| Groq | `qwen/qwen3-32b` | Generosa, gratis | Python, lógica de negocio |
| Groq | `openai/gpt-oss-120b` | Generosa, gratis | Problemas difíciles, diseño de prompts |
| OpenCode | `deepseek-v4-flash-free` | Sin límite | Fallback sin API key |

> [!NOTE]
> Cambiar de modelo en OpenCode: `Ctrl+X` → `M` para abrir el selector, o `F2` para ciclar entre recientes.

### Herramientas descartadas y por qué

| Herramienta | Motivo de descarte |
|---|---|
| **Cursor** | Redundante — Antigravity y OpenCode escriben el código; Cursor solo aporta autocomplete para escritura manual |
| **v0 by Vercel** | Pospuesto a v0.5 — útil para generar componentes React, sin valor en fases 0.1-0.4 de backend puro |

> [!IMPORTANT]
> **Regla de gestión de cuota:** usar OpenCode+Groq para tareas mecánicas (crear archivos, escribir funciones, tests). Reservar Antigravity/Sonnet para arquitectura, revisiones y decisiones de diseño.

### Estructura de carpetas y gestión de contexto

```
qia-correction/                              ← workspace único de VS Code
├── api_correccion_plan.md                   ← planificación y arquitectura
├── backlog.md                               ← historias de usuario con criterios de aceptación
├── sesion_01_asincronia_y_colas.md          ← ✅ Síncrono/Asíncrono · Celery + Redis
├── sesion_02_storage_y_structured_outputs.md← ✅ Object Storage · Structured Outputs · Presigned URLs
├── decisiones.md                            ← registro ADR de todas las decisiones del proyecto
├── glosario.md                              ← términos técnicos explicados en castellano
├── AGENTS.md                                ← contexto persistente para OpenCode (creado con /init)
└── backend/                                 ← todo el código Python
    ├── main.py
    ├── routers/
    ├── models/
    └── services/
```

### Reglas de trabajo con Antigravity

1. **Plan primero** — antes de ejecutar cualquier cambio, se presenta qué se va a hacer y qué archivos se van a tocar. Sin aprobación, no se actúa.
2. **Documentar siempre** — si un cambio afecta al stack, backlog, arquitectura o entorno, se refleja en el documento correspondiente antes de cerrar la tarea.
3. **Comprobar dependencias** — verificar que ningún otro documento o historia quede inconsistente tras un cambio.
4. **Explicar los conceptos** — cuando aparece un concepto nuevo, se explica en el momento: analogía primero, tecnicismo después.
5. **Navaja de Ockham** — siempre la solución y explicación más sencilla que resuelva el problema. Sin complejidad innecesaria.
6. **Sin siglas solas** — cualquier acrónimo se escribe con su nombre completo entre paréntesis la primera vez que aparece. Ejemplo: ADR (Architecture Decision Records — Registro de Decisiones de Arquitectura).
7. **Glosario vivo** — cada término técnico nuevo que aparezca en el proyecto se añade a `glosario.md` con su explicación en castellano.
8. **Credenciales nunca en el código** — ninguna API key, contraseña o dato sensible se escribe directamente en un archivo `.py` o cualquier archivo que vaya al repositorio. Siempre van en `.env` (que está en `.gitignore`). Los bots escanean GitHub continuamente: una clave expuesta puede generar facturas de miles de euros en minutos.
9. **Datos personales nunca expuestos (seudonimización en nube)** — ningún dato personal o nombre de menor se sube a internet ni al repositorio. En BBDD: los alumnos se identifican solo por `alumno_id`. En la nube y la IA: la imagen se recorta localmente antes de subirse a Cloudinary/S3 o enviarse al LLM. Ninguna imagen original con el nombre real toca la nube ni se conserva tras la subida. Con los proveedores de IA: contratos de Zero Data Retention.
10. **Respuestas concisas** — sin repetir lo que el usuario ya sabe, sin introducciones, sin conclusiones que resumen lo dicho. Las explicaciones con analogía son bienvenidas cuando el concepto lo requiere — la analogía aporta valor. Resumir lo obvio no.
11. **Output de tests mínimo** — los scripts y tests imprimen solo lo imprescindible para validar el resultado. Sin volcar JSON completos en terminal salvo que sea necesario para depurar. Usar resúmenes (`✅ campo X presente`) en lugar de dumps completos.

---

**Regla de contexto en Antigravity** — abrir en VS Code solo los archivos relevantes para la tarea en curso:

| Tarea | Archivos a tener abiertos |
|---|---|
| Planificación / arquitectura | Solo los `.md` de documentación |
| Revisión de código específico | El archivo `.py` concreto + `backlog.md` |
| Sesión de código completa | `backend/` activo + `backlog.md` |
| Nunca | Todos los archivos a la vez |

**Contexto de OpenCode:** se gestiona con `AGENTS.md` en la raíz. OpenCode lo lee automáticamente al arrancar. Se genera una sola vez con `/init` y se actualiza cuando cambia la arquitectura del proyecto.

---

## Calendario Orientativo

> [!NOTE]
> La **reunión con el contacto de la AESIA** es una oportunidad puntual, no un paso bloqueante del roadmap. Se puede producir en cualquier momento del desarrollo. El BLOQUE 3 documenta las preguntas a llevar preparadas; la reunión en sí se agenda cuando haya disponibilidad. **La apertura del repositorio en GitHub** se hace al arrancar el código (v0.1), no al finalizar el proyecto — el repo público desde el primer commit es parte de la narrativa de portfolio.

| Sesión | Bloque | Contenido | Estado |
|---|---|---|---|
| ✅ | Bloque 1 | Stack tecnológico — CERRADO | 💬 Antigravity |
| ✅ | Bloque 2 | Síncrono/Asíncrono + Colas de tareas | 💬 Antigravity |
| ✅ | Bloque 2 | Object Storage + Structured Outputs + Presigned URLs | 💬 Antigravity |
| ✅ | Bloque 9 | Entorno de desarrollo configurado (WSL + OpenCode + Gemini + Groq) | 🛠️ Completado |
| — | Bloque 3 | **Preparación preguntas reunión AESIA** (leer BLOQUE 3 del plan) | 📋 Pendiente |
| ⭐ | — | **Reunión con contacto AESIA** *(fecha libre, no bloqueante)* | 🤝 Cuando haya disponibilidad |
| 🚀 | — | **Apertura repo en GitHub + primera línea de código — v0.1** | 🖥️ OpenCode + Antigravity |
| — | Bloque 4 | Marco legal: RGPD, AI Act, trazabilidad | 💬 Antigravity |
| — | Bloque 5 | Diseño del modelo de datos | 💬 Antigravity |
| — | Bloque 5 | JSON de salida y pipeline asíncrono | 💬 Antigravity |
| — | Bloque 6 | Servicios y configuración de entorno | 💬 Antigravity |
| — | Bloque 7 | Programa de versiones definitivo | 💬 Antigravity |
| — | Bloque 8 | Portfolio/README profesional (v1.0) | 💬 Antigravity |

---

## APÉNDICE — Backlog de Ideas Futuras (Post-MVP)

### 🎮 UX, Gamificación y Fidelización
- Panel de tiempo ahorrado ("Este mes has recuperado X horas")
- Progreso de batch al corregir una tanda
- Evolución de clase por competencia a lo largo del trimestre
- Reutilización de rúbricas propias
- Modo oscuro

### 👩‍🎓 Portal del Alumno
- Acceso por código de clase generado por el profesor
- Vista de su propia corrección (solo lectura)
- Historial de evolución personal
- Marco legal: LOPDGDD art. 7, consentimiento parental para menores de 14

### 📱 App Nativa (Versión 2.0)
- React Native sobre el código React de la PWA
- App Store + Google Play
- Notificaciones push, escáner optimizado, modo offline parcial

### 💳 Sistema de Monetización y Pagos (Stripe)
- Integración de pasarela de pago para modelo B2C (suscripción mensual de profesores)
- Gestión de API Keys y facturación por uso para clientes B2B (colegios/EdTech)
- Lógica de límites (tier freemium vs. tier premium)
- Anuncios de Google Ads

---

*Documento generado el 07/07/2026 — Antigravity para Alba Camiña García*  
*Actualizado el 08/07/2026 — BLOQUE 9 reescrito con entorno real desplegado*  
*Actualizado el 09/07/2026 — sincronizadas reglas de trabajo (9, 10, 11), modelo multi-folio archivos_urls, compresión en cliente [D-020] y retención en Cold Storage [D-021]*
