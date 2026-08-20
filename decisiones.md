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
| [D-030](#d-030) | Capa de Persistencia y Migraciones Transaccionales en Modularidad Plana (`SQLAlchemy + Alembic`) | Jul 2026 | ✅ Adoptada |
| [D-031](#d-031) | Blindaje de Privacidad y Seguridad sin Claves Maestras (`Seudonimización Estricta + bcrypt`) | Jul 2026 | ✅ Adoptada |
| [D-032](#d-032) | Trazabilidad Bidireccional Git-Web (`Bidirectional Traceability`) y Gobernanza de Milestones | Jul 2026 | ✅ Adoptada |
| [D-033](#d-033) | Gestión de Vigencia Legislativa Curricular en el Modelo de Datos (`Metadatos Estáticos de Validación YAGNI`) | Jul 2026 | ✅ Adoptada |
| [D-034](#d-034) | Segunda Capa de Comprobación y Redacción PII ante Casos de Borde Fotográficos (`Client-Side Blackout Tool` + Freno Pre-Nube) | Jul 2026 | ✅ Adoptada |
| [D-035](#d-035) | Gobernanza de cambios sensibles y criterio de cierre de auditoría técnica (`AGENTS.md Regla 6`) | Jul 2026 | ✅ Adoptada |
| [D-036](#d-036) | Simetría Lingüística en Entornos Co-oficiales (`Espejo Lingüístico Bilingüe`) | Jul 2026 | ✅ Adoptada |
| [D-037](#d-037) | Estandarización del Historial Git (`Conventional Commits` y Trazabilidad ADR) | Jul 2026 | ✅ Adoptada |
| [D-038](#d-038) | Mitigación de Pérdida de Contexto en Prompts Densos (`Prompt Anchoring` & `XML Tags`) | Jul 2026 | ✅ Adoptada |
| [D-039](#d-039) | Desacoplamiento de Calificación Numérica y Cualitativa en Pruebas Evaluables | Jul 2026 | ✅ Adoptada |
| [D-040](#d-040) | Distinción normativa LEY vs. CONFIGURACIÓN DE CENTRO como principio rector de calificación | Jul 2026 | ✅ Adoptada |
| [D-041](#d-041) | Soporte multi-etapa: campo `etapa` (ESO/BACH) en `marcos_evaluacion` | Jul 2026 | ✅ Adoptada |
| [D-042](#d-042) | Corrección de abreviatura cualitativa oficial: "BE" (Bien), nunca "BI" — corrige D-039 | Jul 2026 | ✅ Adoptada |
| [D-043](#d-043) | Nota de prueba por media ponderada; la IA no suma, el backend recalcula — corrige D-039 | Jul 2026 | ✅ Adoptada |
| [D-044](#d-044) | Trazabilidad obligatoria criterio de evaluación → competencia clave | Jul 2026 | ✅ Adoptada |
| [D-045](#d-045) | Semántica HitL de la nota: `calificacion_numerica` es orientativa con decimales; el redondeo a entero de boletín lo hace el docente | Jul 2026 | ✅ Adoptada |
| [D-046](#d-046) | Etapa como `str` Enum de Python en lugar de tabla catálogo en BD | Jul 2026 | ✅ Adoptada |
| [D-051](#d-051) | Adopción de OpenAI (`gpt-4o-mini`) para Visión y retención de Groq para Texto (Workload Routing) | Ago 2026 | ✅ Adoptada |
| [D-052](#d-052) | Asignación determinista de la cualitativa ESO en el backend (umbral de suelo); la regla de redondeo al entero de boletín es configuración de centro | Ago 2026 | ✅ Adoptada |
| [D-053](#d-053) | Unificación del motor LLM en OpenAI (`gpt-4o-mini`) para texto e imagen tras deprecación de `llama-3.3-70b-versatile` en Groq y fallo de Qwen con JSON complejo | Ago 2026 | ✅ Adoptada |
| [D-054](#d-054) | Limitación conocida del RAG Determinista v1: ausencia de materiales didácticos del docente como contexto evaluativo | Ago 2026 | ✅ Adoptada |

---

## Decisiones de Producto y Negocio

### D-001
## Comunidad autónoma objetivo: Galicia (`seed` curricular principal)

**Fecha:** Julio 2026 (Actualizada el 09/07/2026)  
**Estado:** ✅ Adoptada

**Contexto:**  
El sistema de evaluación educativa en España varía por comunidad autónoma. Adaptarlo a todas desde el principio haría el MVP inviable. La autora reside y está empadronada en **A Coruña (Galicia)**, hogar de la sede nacional de la **Auditoría (Agencia Española de Supervisión de la IA)** y del clúster *Ciudad de las TIC*.

**Opciones consideradas:**
- **Galicia** — coherencia total entre sede técnica (A Coruña), normativa (Decreto autonómico de la Xunta / LOMLOE Galicia), facilidad de testeo con profesoras locales, potencial diferencial bilingüe (castellano/gallego) y alineación con las ayudas/aceleradoras locales (IGAPE, Polo de Emprendemento de A Coruña, Explorer UDC, Activa Startups Galicia).
- **Andalucía** — mayor volumen demográfico en España, contemplado inicialmente, pero sin conexión física con el ecosistema en el que se mueve y desarrollará el proyecto.
- **Nacional genérico** — inviable como MVP, demasiado amplio.

**Decisión:** **Galicia** como comunidad autónoma objetivo principal y primer marco curricular precargado (`seed`). Logra la máxima cohesión entre la prueba de concepto, las validaciones con docentes de la zona y la presentación institucional ante la **Auditoría en la Ciudad de las TIC**.

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

**Decisión:** Human-in-the-Loop. La IA actúa exclusivamente como copiloto: propone un borrador de corrección o sugerencias de verificación formativa. El profesor tiene siempre la última palabra para aprobar, ajustar o rechazar.

**Consecuencias:** 
1. El estado general de `Submission` incluye el paso `REVIEW` antes de `GRADED`.
2. La tabla de auditoría inmutable `ChangeLog` separa estrictamente dos planos para el cumplimiento probatorio:
   - **Diff de Negocio (`datos_anteriores` / `datos_nuevos`):** Contiene exclusivamente los estados reales antes y después de la acción (ej. transiciones de `estado` o `estado_feed_forward`).
   - **Contexto de Auditoría (`audit_metadata`):** JSON que captura información auxiliar de trazabilidad (`ia_propuso_verificacion`, `evaluation_id`, versión del prompt, etc.).
3. **Invariante legal de autoría:** El `actor` persistido en `ChangeLog` en transiciones críticas o de firma es **siempre un humano** (`PROFESOR_ID_X`). La IA no actúa nunca como actora ejecutora en transiciones formativas firmadas; su participación queda registrada únicamente en `audit_metadata` como señal de influencia o sugerencia. Esta decisión es el escudo legal central del producto bajo el AI Act y RGPD.

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

**Consecuencias:** El seed de la BBDD en v0.2 incluirá un marco de evaluación real de **Filosofía de Bachillerato gallego** (Decreto 157/2022, Xunta de Galicia) como primer registro. Coherente con D-001 (sede en A Coruña, Auditoría, Decretos 156/157/2022).

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

**Decisión:** La tabla `submissions` incorpora el campo `adaptaciones_alumno` (JSONB) configurable por la profesora. El sistema clasifica las adaptaciones en 4 niveles (DEA/ACNS/ACS/ACIS) según el Decreto 229/2011 de Galicia. El LLM **siempre detecta y reporta** todos los errores específicos, pero el campo `errores_excluidos_por_adaptacion` los separa de los penalizables. Tras una pausa arquitectónica (*Stop & Consult*), se unifican las exclusiones visuales bajo un único tipo de marcador genérico (`type: "error_excluido"` en lugar de tipos específicos como `ortografia_excluida` o `calculo_excluido`) para simplificar el prompt del LLM y optimizar su consumo de tokens, permitiendo que la PWA muestre de forma homogénea en gris/neutro cualquier adaptación aplicada (dislexia/DEA, discalculia, inteligencia límite/NEE o trastornos psiquiátricos graves/CPHE). La IA **nunca diagnostica** NEAE; solo aplica instrucciones recibidas. Toda configuración queda en el `changelog` con timestamp (trazabilidad AI Act). El detalle exhaustivo de la jerarquía normativa en 4 capas y el marco autonómico general/NEAE se encuentra documentado en `marco_normativo_y_adaptaciones.md`.

**Consecuencias:** Nueva clave `adaptaciones_alumno` (JSONB nullable) en `submissions`. Nuevo bloque en el contrato JSON del LLM: `ortografia_detectada`, `errores_excluidos_por_adaptacion` y marcadores de tipo `error_excluido`. Los datos de adaptaciones son datos de salud de menores → acceso restringido al `profesor_id` propietario. Implementación en `v0.2-007`. Casos de ACS grave (discapacidad intelectual) quedan fuera del MVP actual y se marcan con aviso `adaptacion_significativa: true`.

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
   * *Señal auxiliar de verificación (`feed_forward_verification_suggestion`):* En evaluaciones posteriores del mismo alumno, el contrato Pydantic puede emitir un booleano (`True/False`) recomendando al docente si el alumno ha incorporado con éxito el paso accionable anterior. Esta señal es únicamente informativa para el panel PWA y **no altera ningún estado en BBDD automáticamente**.
3. **Índice de Confianza IA (`confidence_score`):** Un valor float entre `0.0` y `1.0` que indica la certeza técnica de la lectura OCR o interpretación del modelo. Si es `< 0.75`, el panel de la profesora muestra una alerta preventiva ("Caligrafía confusa o respuesta ambigua — requiere revisión manual prioritaria"), reforzando el *Human-in-the-Loop* bajo la AI Act.

**Consecuencias:** El esquema JSON del smoke test (`smoke_test_llm.py` en `v0.1-000`) y de Pydantic en FastAPI incluirá estos tres campos. La PWA mostrará el *confidence score* en el panel dual de corrección y destacará el "Siguiente Paso Accionable" como tarjeta prioritaria para el docente y el alumno.

> [!IMPORTANT]
> **La combinación es imbatible:** usamos la legalidad y los criterios competenciales cualitativos de Galicia como cimiento (`marcos_evaluacion` en `JSONB`), e inyectamos las técnicas pedagógicas más avanzadas de Reino Unido y USA (*Next Steps* y *Confidence Score*) como superpoder del motor de IA. Es un producto redondísimo para presentar tanto en la Auditoría como en cualquier instituto o entrevista de ingeniería EdTech.

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
**Estado:** ✅ Adoptada (`[v0.2-005]` / `feature/feed-forward-state-transitions`)

**Contexto:**  
En el modelo de corrección de api-correccion-formativa-ia-galicia (`[D-024]`), el motor LLM devuelve un "Siguiente Paso Accionable" (*Feed Forward*) con una directriz clara y concreta para que el estudiante la ejecute de inmediato (*"Reescribe el párrafo 3 incorporando dos conectores temporales"*). Surge el dilema sobre si el sistema y el docente deben evaluar o calificar numéricamente la entrega o devolución de dicho paso.

**Opciones consideradas:**
- **Calificar numéricamente cada devolución de Feed Forward:** Rechazado categóricamente por generar una duplicación masiva de la carga burocrática del profesor (convertir cada corrección en una nueva mini-tarea evaluable que revisar al día siguiente), destruyendo la promesa de alivio docente del producto.
- **Dejar el Feed Forward como recomendación informal sin registro:** Rechazado por generar falta de rendición de cuentas (*accountability*) en el alumno, convirtiendo el feedback en texto inerte.
- **Registro de Checklist Formativo de Autoevaluación y Verificación Docente en Base de Datos (`estado_feed_forward` — *Sin Carga Sumativa*):** **Elegida por coherencia pedagógica, UX docente y blindaje HitL**.

**Decisión:**  
El cumplimiento del Siguiente Paso Accionable se modela como una columna propia (`estado_feed_forward`) en la tabla `submissions`, independiente del ciclo de vida sumativo (`estado`), desglosada en tres valores exactos:
1. `PENDIENTE`: Asignado por defecto por el sistema al inicializar o corregir la entrega.
2. `REALIZADO_ALUMNO`: El estudiante (o el profesor como proxy en el aula) indica que ha completado la acción de mejora en su estudio personal o cuaderno.
3. `VERIFICADO_EN_PRUEBA_SIGUIENTE`: En la evaluación del siguiente instrumento dentro de la misma Situación de Aprendizaje (`SdA`), se constata e interioriza que la mejora previa fue aplicada con éxito.

**Invariante Arquitectónica y Reglas de Transición:**
> [!IMPORTANT]
> **El LLM no persiste nunca `estado_feed_forward`; solo propone, el profesor confirma.** Aunque la IA emita la señal `feed_forward_verification_suggestion=True`, la actualización real en BBDD requiere una acción humana explícita mediante los endpoints transicionales.

El backend prohíbe saltos no permitidos o reejecuciones, rechazando con HTTP `409 Conflict` cualquier transición fuera de este flujo estrictamente unidireccional:
`PENDIENTE` ──(PATCH /realizado)──> `REALIZADO_ALUMNO` ──(PATCH /verificado)──> `VERIFICADO_EN_PRUEBA_SIGUIENTE`

**Endpoints dedicados:**
- `PATCH /api/v1/submissions/{id}/feed-forward/realizado`: Requiere autenticación docente (proxy del alumno). Cambia `PENDIENTE → REALIZADO_ALUMNO`.
- `PATCH /api/v1/submissions/{id}/feed-forward/verificado`: Requiere autenticación docente. Cambia `REALIZADO_ALUMNO → VERIFICADO_EN_PRUEBA_SIGUIENTE`. Acepta un body opcional (`FeedForwardVerificadoRequest`) para inyectar en el log si la IA recomendó la verificación.

**Consecuencias:**  
Todas las transiciones quedan registradas de forma atómica en `ChangeLog` asociando al docente como `actor` y aislando la influencia del LLM (`ia_propuso_verificacion`, `evaluation_id`) dentro del campo `audit_metadata` (`[D-002]`).

---

### D-027
## Modo dual de interacción rúbrica-normativa seleccionable en PWA (`COMBINADO` vs `AUDITORIA_CURRICULAR`)

**Estado:** Adoptada (`[v0.2-004]`)  
**Fecha:** Julio 2026  
**Contexto:**  
En el diseño del hito `[v0.2-004]`, surgió el debate técnico sobre cómo deben interactuar los criterios del marco normativo autonómico (Decreto 157/2022 de la Xunta de Galicia) y la rúbrica personalizada creada por la profesora. Se plantearon inicialmente dos opciones mutuamente excluyentes: combinación simple o auditoría pedagógica de coherencia.

**Decisión:**  
En lugar de forzar una única estrategia fija en el backend, se implementa un **Modo Flexible y Multicriterio de Evaluación** configurable por la profesora directamente desde la interfaz PWA y transmitido en cada petición de corrección (`modo_evaluacion` en el JSON / columna en `submissions`):
1. **Modo Rúbrica Pura (Evaluación General):** Se activa de forma natural si la petición **no especifica un `marco_id`** (`marco_id = None/null`). El motor LLM evalúa y corrige la entrega utilizando en exclusiva los criterios de la rúbrica personalizada de la profesora, ignorando cualquier currículo oficial. Esto permite agilidad en tareas rápidas diarias y el uso de la app fuera de la región o del marco español.
2. `COMBINADO` (Evaluación Rápida Cotidiana): Requiere `marco_id`. El motor LLM fusiona de forma aditiva los saberes básicos oficiales y los criterios específicos de la rúbrica del docente para calificar con agilidad tareas del día a día, controles cortos o exposiciones bajo la LOMLOE.
3. `AUDITORIA_CURRICULAR` (Coherencia e Inspección Pedagógica): Requiere `marco_id`. Diseñado para evaluaciones formales de fin de trimestre. El motor corrige la entrega pero además actúa como orientador pedagógico para el docente, contrastando la rúbrica de aula contra el Decreto de la Xunta de Galicia e informando confidencialmente en `teacherSummary` si la rúbrica omite competencias básicas obligatorias.

**Consecuencias:**  
Otorga una flexibilidad total al docente (permitiendo evaluar de forma informal con rúbricas propias rápidas) y aporta un valor diferencial extraordinario ante inspección educativa en las evaluaciones formales, posicionando al sistema como un copiloto adaptable y robusto.

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

### D-032
## Trazabilidad Bidireccional Git-Web (`Bidirectional Traceability`) y Gobernanza de Milestones

**Estado:** ✅ Adoptada (`[v0.2]`)  
**Fecha:** Julio 2026 (13/07/2026)  
**Contexto:**  
En proyectos individuales o de desarrollo por parejas (`Phase Ninja`), la gestión de tareas puede bifurcarse entre archivos de texto locales dentro del repositorio (`backlog.md`) y herramientas de gestión de producto en la nube (tableros de GitHub Issues y Milestones). Se evaluó cómo evitar la burocracia pesada de abrir decenas de micro-issues en la web manteniendo, al mismo tiempo, una presentación directiva corporativa e impecable ante tribunales o reclutadores.

**Opciones consideradas:**
- **Exclusivamente gestión web en GitHub Issues:** Rechazada por introducir latencia en el flujo de pair programming y crear dependencia externa si se inspecciona el código local offline.
- **Exclusivamente archivo local `backlog.md` sin rastro en la web:** Rechazada por desaprovechar la potencia visual de GitHub Projects/Releases ante evaluadores o inversores.
- **Trazabilidad Bidireccional (`Local <-> Web`) con Épicas por Versión:** **Elegida por su equilibrio perfecto entre agilidad PonyTail/YAGNI y excelencia de escaparate corporativo**.

**Decisión:**  
Se establece como invariante de gobernanza del proyecto la **Trazabilidad Bidireccional de Milestones**:
1. **En GitHub Web:** Se abre una **única Issue Épica por Versión/Milestone** (`Issue #1 v0.1`, `Issue #2 v0.2`, `Issue #3 v0.3`), agrupando en su cuerpo el listado de historias de usuario y ADRs. Si durante el desarrollo surge un pivote arquitectónico, la Issue se edita o se cierra formalmente con el motivo nativo **`Close as not planned`** argumentando el ADR de respaldo.
2. **En el Repositorio Local (`backlog.md`):** Se enlaza explícitamente cada cabecera de versión con su número de Issue web correspondiente (`[GitHub Issue #X]`), permitiendo una trazabilidad instantánea bidireccional desde cualquier entorno.

**Consecuencias:**  
El proyecto mantiene velocidad máxima en el desarrollo en terminal, a la vez que proyecta una madurez de gestión de producto y control de cambios al nivel de los estándares internacionales más exigentes.

---

---

### D-033
## Gestión de Vigencia Legislativa Curricular en el Modelo de Datos (`Metadatos Estáticos de Validación YAGNI vs Crawler Automático de Boletines`)

**Estado:** ✅ Adoptada (`[v0.2-003]`)  
**Fecha:** Julio 2026 (14/07/2026)  
**Contexto:**  
Las leyes educativas autonómicas y estatales (decretos de la Xunta de Galicia / LOMLOE) son susceptibles de cambios, enmiendas y derogaciones parciales a lo largo del tiempo. Evaluar a estudiantes bajo un marco legal obsoleto viola el principio de equidad y podría comprometer el cumplimiento de la EU AI Act en materia de precisión y gobernanza de sistemas de alto riesgo. Se evaluó la conveniencia de implementar un sistema dinámico y automatizado de sincronización web (BOE/DOG Tracker).

**Opciones consideradas:**
- **Sistema Automatizado de Scraping y Parseo Curricular (BOE/DOG Tracker):** Rechazado por introducir una altísima complejidad técnica, dependencias de bibliotecas externas de parseo web y gran fragilidad ante cambios estructurales en los portales gubernamentales. Esto violaría flagrantemente el principio YAGNI para una base de datos que se modifica de forma muy infrecuente (frecuencia anual o plurianual).
- **Esquema de Metadatos de Verificación Manual (Enfoque YAGNI-friendly):** **Elegido por su simplicidad y efectividad**. Se añaden al modelo del marco de evaluación campos estáticos que indican la fecha de la última validación humana del decreto y la URL de la fuente legislativa oficial. Permite proyectar total transparencia jurídica al docente y a la inspección sin añadir código complejo o inestable.

**Decisión:**  
Se adopta el esquema de metadatos estáticos en el modelo de datos `MarcoEvaluacion`:
1. **Campos en Base de Datos:** Se incorporan las columnas `ultima_verificacion_manual` (DATE, nullable) y `fuente_legislativa_url` (VARCHAR, nullable) a la tabla `marcos_evaluacion`.
2. **Visualización Docente:** La interfaz de usuario expondrá estos metadatos para que el docente tenga la certeza jurídica de la ley aplicada y su fecha de última validación.
3. **Roadmap de Automatización:** Se relega el rastreo automático a un ítem a futuro del Roadmap (`[Roadmap-001]`), justificando que la versión actual se mantiene manual por criterios de agilidad, estabilidad y minimización de deuda técnica.

**Consecuencias:**  
El sistema cumple de manera transparente con las obligaciones de gobernanza de datos y trazabilidad de la EU AI Act de forma inmediata, manteniendo la base de código libre de integraciones inestables y scrapers redundantes.

---

### D-034
## Segunda Capa de Comprobación y Redacción PII ante Casos de Borde Fotográficos (`Client-Side Blackout Tool en PWA + Freno Offline Pre-Nube`)

**Estado:** ✅ Adoptada (`[v0.3-005]` / `Roadmap v0.8`)  
**Fecha:** Julio 2026 (15/07/2026)  
**Contexto:**  
Aunque el patrón de **Cámara de Exclusión Pre-Nube (`[D-022]`)** recorta automáticamente el margen superior del examen mediante `Pillow`, en la práctica real del aula de secundaria se producen **casos de borde fotográficos (`Edge Cases`)**: alumnos que escriben su nombre y apellidos en el centro del folio debajo de un dibujo, en el margen lateral derecho o como firma al final de la última respuesta. Si el recorte mecánico superior actúa en solitario, el nombre del estudiante superviviente viajaría intacto a los servidores de la nube (`Cloudinary / Groq`), cometiendo una cesión internacional ilegal de datos de menores identificables bajo el RGPD y la LOPDGDD.

**Opciones consideradas:**
- **Subida a ciegas confiando exclusivamente en el recorte superior:** Rechazado categóricamente por dejar expuesto al centro educativo a multas por fugas de PII (*Personally Identifiable Information*) cuando el alumno no escribe en el encabezado.
- **Segunda Capa de Verificación Visual y Redacción en PWA (`HitL Client-Side Blackout Box`):** La PWA de la profesora (`React / Canvas`) muestra una vista previa pre-subida con la franja superior negra por defecto y permite al docente arrastrar recuadros negros adicionales sobre cualquier nombre descolocado o firma lateral antes de confirmar la subida. Los píxeles del nombre se funden y eliminan en el propio navegador del cliente (*Zero Data Retention* absoluto). — **Elegido como estándar innegociable para la PWA desde `v0.5-002` / `v0.3-005`**.
- **Escáner Local Offline de PII en Servidor (`Automated Offline PII Shield` con `Microsoft Presidio / Tesseract`):** Como capa secundaria automática en servidor local pre-nube (`v0.8+`), antes de salir hacia la nube exterior el archivo es escaneado offline en RAM. Si detecta texto compatible con nombres propios o coincidentes con el listado oficial del curso (`PII Confidence > 0.8`), bloquea el envío y arroja un error 422 alertando al docente para su revisión visual en pantalla.

**Decisión:**  
Se adopta una defensa multinivel pre-nube para casos de borde de PII:
1. **Inspección Visual y Tampón en Navegador (`Client-Side HitL Blackout Box` en `v0.5-002`):** El docente es el soberano legal de la purga. Si advierte que el alumno escribió fuera del margen superior, difumina/recorta la zona infractora con el dedo o ratón directamente sobre el Canvas de la PWA antes de autorizar el `fetch` a la nube.
2. **Evolución Offline en Backend (`Roadmap v0.8`):** Se planifica la integración de una comprobación automática offline en memoria como salvaguarda secundaria en el servidor antes de conectar con APIs externas de IA.

**Consecuencias:**  
Se elimina al 100% el riesgo de fuga de datos en folios atípicos, demostrando ante agencias de supervisión (*Auditoría / AEPD*) una cultura de ingeniería de ciberseguridad *Privacy by Design / Privacy by Default* superior al estándar del sector.

---

### D-035
## Gobernanza de cambios sensibles y criterio de cierre de auditoría técnica

**Estado:** ✅ Adoptada (`[v0.2-008]` / `AGENTS.md Regla 6`)  
**Fecha:** Julio 2026 (16/07/2026)

**Contexto:**  
En un sistema de evaluación formativa asistido por IA, los cambios que afectan a estados de negocio, permisos, trazabilidad o al contrato HitL del modelo tienen impacto directo en cumplimiento y responsabilidad. Históricamente, es fácil que el código avance más rápido que los tests o la documentación, generando zonas de sombra: funcionalidades que “funcionan” pero no están trazadas ni defendibles en una revisión técnica.

**Decisión:**  
Se establece una política de gobernanza para **cambios sensibles**, definida como cualquier modificación sobre:

1. Estados del ciclo de vida de negocio o del alumno (`Submissions.estado`, `estado_feed_forward`).
2. Trazabilidad probatoria y registros inmutables (`ChangeLog`, `audit_metadata`).
3. Autenticación, permisos de propiedad o roles (`auth`, respuestas `403 Forbidden`).
4. Contratos estructurados de salida del LLM (`EvaluacionIA`) y su frontera con la firma humana (`HitL`).

Un cambio de este tipo solo se considera **auditado y cerrado** cuando cumple, de forma simultánea, los siguientes cuatro pilares:

1. **Diseño y gobernanza:** Existe una decisión arquitectónica justificada y registrada en `decisiones.md` (ADR) que describe contexto, opciones y consecuencias.
2. **Implementación:** El código productivo refleja esa decisión de forma coherente, siguiendo los principios de modularidad plana y modelos tipados (`Pydantic` / `SQLAlchemy`).
3. **Evidencia:** La suite de pruebas relevante (`pytest`) se ejecuta en verde en entorno limpio (`WSL`, contenedor Docker), demostrando el comportamiento esperado.
4. **Sincronización documental:** `README.md` proporciona visibilidad técnica actualizada, `backlog.md` registra historias completadas y cualquier deuda técnica restante, y los cambios de ambos quedan vinculados al mismo Pull Request o sesión de trabajo.

**Consecuencias:**  

- Cualquier módulo que no cumpla los cuatro pilares se clasifica explícitamente como **“Estado: Parcial / Pendiente de auditoría”** y no se considera listo para revisión externa o defensa de portfolio.
- Esta política se incorpora al comportamiento del asistente (`AGENTS.md`, Regla 6), de modo que tanto humanos como IA deben verificar el impacto multinivel antes de dar por finalizada una tarea sensible.
- La trazabilidad entre decisiones (`decisiones.md`), implementación, pruebas y documentación se convierte en condición de salida estándar para cambios con impacto en estados, permisos, trazabilidad o HitL.

---

### [D-036] Simetría Lingüística en Entornos Co-oficiales (`Espejo Lingüístico Bilingüe`)

**Estado:** ✅ Adoptada (`[v0.2]` / `prompt_builder.py Regla 7`)  
**Fecha:** Julio 2026 (17/07/2026)

**Contexto:**  
Galicia opera bajo un sistema de co-oficialidad lingüística (gallego/castellano) en el que el alumnado tiene el derecho y la libertad de realizar sus pruebas evaluables en cualquiera de los dos idiomas o según la vehicularidad fijada por el proyecto lingüístico del centro. Dado que el `SYSTEM_PROMPT` base del motor LLM se redacta en castellano, existe el riesgo del comportamiento por defecto de la IA de responder en castellano (`reasoning`, `teacherSummary`, `siguiente_paso_accionable`) ante una entrega o rúbrica redactada en gallego, rompiendo la coherencia pedagógica y la inmersión normativa de la materia.

**Decisión:**  
Se adopta la **Regla de Simetría Lingüística (*Espejo Lingüístico*)** inyectada de forma imperativa en el `SYSTEM_PROMPT` (Directriz 7): el motor LLM tiene orden estricta de detectar el idioma vehicular de la respuesta del estudiante y de la rúbrica, y de formular el 100% del feedback cualitativo y accionable en ese mismo idioma (gallego normativo o castellano), sin mezclar lenguas ni requerir traducción o configuración manual adicional en cada corrección.

**Consecuencias:**  
1. **Inclusión lingüística nativa:** El alumno que responde en gallego recibe su `Siguiente Paso Accionable` y razonamiento en gallego normativo impecable, respetando el Decreto 157/2022 de la Xunta de Galicia.
2. **Cero fricción docente:** La profesora no necesita seleccionar un toggle de "Idioma: Gallego" o "Idioma: Castellano" en la PWA; el motor actúa como espejo dinámico automático en cada llamada.

---

### [D-037] Estandarización del Historial Git (`Conventional Commits` y Trazabilidad ADR)

**Estado:** ✅ Adoptada (`[v0.2]` / `AGENTS.md Regla 7`)  
**Fecha:** Julio 2026 (18/07/2026)

**Contexto:**  
En un proyecto orientado a construir un portfolio de ingeniería de alto nivel y preparatorio para reuniones técnicas y auditorías de código, el historial de commits es tan importante como el código en sí. Un historial desordenado o mensajes opacos restan credibilidad a la arquitectura diseñada. Existe el riesgo de que al evolucionar rápidamente, los mensajes de commit pierdan su conexión con las tareas del backlog y las decisiones de arquitectura (ADRs), rompiendo la trazabilidad probatoria del proyecto.

**Decisión:**  
Se adopta el uso riguroso y obligatorio del estándar **Conventional Commits** (`feat:`, `fix:`, `docs:`, `test:`, `style:`) acompañado siempre de un **scope** descriptivo entre paréntesis (ej. `feat(submissions):`). Adicionalmente, se decreta que todo mensaje de commit (o PR) **debe incluir la referencia cruzada** al ID de la tarea del backlog (ej. `[v0.2-009]`) o al registro arquitectónico que lo motiva (ej. `[D-035]`).

**Consecuencias:**  
1. **Portfolio auto-explicativo:** El repositorio de GitHub se convierte en un artefacto que demuestra madurez en ingeniería de software (*Governance*), facilitando su lectura por parte de empresas tecnológicas, consultoras o mentores (Auditoría).
2. **Trazabilidad bidireccional real:** Cualquier evaluador técnico puede navegar desde una línea de código específica, ver el commit que la introdujo, leer el mensaje y saltar directamente al documento `decisiones.md` para entender el razonamiento de negocio que justificó ese cambio.

---

### [D-038] Mitigación de Pérdida de Contexto en Prompts Densos (`Prompt Anchoring` & `XML Tags`)

**Estado:** ✅ Adoptada (`[v0.2]` / `AGENTS.md Regla 8`)  
**Fecha:** Julio 2026 (18/07/2026)

**Contexto:**  
Al procesar rúbricas extensas, normativas largas (`marcos_evaluacion`) y folios transcritos masivos, la IA corre el riesgo de sufrir *Lost in the Middle* o *Context Overflow*, olvidando las reglas pedagógicas iniciales inyectadas en nuestro `SYSTEM_PROMPT` (como la Regla de simetría lingüística o la obligación de estructurar el JSON).

**Decisión:**  
Se adopta como arquitectura defensiva el uso estructurado de delimitadores semánticos (XML Tags) para separar los inputs del dominio (ej. `<rubrica>`, `<respuesta_alumno>`) en la fase de inyección de prompt (`prompt_builder.py`). Además, se aplica sistemáticamente **Prompt Anchoring**, repitiendo imperativamente la instrucción final de retorno JSON y la orden de usar el idioma vehicular del alumno justo en la última línea del user prompt. En el ámbito del ciclo de desarrollo, se adopta la política de **Context Reset** para las sesiones con agentes de IA.

**Consecuencias:**  
Se reducen drásticamente las alucinaciones de formato y el motor de corrección mantiene el foco cognitivo en la equidad y en el *Siguiente Paso Accionable*, blindando el comportamiento de la IA en producción independientemente de lo masiva que sea la entrada de contexto. Demuestra un conocimiento avanzado de las vulnerabilidades actuales en la arquitectura de los modelos fundacionales (Transformers).

---

### [D-039] Desacoplamiento de Calificación Numérica y Cualitativa en Pruebas Evaluables

**Estado:** ✅ Adoptada (`[v0.2]`)  
**Fecha:** Julio 2026 (18/07/2026)

**Aviso de Supersesión:** Corregida por D-042 (la escala correcta es IN, SU, BE, NT, SB) y D-043 (media ponderada determinista en backend, la IA no suma).

**Contexto:**  
La normativa LOMLOE (ej. Decreto 157/2022 de Galicia) establece una evaluación competencial y cualitativa (IN, SU, BE, NT, SB) que representa el nivel de logro del alumno al final del ciclo o curso de forma global e interdisciplinar. Sin embargo, las materias y sus instrumentos de evaluación diarios (exámenes, pruebas, murales) siguen requiriendo obligatoriamente una calificación cuantitativa/numérica (0-10) en la praxis docente y administrativa. El contrato JSON inicial (`[D-024]`) limitaba el retorno de la IA únicamente a la calificación competencial.

**Decisión:**  
Se actualiza el contrato `EvaluacionIA` (y el System Prompt) para exigir a la IA que calcule y devuelva **ambos valores desacoplados**:
1. `calificacion_numerica`: Puntuación exacta (float 0.0 - 10.0) de la prueba evaluable, derivada directamente de la media ponderada determinista en backend (la IA no suma).
2. `calificacion_cualitativa`: Mapeo cualitativo oficial para alimentar el perfil competencial a final de curso.

**Consecuencias:**  
El sistema es ahora jurídicamente perfecto y responde a la realidad del profesorado en el aula, manteniendo el espíritu competencial de la ley sin perder la precisión numérica de las tareas evaluables. Se han modificado los esquemas Pydantic para cumplir este requerimiento, registrado como cambio sensible (HitL) según Regla 6.

---

---

### D-040 — Distinción LEY vs. CONFIGURACIÓN DE CENTRO

**Contexto.** Al auditar el motor de calificación contra la normativa gallega (Decreto 156/2022 y su Orde do 26/05/2023 para Educación Secundaria Obligatoria — ESO; Decreto 157/2022 y su Orde do 26/05/2023 para Bachillerato), se detectó que el sistema trataba como obligaciones legales varios elementos que la normativa NO regula.

**Decisión.** El agente y el motor distinguen explícitamente dos categorías de reglas:
- **Obligatorio por ley** (no configurable): escalas de calificación (ESO 1-10 entero; Bachillerato 0-10 entero, sin decimales); correspondencia cualitativa oficial solo en ESO (IN=1-4, SU=5, BE=6, NT=7-8, SB=9-10); los criterios de evaluación como referente único de calificación; competencias clave expresadas en términos cualitativos.
- **Configuración de centro/departamento** (la ley no lo fija): puntuación y decimales por criterio, niveles de logro 1-4, pesos de los criterios, fórmula de media (aritmética o ponderada) y regla de redondeo.

**Consecuencia.** El agente nunca presenta una decisión de departamento como mandato legal. Los avisos de configuración se reportan en `teacherSummary`.

**Fuente.** Orde do 26/05/2023 (DOG 13/06/2023), Arts. 21.3, 22.2, 27.1, 27.4 (ESO); Arts. 17.1, 24.3, 29 (Bachillerato).

---

### D-041 — Soporte multi-etapa: campo `etapa` en `marcos_evaluacion`

**Contexto.** El producto sirve tanto ESO como Bachillerato, pero la regla de calificación cualitativa oficial solo existe en ESO. El modelo `MarcoEvaluacion` solo tenía `asignatura` y `curso` como texto libre, obligando al modelo de lenguaje a inferir la etapa.

**Decisión.** Se añade el campo `etapa: Literal["ESO","BACH"]` a `marcos_evaluacion` (y a los esquemas Pydantic asociados). En ESO la calificación oficial fuerte es la cualitativa; en Bachillerato es la numérica (0-10) y la cualitativa se marca como `"NA"` (no aplicable / orientativa).

**Consecuencia.** Migración Alembic (herramienta de migración de base de datos) con valor por defecto `"BACH"` por compatibilidad con el estado actual (Filosofía de Bachillerato); revisar manualmente los marcos de ESO al cargarlos.

---

### D-042 — Abreviatura cualitativa oficial "BE", nunca "BI" (corrige D-039)

**Contexto.** El esquema `EvaluacionIA`, la documentación y la propia **D-039** usaban `"BI"` para "Bien". La abreviatura oficial en la normativa es **"BE"** (Art. 27.1, Decreto 156/2022). El `Literal` de Pydantic rechazaba la salida correcta.

**Decisión.** Se sustituye `"BI"` por `"BE"` en el esquema, el prompt y toda la documentación (plan, backlog, glosario). Se añade a la D-039 una nota "Corregida por D-042: la escala correcta es IN, SU, **BE**, NT, SB".

**Consecuencia.** Bug corregido: la validación ya no rechaza calificaciones "Bien" correctas.

---

### D-043 — Nota de prueba por media ponderada; la IA no suma, el backend recalcula (corrige D-039)

**Contexto.** La D-039 y la descripción de `calificacion_numerica` indicaban que la nota se derivaba "de la **suma** ponderada" y que **la IA la calcula**. Sumar criterios con distintos `maxScore` produce resultados incoherentes, y delegar la aritmética en el modelo de lenguaje es una fuente de errores no auditable.

**Decisión.**
1. La nota de prueba se calcula como **media ponderada** de los criterios, normalizando cada uno a base 10 (`score/maxScore*10`) y aplicando su `peso` (%). La suma de pesos debe ser 100 % (validado en `RubricaCreate`).
2. **La IA NO suma ni calcula la nota.** El contrato `EvaluacionIA` exige que el modelo devuelva únicamente, por criterio: `score`, `maxScore` y `peso`.
3. El **backend recalcula** `calificacion_numerica` de forma determinista mediante un `@model_validator(mode="after")` que actúa como **mutador** (sobrescribe el valor), **nunca como bloqueante**: no lanza 422 si la IA envía un valor incoherente, simplemente lo corrige.
4. El frontend solo **muestra** el valor recalculado; no lo calcula.

**Consecuencia.** Se sustituye el "suma ponderada" de la D-039 por "media ponderada determinista en backend". La aritmética queda fuera del alcance del modelo de lenguaje, es auditable y reproducible.

---

### D-044 — Trazabilidad criterio → competencia clave

**Contexto.** El `RubricItem` no vinculaba cada criterio a su código oficial ni a las competencias clave. Sin esa cadena, el backend no puede agregar el grado de competencias del trimestre, que es el núcleo de la evaluación LOMLOE (Ley Orgánica de Modificación de la LOE).

**Decisión.** `RubricItem` y `CriterioRubrica` incorporan `criterio_codigo`/`criterio_codigo_oficial` y `competencias_clave` (lista de: CCL, CP, STEM, CD, CPSAA, CC, CE, CCEC).

**Consecuencia.** El backend puede reconstruir la evaluación de competencias a partir de los criterios evaluados en cada prueba.

---

### D-045 — Semántica HitL de la nota

**Contexto.** `calificacion_numerica` (con decimales) podía confundirse con la nota oficial de boletín (entero).

**Decisión.** `calificacion_numerica` es una **orientación** con decimales que el agente NO redondea. El docente decide la nota definitiva y aplica el redondeo a entero al aprobar (Human-in-the-Loop), guardándola en `nota_final`. El agente evalúa una sola evidencia; la agregación a nota de materia y competencias del trimestre la hace el backend.

**Consecuencia.** Refuerza el escudo legal HitL (D-002) y separa el rol del asistente del rol decisor del docente.

---

### D-046 — Etapa como `str` Enum de Python en lugar de tabla catálogo en BD

**Estado:** ✅ Adoptada (`refactor/multi-region-extensibility`, Issue #12 — Fase 5)  
**Fecha:** Julio 2026 (22/07/2026)

Durante la Fase 5 de la Issue #12 se evaluaron dos opciones para hacer el tipo `Etapa` extensible a futuras CC.AA.: (A) tabla `etapas_educativas` en BD y (B) `class Etapa(str, enum.Enum)` en Python. Se eligió la **Opción B** por alineación con decisiones previas — D-004 (la extensibilidad multi-autonómica ya está resuelta en el JSONB de `rubrica_completa`), D-033 (YAGNI: frecuencia de cambio de las etapas educativas ≈ cero), D-040 (las etapas son obligación legal LOMLOE, no configuración de centro) y D-041 (que ya adoptó `Literal["ESO","BACH"]`). La Opción A habría eliminado la validación automática de Pydantic en el contrato del LLM sin justificación de ganancia proporcional. Esfuerzo de implementación: 3 líneas en `models/marco.py`, cero migraciones de columna.

---

### D-047 — Adopción de Groq Vision (LPU) con fallback GPT-4o como motor multimodal

**Estado:** ✅ Adoptada (`v0.3-004`)  
**Fecha:** Julio 2026

**Contexto:** El MVP inicial (D-003) posterga el OCR/multimodal a v0.3, momento en el que la lógica de evaluación textual ya está validada. Se necesita seleccionar el motor de visión que procesará las imágenes anonimizadas.

**Opciones consideradas:**
- **GPT-4o Vision en exclusiva:** máxima calidad, pero coste recurrente incompatible con la Fase Ninja sin alta de autónomos (D-010).
- **Modelo propio de OCR entrenado:** sobreingeniería, viola YAGNI.
- **Groq Vision (`qwen/qwen3.6-27b`) como primario:** coherente con D-028 (Groq como motor primario de coste cero). *(Nota: `llama-3.2-11b/90b-vision-preview`, opción considerada originalmente, fue deprecado por Groq antes de la implementación. Ver D-051.)*

**Decisión:** Se adopta Groq Vision como motor multimodal primario, manteniendo la bifurcación plana de proveedor ya establecida en D-028 (`LLM_PROVIDER`), con fallback a `gpt-4o` cuando Groq no esté disponible o el caso de uso lo requiera. El contrato `EvaluacionIA` admite transcripción con marcadores `ILEGIBLE` y coordenadas aproximadas sin romper la validación Pydantic.

**Consecuencias:** `llm_client.py` extiende su bifurcación plana para incluir el envío de imagen (Base64 si es local, URL si es nube) en el payload multimodal. Esta decisión depende funcionalmente de D-022 (seudonimización pre-nube) — solo la imagen ya anonimizada puede llegar a este cliente.

---

### D-048 — FastAPI BackgroundTasks como cola de tareas del MVP (Celery/Redis diferido a Roadmap)

**Estado:** ✅ Adoptada (`v0.4-004`)  
**Fecha:** Julio 2026

**Contexto:** El plan de trabajo original (Bloque 6, Bloque 9) contemplaba Celery + Redis como sistema de colas para v0.4. Durante la implementación se detectó que configurar Celery en WSL añade una complejidad de entorno desproporcionada frente al valor demostrable en el MVP, y que el criterio de éxito real de v0.4 (5 correcciones simultáneas sin colapso, respuesta 202 en menos de 1 segundo) es alcanzable sin un broker dedicado.

**Opciones consideradas:**
1. **Celery + Redis desde el inicio:** arquitectura "correcta" a escala, pero bloquea el desarrollo con fricción de configuración en WSL sin aportar valor proporcional al MVP (viola YAGNI/Regla 5, Protocolo de Pausa Arquitectónica).
2. **FastAPI BackgroundTasks:** nativo, sin dependencias nuevas, suficiente para la carga de prueba definida en v0.4-004.
3. **Descartar la asincronía y usar procesamiento síncrono:** inviable, rompe la promesa de UX de confirmación inmediata (202 Accepted).

**Decisión:** Se adopta BackgroundTasks de FastAPI como mecanismo real de asincronía en el MVP (v0.4). Celery + Redis queda documentado explícitamente en el README como mejora arquitectónica futura para producción a escala, demostrando conocimiento técnico sin sobre-ingeniería prematura.

**Consecuencias:** Todos los criterios de aceptación de v0.4-001, v0.4-002 y v0.4-003 que mencionan "Celery" o "worker" se reinterpretan como BackgroundTasks en la implementación real; la mención a Celery se mantiene únicamente en v0.4-001 como ejercicio de configuración exploratoria y en el Roadmap. Esta ADR resuelve formalmente la inconsistencia detectada entre v0.4-002 (que citaba "Celery" en su criterio de aceptación) y la nota arquitectónica de v0.4-004.

---

### D-049 — Calificación cualitativa condicional por etapa (ESO vs BACH)

**Estado:** ✅ Adoptada  
**Fecha:** Julio 2026

**Contexto:** El Decreto 156/2022 (ESO) traduce el proceso competencial a una etiqueta cualitativa de cierre de acta (IN, SU, BE, NT, SB — D-042). El Decreto 157/2022 (Bachillerato) cierra actas trimestrales y finales únicamente con nota numérica del 1 al 10 con un decimal, sin etiqueta cualitativa equivalente en el expediente oficial, aunque el proceso de evaluación por competencias (Capas 1-4) se aplica igual en ambas etapas.

**Decisión:** El campo `calificacion_cualitativa` en `EvaluacionIA` es **Optional[Literal["IN","SU","BE","NT","SB"]]**, y el backend debe forzarlo a `null` cuando `etapa == "BACH"`. El desglose competencial interno (`competencias_criterios`, `rubricBreakdown`) permanece activo en ambas etapas; solo se omite la etiqueta de cierre de acta en Bachillerato.

**Consecuencias:** Corrige el ejemplo JSON de `/api/v1/evaluate` en README.md y api_correccion_plan.md, que mostraban `"NA"` como valor inventado sin respaldo normativo. Requiere validador Pydantic que fuerce `None` si `etapa == "BACH"` independientemente de lo que devuelva el LLM.

### D-050 — Estrategia de RAG Relacional (Determinista) vs RAG Vectorial

**Estado:** ✅ Adoptada  
**Fecha:** 28/07/2026

**Contexto:** Para evaluar formativamente un texto, la IA necesita conocer la rúbrica del profesor y el marco legal asociado (criterios y saberes de la LOMLOE). La tendencia general de la industria para recuperar información externa es usar RAG (*Retrieval-Augmented Generation*) semántico mediante bases de datos vectoriales (ej. ChromaDB, Pinecone). Sin embargo, en el ámbito jurídico-educativo, recuperar un artículo de ley "semánticamente parecido" es inaceptable; se requiere el articulado exacto para garantizar la legalidad de la evaluación.

**Decisión:** Se rechaza la adopción de bases de datos vectoriales para el núcleo del sistema. Se adopta una estrategia de **RAG Relacional (Determinista)**. La API recupera el contexto (Rúbrica del docente y marco normativo LOMLOE) mediante transacciones SQL precisas a través de sus `id` exactos en PostgreSQL (`rubrica_id`, `marco_id`). Estos datos estructurados se inyectan en caliente dentro del prompt que se envía a Groq.

**Consecuencias:**
1. **YAGNI & Simplicidad:** No necesitamos añadir ni mantener microservicios extra para ChromaDB ni ejecutar modelos intermedios de *embeddings*.
2. **Seguridad Legal:** La IA siempre evalúa con el 100% de la ley y los criterios vigentes inyectados de forma transaccional, eliminando la alucinación en la fase de recuperación de contexto (*Retrieval*).
3. **Robustez Arquitectónica:** Proporciona un argumento sólido y demostrable ante auditorías técnicas para justificar que la API no sufre de "ruido semántico".

### D-051 — Adopción de OpenAI (`gpt-4o-mini`) para Visión y retención de Groq para Texto (Workload Routing)

**Estado:** ✅ Adoptada  
**Fecha:** 11/08/2026

**Contexto:** La v0.3 introduce el soporte de imágenes de exámenes manuscritos. Originalmente se documentó el uso de `qwen/qwen3.6-27b` en Groq como motor Vision para mantener el coste a cero. Sin embargo, durante el *Smoke Test* (`smoke_test_vision.py`), se detectó un fallo crítico (HTTP 400): el modelo Qwen de 27B colapsa al intentar parsear el complejo esquema Pydantic anidado `EvaluacionIA` (que contiene listas de rúbricas y coordenadas) en el *JSON Mode* de Groq. 

**Opciones consideradas:**
1. **Pipeline de 2 saltos en Groq:** Usar Qwen solo para OCR simple y pasar el texto a Llama 70B para la evaluación compleja. *Rechazado:* Añade fragilidad (doble punto de fallo), incrementa la latencia y rompe el principio de simplicidad YAGNI.
2. **Google Gemini (`gemini-2.0-flash`):** Uso gratuito mediante AI Studio. *Rechazado:* Violación de YAGNI (requiere un SDK completamente distinto, refactorizando `llm_client.py`) y problemas legales (la capa gratuita de Google se reserva el derecho de entrenar con datos, violando el RGPD y AI Act para menores).
3. **OpenAI (`gpt-4o-mini`):** Reemplazo directo (drop-in) aprovechando la compatibilidad de SDK existente en `llm_client.py`. *Elegida.*

**Decisión:** Se pivota la arquitectura multimodal hacia **OpenAI (`gpt-4o-mini`)** aprovechando sus **Structured Outputs** nativos que garantizan un 100% de cumplimiento del esquema Pydantic sin errores 400. Simultáneamente, **se retiene Groq (`llama-3.3-70b-versatile`)** como motor para las peticiones de texto plano. Este diseño de *Workload Routing* (encaminamiento de cargas) permite mantener el coste a cero y velocidad extrema para correcciones de texto, invirtiendo saldo de API de OpenAI exclusivamente cuando se requiere la fiabilidad de sus "ojos" (Visión) para JSON complejos.

**Consecuencias:**
1. Demostración de madurez arquitectónica: se prioriza la **estabilidad del contrato de datos** (Structured Outputs) frente al ahorro marginal en el MVP.
2. El cliente `llm_client.py` ahora bifurca su comportamiento: el frontend enviará las peticiones con imagen dirigidas explícitamente a OpenAI, y las peticiones de texto a Groq.
3. Se blinda el proyecto contra la volatilidad de los modelos *Preview* de Groq, adoptando un motor de Producción estable.

---

### D-052 — Asignación determinista de la cualitativa ESO en backend y gobernanza del redondeo al entero de boletín

**Estado:** ✅ Adoptada  
**Fecha:** 12/08/2026

**Contexto:** El smoke test de la v0.3 reveló que el LLM (`gpt-4o-mini`) puede devolver una `calificacion_cualitativa` inconsistente con la `calificacion_numerica` final calculada por el backend (ej. retornaba `BE` para una nota de `5.0`, que legalmente es `SU` según el Decreto 156/2022). Además, surge la pregunta de quién decide a qué decimal una nota sube al siguiente entero de boletín, ya que el Decreto 156/2022 exige que la nota final sea un entero pero **no fija ninguna regla de redondeo**.

**Análisis (D-040 — LEY vs CONFIGURACIÓN DE CENTRO):**
- **Obligatorio por ley:** La nota final de boletín en ESO debe ser un entero (1-10). La escala cualitativa oficial es `IN`=1-4, `SU`=5, `BE`=6, `NT`=7-8, `SB`=9-10.
- **NO fijado por ley:** La regla de redondeo (si 5.5 sube a 6 o se queda en 5). Esto es potestad del departamento didáctico o del centro educativo.

**Decisión (dos pilares):**
1. **Asignación determinista de la cualitativa:** Se añade un tercer `model_validator` en `EvaluacionIA` (`asignar_cualitativa_legal`) que, después de que `recalcular_media_ponderada` corrija la nota numérica, asigna la cualitativa ESO de forma automática usando la escala oficial del Decreto 156/2022. Se usa **umbral de suelo** (*floor*) como criterio neutro y conservador (ej. `5.9` → `SU`). La IA ya no es responsable de esta asignación.
2. **Redondeo al entero es HitL (D-045):** La `calificacion_numerica` con decimales que produce el backend es **orientativa**. El docente (Human-in-the-Loop) ve la nota decimal y la cualitativa orientativa, aplica la regla de redondeo de su centro (que puede diferir del suelo) y firma el entero final (`nota_final`) en el endpoint de aprobación. El backend **nunca redondea**.

**Consecuencias:**
1. Se elimina una fuente de error legal: la cualitativa nunca puede contradecir la nota numérica, independientemente de lo que proponga la IA.
2. Se respeta la soberanía pedagógica del centro: el backend no impone una regla de redondeo que la ley no exige.
3. La responsabilidad del entero de boletín sigue siendo 100% humana, en línea con el EU AI Act (sistema de alto riesgo con supervisión humana significativa).

---

### D-053 — Unificación del motor LLM en OpenAI (`gpt-4o-mini`) tras deprecación de Groq Llama 3.3 70B

**Estado:** ✅ Adoptada  
**Fecha:** 14/08/2026

**Contexto:** El 14/08/2026 se recibió un aviso oficial de Groq indicando que `llama-3.3-70b-versatile` (motor de texto de referencia desde D-028) sería dado de baja el 16/08/2026. Se inició un protocolo de migración urgente con tres opciones.

**Opciones evaluadas:**
1. **`qwen/qwen3.6-27b` en Groq (Opción A):** Primer candidato recomendado por Groq. *Descartado:* error 400 (`json_validate_failed`) idéntico al documentado en D-051 para visión. El modelo Qwen no parsea fiablemente el esquema `EvaluacionIA` con `json_object`.
2. **GPT OSS 120B en Groq (Opción B):** Segundo candidato mencionado en el correo de Groq. *Descartado antes de probar:* el ID exacto del modelo en GroqCloud no es públicamente conocido y el riesgo de repetir el mismo patrón de inestabilidad de modelos Preview es alto.
3. **OpenAI `gpt-4o-mini` para texto (Opción C):** *Elegida.* Smoke test (`smoke_test_llm.py`) verde en la primera ejecución.

**Decisión:** Se unifica el motor LLM en **OpenAI (`gpt-4o-mini`)** para ambos tipos de carga (texto e imagen). El `LLM_PROVIDER=openai` y `LLM_MODEL=gpt-4o-mini` quedan como valores por defecto en `.env`. La rama de código `if provider == "groq"` se mantiene en `llm_client.py` como resiliencia latente (el operador puede activar Groq si en el futuro ofrece un modelo estable con Structured Outputs) pero no se ejecuta en la configuración estándar.

**Consecuencias:**
1. Simplificación operativa: un solo proveedor, una sola API Key activa, un solo modelo.
2. El SDK `groq` se elimina de `requirements.txt` (era redundante: `llm_client.py` usa el SDK de `openai` con `base_url` para llamar a Groq).
3. Mayor coste por petición de texto respecto a Groq (coste cero → saldo OpenAI), aceptable en MVP donde el volumen de peticiones es bajo.
4. El docstring de `evaluate_answer` se actualiza para reflejar la arquitectura real.


---

### D-054
## Limitación conocida del RAG Determinista v1: ausencia de materiales didácticos del docente como contexto evaluativo

**Estado:** ✅ Adoptada (Limitación documentada)  
**Fecha:** 18/08/2026

**Contexto:**  
La arquitectura actual implementa un **RAG Determinista** (`[Roadmap-003]`): la normativa autonómica (Decretos 156/157/2022 de la Xunta de Galicia) y la rúbrica del docente se recuperan de PostgreSQL por `marco_id` y `rubrica_id` respectivos y se inyectan como contexto estructurado en el prompt del LLM. Esta estrategia fue validada técnicamente por el mentor de AESIA (Doctor en BBDD) durante la revisión del sistema en julio de 2026.

Sin embargo, esta aproximación tiene una **limitación pedagógica real e identificada por la propia autora del sistema**: el LLM evalúa al alumno usando su conocimiento general (lo que GPT-4o-mini sabe sobre la materia) más el marco normativo y la rúbrica. El sistema **no tiene acceso** a los materiales específicos que el docente ha impartido: el libro de texto adoptado por el departamento, los apuntes propios, los ejemplos del aula, el alcance real del temario tratado hasta la prueba, ni las instrucciones concretas dadas en el examen.

Esto puede generar dos tipos de error evaluativo:
1. **Falso negativo:** Penalizar a un alumno por no aplicar un concepto que el profesor aún no había explicado en clase.
2. **Falso positivo:** Valorar positivamente una respuesta que el alumno ha copiado de una fuente externa que el profesor no reconoce como válida según su criterio de aula.

**Opciones consideradas:**
- **Ignorar la limitación y asumir que el conocimiento general del LLM es suficiente:** Aceptable en v1 donde el flujo HitL garantiza que el docente revisa y aprueba siempre la corrección antes de firmarla (`[D-002]`). El professor detectará manualmente cualquier desvío del contenido impartido.
- **RAG Semántico con materiales del docente (`[Roadmap-005]`):** Permitir al docente subir apuntes, fragmentos del libro de texto y criterios de examen. El sistema los chunkea, los embebe (embeddings) y los indexa en un vector store. Antes de evaluar, recupera los fragmentos más relevantes a la pregunta del alumno y los inyecta como contexto adicional. Esta es la evolución natural pero introduce complejidad técnica significativa (pipeline de embeddings, vector store, chunking strategy) que supera el alcance del MVP v1.

**Decisión:**  
Se documenta formalmente como **limitación conocida y aceptada** de la v1 actual, mitigada por el flujo HitL obligatorio (`[D-002]`). La evolución hacia un **RAG Semántico con materiales didácticos del docente** se planifica como `[Roadmap-005]` en el `backlog.md`.

**Consecuencias:**  
1. El `README.md` de v1.0 (`[v1.0-003]`) documentará esta limitación en la sección de arquitectura con honestidad técnica.
2. El panel PWA del docente en v0.5 mostrará un aviso recordatorio de que la IA evalúa conforme a la normativa y la rúbrica, pero no conoce los materiales específicos del aula.
3. Esta limitación refuerza el argumento pedagógico del HitL: el docente no es un mero firmante burocrático, sino el garante activo de la coherencia entre lo enseñado y lo evaluado.

---

### D-055 — Arquitectura de evaluación asíncrona mediante FastAPI BackgroundTasks (v0.4)

**Estado:** ✅ Adoptada  
**Fecha:** 20/08/2026

**Contexto:**  
En la v0.3, el endpoint `POST /api/v1/submissions/upload-and-evaluate` ejecutaba en un único ciclo HTTP la validación del archivo, el almacenamiento local, la llamada a OpenAI Vision para transcripción y la evaluación LLM. Esto causaba latencias de respuesta de 4 a 8 segundos en el cliente, bloqueando la PWA y ofreciendo una experiencia poco fluida si la conexión docente sufría interrupciones.

**Opciones consideradas:**
1. **Pipelining sincrónico mantenido:** Mantener la petición sincrónica. *Descartada:* Latencia inaceptable para producción y mala UX.
2. **Celery + Redis:** Cola de tareas distribuida y bróker de mensajes pesado. *Descartada por YAGNI (D-001):* Introduce infraestructura compleja que sobrecarga el MVP.
3. **FastAPI `BackgroundTasks` nativo:** Iniciar la tarea de procesamiento en segundo plano inmediatamente después de validar la entrega y persistir el registro inicial en estado `ANALYZING`. *Elegida.*

**Decisión:**  
Se refactoriza el endpoint `POST /api/v1/submissions/upload-and-evaluate` para responder con un estado `HTTP 202 Accepted` en menos de 500ms devolviendo un esquema `SubmissionAsyncResponse` (`submission_id`, `status="ANALYZING"`, `message`). El procesamiento pesado (transcripción Vision + evaluación LLM) se ejecuta asíncronamente mediante `BackgroundTasks.add_task(procesar_evaluacion_en_segundo_plano)`. Al finalizar, se actualiza el estado en BBDD a `REVIEW` (o `ERROR` si ocurre algún fallo no controlado) y se añade la trazabilidad en `ChangeLog`.

**Consecuencias:**  
1. Reducción drástica de la latencia percibida (<500ms).
2. Resiliencia: si el docente navega fuera de la vista o cierra la PWA, la evaluación continúa ejecutándose en el servidor y persistiéndose en la BBDD.
3. Compatibilidad fluida con el sistema de notificaciones SSE (`[v0.4-002]`) y polling.

---

*Documento creado el 08/07/2026 — Alba Camiña García con la ayuda de Antigravity AI*  
*Actualizado el 28/07/2026 — añadida D-050*  
*Actualizado el 11/08/2026 — añadida D-051 (Pivote arquitectónico a OpenAI para Visión manteniendo Groq para Texto).*  
*Actualizado el 12/08/2026 — añadida D-052 (Asignación determinista de cualitativa ESO y gobernanza del redondeo).*  
*Actualizado el 14/08/2026 — añadida D-053 (Unificación en OpenAI tras deprecación de Groq Llama 3.3 70B).*  
*Actualizado el 18/08/2026 — añadida D-054 (Limitación conocida del RAG Determinista v1 y planificación de RAG Semántico con materiales docentes como Roadmap-005).*  
*Actualizado el 20/08/2026 — añadida D-055 (Arquitectura de evaluación asíncrona mediante FastAPI BackgroundTasks).*  
*Total de decisiones registradas: 55*