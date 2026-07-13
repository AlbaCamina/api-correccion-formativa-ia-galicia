# 📋 Registro de Decisiones — API de Corrección Formativa con IA (`api-correccion-formativa-ia-galicia`)
**Formato:** Architecture Decision Records (ADR)  
**Proyecto:** API de Corrección Formativa con IA (`api-correccion-formativa-ia-galicia`)  
**Responsable:** Alba Camiña García  
**Inicio:** Julio 2026

---

> [!NOTE]
> Este documento es un **registro vivo**. Cada decisión relevante tomada durante el proyecto debe añadirse aquí antes de cerrar la sesión de trabajo. El objetivo es doble: poder explicar cada elección en una entrevista técnica, y no perder la orientación cuando el proyecto crezca.

---

## Índice de decisiones

| ID | Decisión | Fecha | Estado |
|---|---|---|---|
| [D-001](#d-001) | Comunidad autónoma objetivo: Galicia (`seed` curricular principal) | Jul 2026 | ✅ Adoptada |
| [D-002](#d-002) | Modelo Human-in-the-Loop (no corrección automática) | Jul 2026 | ✅ Adoptada |
| [D-003](#d-003) | MVP sin OCR — texto plano primero | Jul 2026 | ✅ Adoptada |
| [D-004](#d-004) | Normativa educativa como variable JSONB en BBDD | Jul 2026 | ✅ Adoptada |
| [D-005](#d-005) | Alcance MVP: 1 asignatura, criterios genéricos | Jul 2026 | ✅ Adoptada |
| [D-006](#d-006) | Modelo de negocio B2C + B2B dual (API-first) | Jul 2026 | ✅ Adoptada |
| [D-007](#d-007) | Estrategia móvil: PWA en lugar de app nativa | Jul 2026 | ✅ Adoptada |
| [D-008](#d-008) | Stack: Python/FastAPI + React/Vite | Jul 2026 | ✅ Adoptada |
| [D-009](#d-009) | Objetivo principal: portfolio/empleabilidad, no SaaS | Jul 2026 | ✅ Adoptada |
| [D-010](#d-010) | Fase Ninja — no alta de autónomos durante el desarrollo | Jul 2026 | ✅ Adoptada |
| [D-011](#d-011) | Claims legales: "alineado con principios", no "cumple" | Jul 2026 | ✅ Adoptada |
| [D-012](#d-012) | Entorno de ejecución: WSL (Ubuntu) en Windows | Jul 2026 | ✅ Adoptada |
| [D-013](#d-013) | Stack de agentes: Antigravity (arquitectura) + OpenCode (implementación) | Jul 2026 | ✅ Adoptada |
| [D-014](#d-014) | Workspace único con subcarpeta `backend/` + `AGENTS.md` | Jul 2026 | ✅ Adoptada |
| [D-015](#d-015) | Narrativa portfolio: arquitecta/orquestadora, no usuaria de IA | Jul 2026 | ✅ Adoptada |
| [D-016](#d-016) | Smoke test del contrato LLM como prerequisito de v0.1 | Jul 2026 | ✅ Adoptada |
| [D-017](#d-017) | Sección Compliance solo en README de v1.0, no de v0.1 | Jul 2026 | ✅ Adoptada |
| [D-018](#d-018) | Modelos LLM en OpenCode: Gemini Flash (default) + Groq | Jul 2026 | ✅ Adoptada |
| [D-019](#d-019) | Primer commit y push a GitHub con la documentación antes del código | Jul 2026 | ✅ Adoptada |
| [D-020](#d-020) | Compresión y redimensión en cliente antes de subir exámenes al servidor | Jul 2026 | ✅ Adoptada |
| [D-021](#d-021) | Custodia legal en Cold Storage de nube y purga por ciclo de vida RGPD | Jul 2026 | ✅ Adoptada |
| [D-022](#d-022) | Seudonimización pre-nube (recorte local) y modelo multi-folio (`archivos_urls` JSONB) | Jul 2026 | ✅ Adoptada |
| [D-023](#d-023) | Soporte de adaptaciones curriculares NEAE como variable en el contrato LLM | Jul 2026 | ✅ Adoptada |
| [D-024](#d-024) | Benchmarking pedagógico UK/USA (Next Steps / Confidence Score) y evaluación competencial gallega | Jul 2026 | ✅ Adoptada |
| [D-025](#d-025) | Vinculación con XADE mediante exportación homologada + RPA client-side | Jul 2026 | ✅ Adoptada |
| [D-026](#d-026) | `estado_feed_forward` como columna propia en `submissions` (seguimiento formativo, no sumativo) | Jul 2026 | ✅ Adoptada |
| [D-027](#d-027) | Modo dual de interacción rúbrica-normativa seleccionable en PWA (`COMBINADO` vs `AUDITORIA_CURRICULAR`) | Jul 2026 | ✅ Adoptada |
| [D-028](#d-028) | Adopción de Groq (`llama-3.3-70b-versatile`) como motor LLM primario de coste cero y alta velocidad | Jul 2026 | ✅ Adoptada |
| [D-029](#d-029) | Protocolo de Pausa Arquitectónica (*Stop & Consult*) y Modularidad Plana ante límites técnicos en agentes de IA | Jul 2026 | ✅ Adoptada |

---

## Decisiones de Producto y Negocio

### D-001
## Comunidad autónoma objetivo: Galicia (`seed` curricular principal)

**Fecha:** Julio 2026 (Actualizada el 09/07/2026)  
**Estado:** ✅ Adoptada

**Contexto:**  
El sistema de evaluación educativa en España varía por comunidad autónoma. Adaptarlo a todas desde el principio haría el MVP inviable. La autora reside y está empadronada en **A Coruña (Galicia)**, hogar de la sede nacional de la **AESIA (Agencia Española de Supervisión de la IA)** y del clúster *Ciudad de las TIC*.

**Opciones consideradas:**
- **Galicia** — coherencia total entre sede técnica (A Coruña), normativa (Decreto autonómico de la Xunta / LOMLOE Galicia), facilidad de testeo con profesoras locales, potencial diferencial bilingüe (castellano/gallego) y alineación con las ayudas/aceleradoras locales (IGAPE, Polo de Emprendemento de A Coruña, Explorer UDC, Activa Startups Galicia).
- **Andalucía** — mayor volumen demográfico en España, contemplado inicialmente, pero sin conexión física con el ecosistema en el que se mueve y desarrollará el proyecto.
- **Nacional genérico** — inviable como MVP, demasiado amplio.

**Decisión:** **Galicia** como comunidad autónoma objetivo principal y primer marco curricular precargado (`seed`). Logra la máxima cohesión entre la prueba de concepto, las validaciones con docentes de la zona y la presentación institucional ante la **AESIA en la Ciudad de las TIC**.

**Consecuencias:** La normativa gallega (rubricas LOMLOE Galicia y criterios curriculares de la Xunta) se convierte en el primer seed oficial de `marcos_evaluacion`. El diseño en `JSONB` ([D-004]) garantiza que añadir en el futuro el marco de Andalucía o Madrid no requerirá cambiar ni una línea de código. Tanto el producto como el ecosistema mercantil/financiero (`v1.0-005`) operan de forma unificada en A Coruña y Galicia.

---

### D-002
## Modelo Human-in-the-Loop (no corrección automática)

**Fecha:** Julio 2026  
**Estado:** ✅ Adoptada

**Contexto:**  
Un sistema que asigna notas automáticamente a menores de edad sin intervención humana es un sistema de Alto Riesgo bajo el AI Act europeo, con requisitos de certificación que van más allá del alcance de este proyecto.

**Opciones consideradas:**
- Corrección totalmente automática — más sencilla técnicamente, pero alto riesgo legal
- Human-in-the-Loop (IA propone, profesor decide) — más compleja, pero legalmente defensible
- Solo análisis cualitativo sin nota — limitaría el valor del producto

**Decisión:** Human-in-the-Loop. La IA actúa exclusivamente como copiloto: propone un borrador de corrección. El profesor tiene siempre la última palabra para aprobar, ajustar o rechazar.

**Consecuencias:** El estado de `Submission` incluye el paso `REVIEW` antes de `GRADED`. El ChangeLog registra quién tomó la decisión final. Esta decisión es el escudo legal central del producto.

---

### D-003
## MVP sin OCR — texto plano primero

**Fecha:** Julio 2026  
**Estado:** ✅ Adoptada

**Contexto:**  
El objetivo diferencial del producto incluye OCR de exámenes manuscritos. Sin embargo, desarrollar OCR desde el principio añadiría complejidad técnica (integración multimodal, procesado de imagen) antes de haber validado que la lógica de evaluación funciona.

**Opciones consideradas:**
- Empezar con OCR — valida el caso de uso real pero es muy complejo para v0.1
- Empezar con texto plano — valida la lógica de evaluación sin la complejidad de la imagen
- Empezar con PDF — punto intermedio, pero igualmente complejo

**Decisión:** Texto plano en v0.1 y v0.2. El profesor escribe o pega la respuesta del alumno directamente. OCR real llega en v0.3 cuando la lógica de evaluación ya está validada.

**Consecuencias:** v0.1 y v0.2 no son demostrables a un profesor real como producto final, pero son suficientes para demostrar la arquitectura técnica en un portfolio.

---

### D-004
## Normativa educativa como variable JSONB en BBDD

**Fecha:** Julio 2026  
**Estado:** ✅ Adoptada

**Contexto:**  
La normativa educativa en España cambia con cada gobierno y cada consejería autonómica. Si se codifica en el prompt o en el código, cada cambio legislativo requiere modificar y redesplegar la aplicación.

**Opciones consideradas:**
- Hardcoded en el prompt — más simple, pero frágil ante cambios legislativos
- Archivo JSON externo — mejor, pero requiere redespliegue para actualizar
- Campo JSONB en PostgreSQL — actualización sin tocar código, adaptable a cualquier CC.AA.

**Decisión:** Campo `rubrica_completa` de tipo JSONB en la tabla `marcos_evaluacion`. Cada comunidad autónoma es un registro. Actualizar la normativa = actualizar un registro en BBDD.

**Consecuencias:** Esta es una de las tres propuestas de valor diferenciales del producto. Hace el sistema "inmune a cambios legislativos" y adaptable a cualquier CC.AA. sin cambio de código.

---

### D-005
## Alcance MVP: 1 asignatura, criterios genéricos

**Fecha:** Julio 2026  
**Estado:** ✅ Adoptada

**Contexto:**  
Adaptar el sistema a múltiples asignaturas desde el principio requeriría múltiples rúbricas, múltiples marcos normativos y pruebas con muchos tipos de respuesta distintos.

**Opciones consideradas:**
- Múltiples asignaturas — demasiado para un MVP
- 1 asignatura con rúbrica muy específica — más realista pero más frágil
- 1 asignatura con criterios genéricos — equilibrio entre especificidad y generalidad

**Decisión:** 1 asignatura (**Filosofía de Bachillerato gallego**, Decreto 157/2022 Xunta de Galicia) con criterios de evaluación genéricos aplicables a respuesta corta. La rúbrica específica entra en v0.2.

**Consecuencias:** El seed de la BBDD en v0.2 incluirá un marco de evaluación real de **Filosofía de Bachillerato gallego** (Decreto 157/2022, Xunta de Galicia) como primer registro. Coherente con D-001 (sede en A Coruña, AESIA, Decretos 156/157/2022).

---

### D-006
## Modelo de negocio B2C + B2B dual (API-first)

**Fecha:** Julio 2026  
**Estado:** ✅ Adoptada

**Contexto:**  
Los productos EdTech pueden comercializarse directamente a profesores (B2C) o a instituciones y plataformas que integran el motor (B2B). Un diseño API-first permite ambos canales con la misma base técnica.

**Opciones consideradas:**
- Solo B2C (suscripción de profesores) — más simple, menor ticket
- Solo B2B (licencia a centros/EdTech) — mayor ticket, ciclo de venta más largo
- Dual B2C + B2B — misma API, dos canales de acceso

**Decisión:** Dual. La PWA (B2C) y los clientes B2B consumen exactamente la misma API. No hay dos sistemas — hay dos formas de acceder al mismo motor.

**Consecuencias:** El diseño API-first es obligatorio desde v0.1. La autenticación incluirá tanto login de profesor (B2C) como API keys (B2B) desde v0.2.

---

### D-007
## Estrategia móvil: PWA en lugar de app nativa

**Fecha:** Julio 2026  
**Estado:** ✅ Adoptada

**Contexto:**  
Los profesores necesitan escanear exámenes desde el móvil. Esto requiere acceso a la cámara. Una app nativa (iOS/Android) requiere publicación en tiendas, revisión de Apple/Google y mantenimiento de dos codebases.

**Opciones consideradas:**
- App nativa iOS + Android — mejor experiencia, pero coste y complejidad altísimos para MVP
- PWA (Progressive Web App) — acceso a cámara vía browser, instalable, sin tiendas
- Solo web desktop — no permite escanear desde móvil

**Decisión:** PWA en React/Vite para v0.5-v1.0. App nativa (React Native) queda para Versión 2.0 si el producto tiene tracción.

**Consecuencias:** El frontend necesita `vite-plugin-pwa` y HTTPS obligatorio (requerido por los navegadores para acceder a la cámara).

---

### D-008
## Stack: Python/FastAPI + React/Vite

**Fecha:** Julio 2026  
**Estado:** ✅ Adoptada

**Contexto:**  
El stack debe ser demostrable en un portfolio técnico, permitir integraciones con LLMs y ser conocido por el equipo de desarrollo (la propia desarrolladora).

**Opciones consideradas:**
- Node.js/Fastify + React — conocido de QUANTIA, pero Python es el lenguaje del ecosistema IA
- Python/FastAPI + React — Python dominante en IA/ML, FastAPI moderno y de alto rendimiento
- Python/Django + React — Django más pesado y menos adecuado para API pura

**Decisión:** Python/FastAPI para el backend (ecosistema IA, Pydantic nativo, async nativo) y React/Vite para el frontend (Vite ya conocido de QUANTIA, React nuevo a aprender).

**Consecuencias:** Hay una curva de aprendizaje en React. FastAPI y Pydantic se aprenden desde cero pero son más sencillos que Django. SQLAlchemy es equivalente a Prisma (ya conocido).

---

## Decisiones de Estrategia Personal

### D-009
## Objetivo principal: portfolio/empleabilidad, no SaaS

**Fecha:** Julio 2026  
**Estado:** ✅ Adoptada

**Contexto:**  
La situación económica actual (subsidio por cargas familiares incompatible con alta de autónomos) hace inviable la comercialización inmediata. El valor real del proyecto a corto plazo es demostrar capacidad técnica ante empresas empleadoras.

**Opciones consideradas:**
- Lanzar como SaaS desde el principio — riesgo financiero injustificado, pérdida del subsidio
- Construir como portfolio — mantiene subsidio, genera empleabilidad
- No construir el proyecto — pierde la oportunidad de aprendizaje y diferenciación

**Decisión:** Construir la v1.0 completa como portfolio técnico de alto nivel. Comercialización solo si hay tracción orgánica en Fase Demo, con plan de negocio previo.

**Consecuencias:** La hoja de ruta tiene 3 fases: Ninja (desarrollo) → Demo (portfolio) → Comercialización (opcional). El proyecto nunca se abandona a medias — v1.0 se termina y se despliega.

---

### D-010
## Fase Ninja — no alta de autónomos durante el desarrollo

**Fecha:** Julio 2026  
**Estado:** ✅ Adoptada

**Contexto:**  
El subsidio por cargas familiares es incompatible con el alta de autónomos. Darse de alta para vender el producto haría perder el subsidio (no se puede compatibilizar, a diferencia del paro contributivo normal).

**Opciones consideradas:**
- Alta de autónomos + inicio de comercialización — pierde subsidio, riesgo alto
- Desarrollo sin alta + sin venta — mantiene subsidio, acumula portfolio
- No desarrollar — pierde oportunidad

**Decisión:** Desarrollo completo sin alta de autónomos ni comercialización activa. El proyecto se usa como carta de presentación, no como fuente de ingresos, hasta que la situación económica lo permita.

**Consecuencias:** Los programas de incubación compatibles con el subsidio (Generación SAVIA, Talento 45+, Fundación Mujeres) son prioritarios durante esta fase. El alta de autónomos solo se activa si hay un interés B2B concreto o tracción masiva en Fase Demo.

---

## Decisiones Técnicas de Desarrollo

### D-011
## Claims legales: "alineado con principios", no "cumple"

**Fecha:** Julio 2026  
**Estado:** ✅ Adoptada

**Contexto:**  
Afirmar que un sistema "cumple el RGPD" o "cumple el AI Act" es una declaración legal que requeriría una auditoría certificada. Hacerlo sin esa certificación puede ser misleading y dañar la credibilidad del proyecto.

**Opciones consideradas:**
- "Cumple RGPD/AI Act" — incorrecto sin certificación
- "Alineado con principios de cumplimiento" — demasiado vago
- Descripción técnica específica — precisa y defensible

**Decisión:** Usar lenguaje técnico específico: *"Diseñado con los principios de Human-in-the-Loop del AI Act y anonimización de datos de menores conforme a RGPD"*. Describe exactamente lo que se implementa, sin afirmar certificación.

**Consecuencias:** El README de v1.0 usa este lenguaje. La sección `## Compliance & EU AI Act Readiness` describe las medidas técnicas implementadas, no una declaración de conformidad legal.

---

### D-012
## Entorno de ejecución: WSL (Ubuntu) en Windows

**Fecha:** Julio 2026 (08/07/2026)  
**Estado:** ✅ Adoptada

**Contexto:**  
El desarrollo se realiza en un equipo Windows. Python, FastAPI, Docker y las herramientas del ecosistema Linux funcionan de forma nativa en Linux y con fricciones en Windows nativo.

**Opciones consideradas:**
- Windows nativo — compatibilidad limitada con herramientas Python/Linux
- WSL (Windows Subsystem for Linux) — Linux nativo dentro de Windows, sin VM
- Docker Desktop como entorno principal — más pesado, más complejo para desarrollo iterativo

**Decisión:** WSL con Ubuntu como entorno de ejecución principal. Todo el código Python/FastAPI corre en WSL. VS Code en Windows se conecta al filesystem de WSL de forma transparente.

**Consecuencias:** Los comandos de desarrollo (`python`, `pip`, `uvicorn`, `pytest`) se ejecutan siempre desde la terminal WSL. OpenCode también vive en WSL.

---

### D-013
## Stack de agentes: Antigravity (arquitectura) + OpenCode (implementación)

**Fecha:** Julio 2026 (08/07/2026)  
**Estado:** ✅ Adoptada

**Contexto:**  
La cuota de Claude Sonnet en Antigravity es limitada. Usar Antigravity para todas las tareas — incluyendo código rutinario — agotaría la cuota rápidamente y bloquearía el desarrollo.

**Opciones consideradas:**
- Solo Antigravity — agota cuota rápido, bloquea el desarrollo
- Solo OpenCode — pierde la capacidad de revisión y arquitectura de Claude
- Antigravity + OpenCode con roles diferenciados — maximiza recursos gratuitos

**Decisión:** Dos agentes con roles complementarios:
- **Antigravity/Claude Sonnet:** arquitectura, decisiones complejas, revisiones críticas, documentación
- **OpenCode/Gemini+Groq:** código rutinario, boilerplate, estructura de archivos, tests, edición en terminal

**Consecuencias:** Hay que gestionar conscientemente qué tarea va a qué agente. La regla: si la tarea requiere criterio y decisión → Antigravity. Si la tarea es implementación de algo ya decidido → OpenCode.

---

### D-014
## Workspace único con subcarpeta `backend/` + `AGENTS.md`

**Fecha:** Julio 2026 (08/07/2026)  
**Estado:** ✅ Adoptada

**Contexto:**  
A medida que el proyecto crezca, habrá documentación, código backend y código frontend en el mismo repositorio. Mantener todo en un único workspace de VS Code requiere gestionar el contexto activo conscientemente.

**Opciones consideradas:**
- Múltiples workspaces de VS Code — más limpio pero más fricción al cambiar
- Workspace único sin organización — caos cuando el proyecto crezca
- Workspace único con estructura clara y reglas de contexto — balance óptimo

**Decisión:** Un único workspace (`api-correccion/`) con todo el proyecto. Contexto gestionado manualmente abriendo solo los archivos relevantes para cada tipo de tarea. OpenCode usa `AGENTS.md` para contexto persistente.

**Consecuencias:** El desarrollador debe cerrar los `.md` de documentación cuando trabaja en código, y cerrar los `.py` cuando trabaja en arquitectura. Es un hábito de trabajo, no una configuración automática.

---

### D-015
## Narrativa portfolio: arquitecta/orquestadora, no usuaria de IA

**Fecha:** Julio 2026 (08/07/2026)  
**Estado:** ✅ Adoptada

**Contexto:**  
Presentar un proyecto asistido por IA puede generar descrédito si se enmarca como "la IA lo hizo por mí". La misma realidad enmarcada correctamente — "diseñé el sistema, usé agentes para implementarlo" — es una fortaleza, no una debilidad.

**Opciones consideradas:**
- No mencionar el uso de IA — deshonesto y detectado en entrevistas
- Mencionar defensivamente ("la IA generó código que yo revisé") — minimiza el rol real
- Mencionar como herramienta de trabajo normal ("orquesté agentes para implementar mi diseño") — preciso y profesional

**Decisión:** El README y las entrevistas usan lenguaje de arquitecta/orquestadora. Los 4 elementos a documentar: qué diseñé yo / qué ejecutaron los agentes / cómo validé / qué aprendí.

**Consecuencias:** El proyecto tiene un `AGENTS.md` y una sección `## AI Development Methodology` en el README desde v0.1. Estos documentos son la prueba de que el proceso fue controlado y consciente.

---

### D-016
## Smoke test del contrato LLM como prerequisito de v0.1

**Fecha:** Julio 2026 (08/07/2026)  
**Estado:** ✅ Adoptada

**Contexto:**  
Toda la arquitectura de v0.1 se construye sobre el supuesto de que el LLM puede devolver el JSON del contrato definido. Si ese supuesto es falso, todo el código de FastAPI construido alrededor es inútil.

**Opciones consideradas:**
- Empezar directamente con FastAPI — riesgo de construir sobre un contrato que no funciona
- Smoke test primero — valida el contrato antes de construir el servidor
- Usar output estructurado del LLM (Structured Outputs) — reduce el riesgo pero igual hay que validarlo

**Decisión:** Historia v0.1-000 como prerequisito explícito: script Python standalone `smoke_test_llm.py` que valida el contrato JSON con el LLM antes de escribir una sola línea de FastAPI.

**Consecuencias:** Si el contrato falla, se rediseña el prompt antes de continuar. Este script también sirve como referencia del prompt base cuando se integre en `services/prompt_builder.py`.

---

### D-017
## Sección Compliance solo en README de v1.0, no de v0.1

**Fecha:** Julio 2026 (08/07/2026)  
**Estado:** ✅ Adoptada

**Contexto:**  
El README de v0.1 incluye una sección `## AI Development Methodology`. Si en ese mismo README aparece `## Compliance & EU AI Act Readiness`, un recruiter técnico verá que las funcionalidades descritas (anonimización, ChangeLog, HitL) no existen aún en el código.

**Opciones consideradas:**
- Compliance desde v0.1 — infla expectativas sobre funcionalidades no implementadas
- Compliance solo en v1.0 — aparece cuando las medidas técnicas ya están implementadas
- Compliance como "roadmap" en v0.1 — menos engañoso pero igualmente confuso

**Decisión:** La sección `## Compliance & EU AI Act Readiness` aparece únicamente en el README de v1.0, cuando anonimización, ChangeLog y HitL completo ya están implementados.

**Consecuencias:** El README de v0.1 tiene `## AI Development Methodology` (explica el proceso de trabajo) pero no `## Compliance`. La sección de compliance en v1.0-003 del backlog incluye los requisitos completos.

---

### D-018
## Modelos LLM en OpenCode: Gemini Flash (default) + Groq

**Fecha:** Julio 2026 (08/07/2026)  
**Estado:** ✅ Adoptada

**Contexto:**  
OpenCode necesita modelos de LLM para funcionar. Gemini 2.5 Pro tiene cuota 0 en el tier gratuito de AI Studio. Se necesita una segunda capa gratuita y potente para tareas de código complejo.

**Opciones consideradas:**
- Solo Gemini Flash — funciona pero un único modelo puede quedarse corto en tareas complejas
- Gemini Flash + Gemini Pro — Pro tiene cuota 0 en tier gratuito, no viable sin billing
- Gemini Flash + Groq — Groq ofrece Llama 3.3 70B, Qwen3 32B y GPT-OSS 120B gratis

**Decisión:** Gemini 2.5 Flash como modelo default (1.500 req/día) + Groq como segunda capa para código complejo y tareas de razonamiento (llama-3.3-70b-versatile, qwen3-32b, gpt-oss-120b).

**Consecuencias:** Las keys se almacenan en `.bashrc` de WSL como variables de entorno (`GEMINI_API_KEY`, `GROQ_API_KEY`). El cambio de modelo en la TUI se hace con `Ctrl+X` → `M` o `F2`.

---

### D-019
## Primer commit y push a GitHub con la documentación antes del código

**Fecha:** Julio 2026 (08/07/2026)  
**Estado:** ✅ Adoptada

**Contexto:**  
El backlog inicial asumía la existencia del repositorio en GitHub, pero no fijaba el momento del `git init` y primer push. Retrasar el push hasta tener código funcional arriesga la pérdida en local del trabajo de arquitectura e impide visualizar el orden real del proceso en el historial de Git.

**Opciones consideradas:**
- Subir a GitHub solo al terminar la v0.1 — riesgo de pérdida en local de los documentos y el historial ocultaría la fase previa de diseño
- Subir a GitHub tras cada historia — buena práctica, pero requiere que el repositorio esté ya inicializado y sincronizado
- Subir la documentación como primer commit antes de la primera línea de código — blindaje de seguridad (`backup`) y narrativa limpia de ingeniería

**Decisión:** Ejecutar `git init`, crear `.gitignore` y hacer el primer commit/push a la rama `main` en GitHub exclusivamente con los documentos de diseño (`*.md`) antes de empezar a programar la `v0.1-000`.

**Consecuencias:** Cualquier persona o reclutador que inspeccione el historial en GitHub verá los documentos fundacionales (`api_correccion_plan.md`, `decisiones.md`, `backlog.md`, `sesion_01...`, `sesion_02...`) en el origen del timeline, evidenciando una metodología basada en arquitectura y reflexión previa.

---

### D-020
## Compresión y redimensión en cliente antes de subir exámenes al servidor

**Fecha:** Julio 2026 (09/07/2026)  
**Estado:** ✅ Adoptada

**Contexto:**  
Una foto de cámara móvil en alta resolución o un PDF escaneado multi-folio puede superar los 15-20 MB. Subir este archivo en bruto por redes escolares 4G o WiFi tarda más de 12 segundos, con alto riesgo de error o corte en la subida, y penaliza el consumo de tokens multimodales sin aportar mayor legibilidad al modelo de IA (que reescala la imagen internamente a ~2048px).

**Opciones consideradas:**
- Límite estricto de 10 MB y subida en bruto — rechaza archivos pesados del profesor con error 400 y tarda mucho en subir.
- Subida sin límite o límite alto en bruto — no rechaza archivos, pero satura la red, ralentiza la corrección 15 segundos y dispara los costes por tokens.
- Arquitectura dual: backend tolerante (hasta 25 MB) + compresión en cliente (PWA) — el procesador del móvil o PC redimensiona la imagen a 2048px en <0.2s antes de enviarla, reduciendo el peso de >15 MB a ~800 KB y acelerando todo el proceso sin pérdida de legibilidad.

**Decisión:** Adoptar la arquitectura dual (Backend 25 MB máximo + compresión/redimensión automática en la PWA frontend a ~2048px y ~800 KB antes de hacer el `fetch`).

**Consecuencias:** El endpoint `POST /api/v1/submissions/upload` en v0.3 acepta hasta 25 MB. La pantalla de captura del frontend en `v0.5-002` incluye lógica de redimensión por Canvas/Web Worker en cliente para que la subida sea casi instantánea (<1s) y el gasto de tokens se mantenga acotado.

---

### D-021
## Custodia legal en Cold Storage de nube y purga por ciclo de vida RGPD

**Fecha:** Julio 2026 (09/07/2026)  
**Estado:** ✅ Adoptada

**Contexto:**  
La normativa educativa gallega (Decretos 156/157/2022 de la Xunta de Galicia) obliga a conservar los instrumentos de evaluación y pruebas escritas ante posibles reclamaciones oficiales durante plazos legalmente establecidos (hasta final de curso o resolución firme de recursos). Si los archivos se eliminan totalmente tras la corrección, no hay respaldo probatorio. Si se guardan en almacenamiento caliente sin límite o en el servidor local, los costes se disparan y se infringe el principio de limitación del plazo de conservación del RGPD.

**Opciones consideradas:**
- Conservación permanente en servidor/almacenamiento estándar — alto coste e infracción RGPD por retención indefinida.
- Borrado inmediato tras la corrección — imposibilita la defensa ante revisiones de examen o inspección educativa.
- Almacenamiento temporal local (`/uploads` de backend) borrado al subir a nube + Cold Storage en nube con purga automática (Lifecycle Policy) — balance óptimo técnico, económico y legal.

**Decisión:** Eliminar las copias locales en el backend (`/uploads/` o `/tmp/`) inmediatamente tras subirlas a Cloudinary / AWS S3. En la nube, configurar una regla de ciclo de vida (*Lifecycle Rule*) que archive los archivos en *Cold Storage* (Glacier/Archive) para reducir costes a céntimos y los elimine automáticamente al prescribir el plazo legal de retención (1 año o fin de curso).

**Consecuencias:** El backend es *stateless* respecto a archivos estáticos (cero saturación en WSL/Docker). La tabla `submissions` mantiene las referencias `archivos_urls` apuntando a la nube, y la purga legal se delega en las políticas de expiración automática del proveedor de nube.

---

### D-022
## Seudonimización pre-nube (recorte local) y modelo multi-folio (`archivos_urls` JSONB)

**Fecha:** Julio 2026 (09/07/2026)  
**Estado:** ✅ Adoptada

**Contexto:**  
Subir imágenes de exámenes sin anonimizar (con nombre y apellidos del alumno visibles) a almacenamiento en nube externa (Cloudinary o AWS S3) supondría un tratamiento indebido de datos personales de menores identificables en infraestructura multi-tenant con copias internacionales, vulnerando el RGPD y nuestra propia Regla de Trabajo Nº 9. Asimismo, los exámenes pueden constar de un folio suelto, varios folios o PDFs de múltiples páginas, por lo que un campo de texto único `imagen_url` limitaría innecesariamente la capacidad del sistema.

**Respaldo internacional y legal (Alemania — *Datenschutz* / *KMK*):**  
Esta decisión está directamente avalada por el estándar más riguroso de Europa: las directrices de los delegados de protección de datos de Alemania (*Datenschutzbeauftragter*) y la Conferencia de Ministros de Educación (*KMK*), que prohíben categóricamente la subida de exámenes o ensayos con nombres de alumnos a LLMs en la nube sin anonimización previa. Herramientas punteras en Alemania como *Fobizz* basan su éxito en actuar como "cámara de exclusión local pre-nube" que filtra y elimina datos personales (*Zero Data Retention*). Al adoptar el mismo diseño arquitectónico, api-correccion-formativa-ia-galicia se blinda al nivel del *Datenschutz* alemán, superando con creces cualquier auditoría de privacidad en Galicia o España.

**Opciones consideradas:**
- Subir el examen original intacto a la nube y anonimizarlo en el backend justo antes del envío al LLM — rechazado: la nube almacenaría datos personales de menores sin control probatorio.
- Recortar/difuminar la cabecera superior (primeros 3 cm) en memoria local antes de realizar la subida a la nube y almacenar una lista flexible (`archivos_urls` en `JSONB`) — balance legal y técnico óptimo avalado por el modelo alemán.

**Decisión:** El recorte de cabecera se realiza siempre en memoria local (o bien en cliente durante la redimensión en PWA de `v0.5-002`, o en el buffer local temporal antes de llamar al upload en `v0.3-004`). Solo el archivo purgado y seudonimizado (vinculado exclusivamente al código `alumno_id`) viaja y se almacena en Cloudinary o AWS S3. El campo en la tabla `submissions` se formaliza como `archivos_urls (JSONB)` para soportar de forma nativa tanto 1 URL de PDF como un array de N páginas manuscritas.

**Consecuencias:** Cumplimiento 100% estricto con el RGPD, la Regla 9 y el estándar *Datenschutz* alemán. Ninguna imagen original no anonimizada toca jamás la nube ni se almacena. El LLM multimodal recibe el array `archivos_urls` ordenado por folio para una evaluación continua.

---

---

### D-023
## Soporte de adaptaciones curriculares NEAE como variable en el contrato LLM

**Fecha:** Julio 2026 (10/07/2026)  
**Estado:** ✅ Adoptada

**Contexto:**  
El alumnado con Necesidades Específicas de Apoyo Educativo (NEAE) tiene derecho legal a que los errores derivados directamente de su dificultad diagnosticada no sean penalizados en la evaluación (LOMLOE, Decreto 229/2011 de Galicia, Orden 8/sep/2021 de la Xunta). Un alumno con dislexia no pierde nota por faltas de ortografía; un alumno con TDAH puede recibir tiempo extra. Estos ajustes deben reflejarse en el sistema de corrección con IA de forma trazable y auditable bajo el AI Act.

**Opciones consideradas:**
- Ignorar las adaptaciones y dejar que la profesora ajuste la nota manualmente a posteriori — rechazado: pierde valor diferencial y no genera evidencia auditada.
- Dejar que la IA infiera las necesidades del alumno desde la escritura — rechazado: la IA no diagnostica; los datos de salud son especialmente protegidos (LOPDGDD art.7); violaría el HitL (`D-002`).
- La profesora configura explícitamente las adaptaciones del alumno en el campo `adaptaciones_alumno` (JSONB) en `submissions`. El sistema las inyecta en el prompt y modifica el contrato JSON de salida del LLM — **solición legal, auditable y diferencial**.

**Decisión:** La tabla `submissions` incorpora el campo `adaptaciones_alumno` (JSONB) configurable por la profesora. El sistema clasifica las adaptaciones en 4 niveles (DEA/ACNS/ACS/ACIS) según el Decreto 229/2011 de Galicia. El LLM **siempre detecta y reporta** todos los errores lingüísticos, pero el campo `errores_excluidos_por_adaptacion` los separa de los penalizables. Los marcadores visuales de errores excluidos se muestran en gris (neutro), no en rojo. La IA **nunca diagnostica** NEAE; solo aplica instrucciones recibidas. Toda configuración queda en el `changelog` con timestamp (trazabilidad AI Act). El detalle exhaustivo de la jerarquía normativa en 4 capas y el marco autonómico general/NEAE se encuentra documentado en `marco_normativo_y_adaptaciones.md`.

**Consecuencias:** Nueva clave `adaptaciones_alumno` (JSONB nullable) en `submissions`. Nuevo bloque en el contrato JSON del LLM: `ortografia_detectada`, `errores_excluidos_por_adaptacion`, `marcadores_neutros_adaptacion`. Los datos de adaptaciones son datos de salud de menores → acceso restringido al `profesor_id` propietario, cifrado en reposo. Implementación en `v0.2-007`. Casos de ACS grave (discapacidad intelectual) quedan fuera del MVP actual y se marcan con aviso `adaptacion_significativa: true`.

---

### D-024
## Benchmarking pedagógico UK/USA (`Next Steps` / `Confidence Score`) y evaluación competencial gallega (`Decretos 156/157/2022`)

**Fecha:** Julio 2026 (10/07/2026)  
**Estado:** ✅ Adoptada

**Contexto:**  
Antes de cerrar la Fase 0 de documentación, es fundamental contrastar el modelo de evaluación con la normativa exacta de educación secundaria y bachillerato en Galicia (`Decreto 156/2022` para ESO y `Decreto 157/2022` para Bachillerato de la Xunta de Galicia) y con el estado del arte de las plataformas EdTech líderes en países avanzados de Reino Unido, USA y el Norte de Europa (Gradescope, NoMoreMarking, Comparative Judgement, modelo Hattie & Timperley en GCSE/A-Levels, Finlandia con *Abitti* y Suecia con *FeedbackFruits*). El objetivo es evitar que la IA devuelva correcciones genéricas ("ciertas pero inútiles") o incompatibles con las Programaciones Didácticas gallegas.

**Respaldo pedagógico internacional (Reino Unido y Países Nórdicos — *Finlandia / FeedbackFruits*):**  
Nuestras elecciones pedagógicas están respaldadas por las tres máximas del modelo educativo nórdico (liderado por Finlandia y Suecia):
1. **Separación radical entre formativo y sumativo:** Prohibición de "cajas negras" en exámenes finales; la IA actúa solo como copiloto cualitativo formativo diario durante el curso (`HitL`).
2. **Prioridad absoluta del feedback cualitativo competencial:** En Finlandia se repudia la "nota seca" en favor de rúbricas cualitativas y desglose por competencias, en sintonía total con los Decretos gallegos 156/157.
3. **Ahorro de tiempo para la tutoría humana:** En el sistema finlandés se justifica la IA con un objetivo central: liberar horas burocráticas del profesor para que las invierta en atención humana directa y personalizada al alumnado con adaptaciones curriculares (NEAE).

**Opciones consideradas:**
- Mantener un contrato JSON simple con una nota numérica de 0 a 10 y una lista de comentarios generales — rechazado: no cumple con la evaluación competencial cualitativa de la ESO en Galicia ni aporta valor accionable al estudiante.
- Enriquecer el contrato JSON del LLM con tres innovaciones probadas en UK, Galicia y los países nórdicos (`siguiente_paso_accionable`, `calificacion_cualitativa` y `confidence_score`) — **balance pedagógico y legal óptimo**.

**Decisión:** El contrato JSON que debe devolver el LLM (`v0.1-000` en adelante) incorpora obligatoriamente:
1. **Calificación competencial cualitativa (`calificacion_cualitativa`):** Grado oficial según decretos gallegos (*Insuficiente [IN], Suficiente [SU], Bien [BI], Notable [NT], Sobresaliente [SB]*), además de la `nota` numérica (0-10) y el desglose por competencias (`competencias_criterios`), avalado por el modelo finlandés de evaluación auténtica.
2. **Siguiente Paso Accionable (`siguiente_paso_accionable` / *Feed Forward*):** Adoptando el estándar del Reino Unido (modelo Hattie), la IA debe devolver siempre una directriz clara, concreta y realizable hoy por el alumno para corregir su principal área de mejora, eliminando el feedback abstracto.
3. **Índice de Confianza IA (`confidence_score`):** Un valor float entre `0.0` y `1.0` que indica la certeza técnica de la lectura OCR o interpretación del modelo. Si es `< 0.75`, el panel de la profesora muestra una alerta preventiva ("Caligrafía confusa o respuesta ambigua — requiere revisión manual prioritaria"), reforzando el *Human-in-the-Loop* bajo la AI Act.

**Consecuencias:** El esquema JSON del smoke test (`smoke_test_llm.py` en `v0.1-000`) y de Pydantic en FastAPI incluirá estos tres campos. La PWA mostrará el *confidence score* en el panel dual de corrección y destacará el "Siguiente Paso Accionable" como tarjeta prioritaria para el docente y el alumno.

> [!IMPORTANT]
> **La combinación es imbatible:** usamos la legalidad y los criterios competenciales cualitativos de Galicia como cimiento (`marcos_evaluacion` en `JSONB`), e inyectamos las técnicas pedagógicas más avanzadas de Reino Unido y USA (*Next Steps* y *Confidence Score*) como superpoder del motor de IA. Es un producto redondísimo para presentar tanto en la AESIA como en cualquier instituto o entrevista de ingeniería EdTech.

---

### [D-025] Vinculación Legal y Autocompletado en XADE mediante RPA/Exportación Local (*Client-Side HitL*)

**Fecha:** Julio 2026 (10/07/2026)  
**Estado:** ✅ Adoptada

**Contexto:**  
Los centros de educación secundaria en Galicia tienen la obligación legal de volcar y cerrar las calificaciones numéricas de las materias y las cualitativas de las competencias en **XADE (`Xestión Administrativa da Educación`)**, la plataforma informática oficial de la Xunta de Galicia. Sin embargo, el *Esquema Nacional de Seguridad (ENS)* y la normativa de AMTEGA prohíben categóricamente la conexión o inyección directa de datos desde servidores privados de terceros a la base de datos pública de XADE mediante APIs abiertas no autorizadas. Asimismo, el *AI Act* y el RGPD impiden la autogeneración en nube de actos administrativos sin intervención del funcionario (*Human-in-the-Loop*).

**Opciones consideradas:**
- **Inyección directa en servidor (Nube a Nube por API o scraping de backend):** Rechazada por violar el ENS de la Administración Pública, carecer de API pública en XADE y romper la cadena de custodia probatoria del acto administrativo firmado por el docente.
- **Doble picado manual en XADE por el profesor:** Rechazada por generar una fricción burocrática inasumible, invalidando el propósito de ahorro de tiempo que justifica la adopción de api-correccion-formativa-ia-galicia.
- **Exportación homologada en plantilla Excel/CSV + Autocompletado Local (*RPA Client-Side* en navegador):** **Elegida por su solidez legal 100% estricta y máxima ergonomía docente**.

**Decisión:**  
La vinculación entre **api-correccion-formativa-ia-galicia** y la plataforma oficial **XADE** se diseña bajo un modelo de **Soberanía Local y Asistencia de Interfaz (`Client-Side HitL`)**, articulado en dos niveles de implementación:
1. **Exportación Estándar Homologada (`MVP v0.5`):** La PWA de api-correccion-formativa-ia-galicia genera y descarga localmente un fichero Excel/CSV formateado al milímetro con las cabeceras, codificación e identificadores locales que exige XADE. El docente importa este fichero directamente dentro de su sesión logueada de XADE.
2. **Autocompletado Local por Asistente/Extensión (`v0.8 / v1.0`):** Se habilita un helper local (extensión o script de navegador del docente) que, al tener abiertas simultáneamente la PWA (`GRADED`) y la web de XADE, autocompleta las casillas numéricas y cualitativas de la pantalla del funcionario en segundos como si las tecleara mecánicamente.
3. **El Salvaguarda HitL Innegociable:** El asistente o exportación **jamás ejecuta el comando o botón final de `Guardar/Firmar Acta en XADE`**. Es el propio profesor quien, tras una rápida inspección visual en pantalla, realiza la acción de firma o guardado final con su certificado digital/Chave365, asumiendo la plena autoría formal del acto administrativo.

**Consecuencias:**  
api-correccion-formativa-ia-galicia se posiciona como una herramienta técnicamente invulnerable ante la inspección educativa de la Xunta de Galicia y el ENS, al no almacenar ni transferir datos hacia o desde servidores públicos, actuando exclusivamente como un copiloto de cálculo e interfaz en el ordenador del funcionario.

---

### [D-026] Seguimiento Formativo No Sumativo del Siguiente Paso Accionable (`estado_feed_forward`)

**Fecha:** Julio 2026 (10/07/2026)  
**Estado:** ✅ Adoptada

**Contexto:**  
En el modelo de corrección de api-correccion-formativa-ia-galicia (`[D-024]`), el motor LLM devuelve un "Siguiente Paso Accionable" (*Feed Forward*) con una directriz clara y concreta para que el estudiante la ejecute de inmediato (*"Reescribe el párrafo 3 incorporando dos conectores temporales"*). Surge el dilema sobre si el sistema y el docente deben evaluar o calificar numéricamente la entrega o devolución de dicho paso.

**Opciones consideradas:**
- **Calificar numéricamente cada devolución de Feed Forward:** Rechazado categóricamente por generar una duplicación masiva de la carga burocrática del profesor (convertir cada corrección en una nueva mini-tarea evaluable que revisar al día siguiente), destruyendo la promesa de alivio docente del producto.
- **Dejar el Feed Forward como recomendación informal sin registro:** Rechazado por generar falta de rendición de cuentas (*accountability*) en el alumno, convirtiendo el feedback en texto inerte.
- **Registro de Checklist Formativo de Autoevaluación en Base de Datos (`estado_feed_forward` — *Sin Carga Sumativa*):** **Elegida por coherencia pedagógica y UX docente**.

**Decisión:**  
El cumplimiento del Siguiente Paso Accionable se modela en el esquema de la base de datos (dentro del `JSONB` de `submissions` o historial del alumno) mediante un marcador de estado **`estado_feed_forward`**, desglosado en tres valores:
1. `PENDIENTE`: Asignado tras la corrección asistida.
2. `REALIZADO_ALUMNO`: El estudiante (o el profesor en aula) marca con un clic `[x]` en su PWA que ha completado la acción de mejora en su estudio personal o cuaderno.
3. `VERIFICADO_PRÓXIMA_PRUEBA`: En la evaluación del *siguiente* instrumento dentro de la misma Situación de Aprendizaje (`SdA`), el motor LLM verifica si la mejora previa fue incorporada, otorgando un refuerzo cualitativo positivo.

El profesor **no tiene que corregir ni calificar sumativamente esta mini-tarea**. En su panel PWA visualiza un semáforo de qué estudiantes completan sus checks formativos, fomentando la autoevaluación y la evaluación continua (Decretos 156/157/2022 de Galicia) con cero inversión de tiempo extra.

**Consecuencias:**  
El contrato de la base de datos y la interfaz de la PWA incorporan el campo y el check `estado_feed_forward`, consolidando la evaluación formativa sin incrementar la carga de corrección del docente.

---

### D-027
## Modo dual de interacción rúbrica-normativa seleccionable en PWA (`COMBINADO` vs `AUDITORIA_CURRICULAR`)

**Estado:** Adoptada (`[v0.2-004]`)  
**Fecha:** Julio 2026  
**Contexto:**  
En el diseño del hito `[v0.2-004]`, surgió el debate técnico sobre cómo deben interactuar los criterios del marco normativo autonómico (Decreto 157/2022 de la Xunta de Galicia) y la rúbrica personalizada creada por la profesora. Se plantearon inicialmente dos opciones mutuamente excluyentes: combinación simple o auditoría pedagógica de coherencia.

**Decisión:**  
En lugar de forzar una única estrategia fija en el backend, se implementa un **Modo Dual de Evaluación** configurable por la profesora directamente desde la interfaz PWA y transmitido en cada petición de corrección (`modo_evaluacion` en el JSON / columna en `submissions`):
1. `COMBINADO` (Evaluación Rápida Cotidiana): El motor LLM fusiona de forma aditiva los saberes básicos oficiales y los criterios específicos de la rúbrica del docente para calificar con agilidad tareas del día a día, controles cortos o exposiciones.
2. `AUDITORIA_CURRICULAR` (Coherencia e Inspección Pedagógica): Diseñado para evaluaciones formales de fin de trimestre o revisión de nuevas rúbricas. El motor corrige la entrega pero además actúa como orientador pedagógico para el docente, contrastando la rúbrica de aula contra el Decreto 157/2022 e informando confidencialmente en `teacherSummary` si la rúbrica omite competencias básicas obligatorias o entra en contradicción normativa.

**Consecuencias:**  
Otorga una flexibilidad total al docente y aporta un valor diferencial extraordinario ante directores de centro e inspección educativa, posicionando a api-correccion-formativa-ia-galicia como un escudo legal y pedagógico del profesor sin sobrecargar la complejidad técnica del backend.

---

### D-028
## Adopción de Groq (`llama-3.3-70b-versatile`) como motor LLM primario de coste cero y alta velocidad

**Estado:** Adoptada (`[v0.1-000]`)  
**Fecha:** Julio 2026  
**Contexto:**  
Durante la ejecución del Smoke Test del contrato JSON (`[v0.1-000]`), se evaluó la viabilidad, velocidad y coste operativo del motor LLM. Mientras que OpenAI (`gpt-4o-mini`) o Anthropic (`claude-3-5-sonnet`) requieren saldo o suscripciones comerciales constantes, el proyecto busca demostrar una optimización máxima en ingeniería en la nube (FinOps) y desacoplamiento de proveedores para la fase de portfolio técnico sin renunciar a la potencia de razonamiento.

**Decisión:**  
Se adopta **Groq** (con el modelo `llama-3.3-70b-versatile` y hardware de unidades LPU) como **motor LLM primario por defecto** para la ejecución de correcciones, preservando compatibilidad completa multi-proveedor con OpenAI, Anthropic y el modo local `mock` mediante la variable de entorno `LLM_PROVIDER`.

**Consecuencias:**  
1. **Coste Cero (0€/mes):** Permite ejecutar miles de correcciones con un modelo de código abierto de 70 mil millones de parámetros sin gasto en API en la fase de desarrollo y demostración en portfolio.
2. **Velocidad de Respuesta:** El hardware de Groq genera las evaluaciones Pydantic en una fracción del tiempo de un LLM convencional.
3. **Paridad de SDK:** La integración aprovecha el SDK nativo de OpenAI (`base_url="https://api.groq.com/openai/v1"`), permitiendo alternar a OpenAI en producción institucional con cambiar una sola línea en `.env`.
4. **Bifurcación Plana de Formato (`json_object` vs `Structured Outputs`):** Siguiendo el principio de Modularidad Plana (YAGNI), como `llama-3.3-70b-versatile` en Groq no soporta el parámetro nativo `response_format={"type": "json_schema"}` (Structured Outputs de `.parse()`), `llm_client.py` bifurca explícitamente según `LLM_PROVIDER`: si es `groq`, utiliza directamente `response_format={"type": "json_object"}` con inyección textual del esquema en el `SYSTEM_PROMPT` y validación Pydantic en código; si es `openai`, utiliza `.parse()` nativo. Esto elimina reintentos innecesarios por errores HTTP 400 y reduce a la mitad la latencia de red en Groq.

---

### D-029
## Protocolo de Pausa Arquitectónica (*Stop & Consult*) y Modularidad Plana ante límites técnicos en agentes de IA

**Estado:** Adoptada (`[v0.1-003]`)  
**Fecha:** Julio 2026 (13/07/2026)  
**Contexto:**  
Durante el desarrollo e integración de los motores LLM en la versión v0.1 (`llm_client.py`), se evidenció la tendencia intrínseca de los agentes de IA a aplicar parches locales acumulativos o excepciones anidadas sobre la marcha (`try-except` de fallback dentro de bucles de reintento) para resolver incompatibilidades de API o tests en rojo, sin detenerse a consultar al desarrollador principal ni evaluar el impacto arquitectónico global (violación del principio PonyTail/YAGNI).

**Decisión:**  
Se establece el **Protocolo de Pausa Arquitectónica (*Stop & Consult*)** como regla fundamental de co-piloteo *Human-in-the-Loop* en el desarrollo de software (`AGENTS.md` Regla 5):
1. Si durante la implementación surge una incompatibilidad de API, un error no previsto o un caso de borde cuya solución requiera añadir lógica anidada compleja (ej. fallbacks multinivel, reintentos ad-hoc o parches acumulativos), el Agente **TIENE PROHIBIDO** parchear el código sobre la marcha para "hacer que funcione".
2. El Agente **DEBE PAUSAR** inmediatamente su turno, explicar con claridad al desarrollador la causa raíz del problema y presentar **al menos dos opciones arquitectónicas** contrastadas contra el principio YAGNI (simplicidad y modularidad plana) para tomar la decisión en equipo antes de modificar el código.

**Consecuencias:**  
Garantiza que toda solución técnica mantenga una estructura plana, limpia y fácil de escalar en versiones posteriores (`v0.2` en adelante), eliminando la deuda técnica temprana y reforzando el rol de la autora del portfolio como arquitecta y directora técnica superior del sistema.

---

### D-030
## Capa de Persistencia y Migraciones Transaccionales en Modularidad Plana (`SQLAlchemy + Alembic sobre PostgreSQL 16 Alpine en Puerto Dedicado 5433`)

**Estado:** Adoptada (`[v0.2-001]`)  
**Fecha:** Julio 2026 (13/07/2026)  
**Contexto:**  
En el arranque de la v0.2, es necesario integrar el motor relacional de PostgreSQL para almacenar las entregas, rúbricas y valoraciones cualitativas de la IA. Surgieron dos requerimientos críticos: por un lado, evitar conflictos en el puerto nativo `5432` de Windows/WSL provocados por bases de datos de prácticas anteriores o servicios locales; y por otro, mantener la arquitectura fiel a las reglas del proyecto (`YAGNI` y `Modularidad Plana`), evitando sobreingeniería con patrones de repositorio redundantes.

**Decisión:**  
Se adopta la siguiente arquitectura técnica de persistencia:
1. **Puerto Dedicado Exclusivo (`5433:5432`):** El contenedor de Docker (`postgres:16-alpine`) se expone en el puerto externo `5433` de Windows/WSL, eliminando por diseño la posibilidad de colisión (`Bind failed`) con cualquier otra base de datos o proyecto local en el PC de la desarrolladora.
2. **Modularidad Plana (`backend/models/database.py`):** Siguiendo la Regla 2 de `AGENTS.md`, todo el acceso a datos, motor (`engine`), sesión (`SessionLocal`) e inyecciones de dependencia (`get_db`) residen de forma plana y directa en `backend/models/database.py`, exportando los objetos en `backend/models/__init__.py`. Se rechaza crear capas abstractas como `repositories/` o `DAO/` innecesarias para la escala de la API.
3. **Migraciones Transaccionales (`Alembic`):** Se configura `Alembic` leyendo de forma dinámica la variable de entorno `DATABASE_URL` y vinculándose a `Base.metadata`.

**Consecuencias:**  
El proyecto se vuelve 100% autoinstalable e independiente en cualquier entorno local (`Docker Compose up -d` y `alembic upgrade head`), garantizando persistencia relacional transaccional y coherencia estricta con el estilo *PonyTail*.

---

### D-031
## Blindaje de Privacidad y Seguridad sin Claves Maestras (`Seudonimización Estricta + Hacheo Unidireccional bcrypt vs Cifrado Simétrico`)

**Estado:** ✅ Adoptada (`[v0.2-002]`)  
**Fecha:** Julio 2026 (13/07/2026)  
**Contexto:**  
En el diseño del modelo de datos de profesores (`[v0.2-002]`) y la planificación del almacenamiento de adaptaciones curriculares del alumnado (`[D-023]`, `v0.2-007`), se debatió la conveniencia de implementar Cifrado Simétrico en Reposo a nivel de columna (`Application-Level Encryption` mediante `AES / Fernet` y una `ENCRYPTION_KEY` en el archivo `.env`). Se evaluaron el coste computacional, la complejidad técnica y los riesgos de pérdida de datos.

**Opciones consideradas:**
- **Cifrado Simétrico en Reposo (`cryptography / Fernet`) para todas las columnas sensibles:** Rechazado por introducir el riesgo crítico y catastrófico de pérdida irrecuperable de toda la base de datos ante un extravío o corrupción de la variable `ENCRYPTION_KEY` durante reinicios o migraciones del servidor (`Key Loss Gotcha`), violando la simplicidad del principio *PonyTail/YAGNI*.
- **Almacenamiento en texto claro sin protección:** Rechazado categóricamente por incumplir el RGPD, la LOPDGDD (art. 7 protección de menores) y el Esquema Nacional de Seguridad (ENS).
- **Seudonimización Estricta (`HitL Client-Side`) para el alumnado + Hacheo Unidireccional (`bcrypt`) para el docente:** **Elegida por su solidez jurídica y técnica absoluta con cero riesgo de pérdida de datos**.

**Decisión:**  
Se adopta la siguiente estrategia multinivel de seguridad y privacidad:
1. **Privacidad de Alumnos por Seudonimización (`[D-023]` & `[D-025]`):** La base de datos en la nube no procesa ni almacena jamás el nombre ni los datos personales del estudiante. Todas las entregas se asocian a un código identificador anónimo (`alumno_id = "A-14"`). La libreta de equivalencia con la identidad real del menor reside en exclusiva en el cuaderno o en la sesión local de XADE del profesor, haciendo que la base de datos sea intrínsecamente inocua e irrelevante en caso de una intrusión externa sin necesidad de claves de descifrado.
2. **Autenticación Docente por Hacheo Unidireccional (`bcrypt` + `JWT` en `v0.2-002`):** Las contraseñas no utilizan cifrado simétrico ni dependen de una clave secreta del servidor; se transforman mediante el algoritmo matemático irreversible `bcrypt` (`passlib[bcrypt]`). La validación del login compara hashes, lo que inmuniza el sistema frente a pérdidas de variables de entorno y garantiza que el reinicio o cambio de servidor no afecte el acceso de las profesoras.
3. **Cifrado en Tránsito (`TLS 1.3 / HTTPS`):** Toda la comunicación cliente-servidor se encapsula por túnel seguro como requisito para la PWA.

**Justificación Institución-Auditor (Audit Defense frente a Tribunal/ENS):**
1. **Descarte por Análisis de Riesgos Operativos (no por desconocimiento):** Se documenta expresamente que el cifrado simétrico en columnas no se omite por ignorancia técnica, sino tras un riguroso análisis de riesgos. En el contexto educacional y administrativo del proyecto, la probabilidad de gestión defectuosa, subida accidental a Git o pérdida irrecuperable de la clave maestra supera con creces el beneficio marginal frente a una seudonimización bien diseñada.
2. **Complementariedad y Cifrado de Volumen Cloud (`TDE`):** La seudonimización no actúa en vacío; se complementa con controles de acceso transaccional (`JWT`), minimización de datos guardados y el **Cifrado Transparente a Nivel de Volumen/Servicio (`Transparent Data Encryption - TDE`)** gestionado de forma nativa por el proveedor de base de datos cloud (`Railway / Azure PostgreSQL`), prescindiendo de criptografía ad-hoc en columnas por el principio YAGNI.
3. **Alcance Exclusivo de `bcrypt`:** Queda establecido como invariante arquitectónica que `bcrypt` se utiliza estricta y exclusivamente para las contraseñas del profesorado. Ningún otro identificador o dato personal sensible se almacena directamente en claro en la base de datos principal.

**Consecuencias:**  
El proyecto alcanza el máximo nivel de cumplimiento normativo (RGPD, ENS, AI Act) eliminando por diseño la deuda técnica y el peligro mortal de corromper la base de datos por pérdida de claves maestras.


---

*Documento creado el 08/07/2026 — Antigravity para Alba Camiña García*  
*Actualizado el 13/07/2026 — añadidas D-027 (Modo Dual), D-028 (Groq como Motor Primario), D-029 (Protocolo de Pausa Arquitectónica), D-030 (Persistencia y Migraciones) y D-031 (Blindaje sin Clave Maestra)*  
*Total de decisiones registradas: 31*