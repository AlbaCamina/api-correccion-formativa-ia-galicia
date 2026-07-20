# 🤖 Contexto y Reglas de Orquestación para Agentes de IA

Este archivo proporciona contexto persistente para cualquier Agente de Inteligencia Artificial que participe en el desarrollo de la **API de Corrección Formativa con IA - Galicia** (`api-correccion-formativa-ia-galicia`).

---

## 🎯 Reglas de Codificación "PonyTail" (YAGNI & Simplicidad)

1. **Principio YAGNI (*You Aren't Gonna Need It*):** 
   * Escribe el código estrictamente necesario para cumplir con los criterios de aceptación del backlog actual.
   * Evita abstraer para el futuro, herencias complejas o "patrones de diseño por si acaso".
2. **Modularidad Plana:**
   * Prioriza la legibilidad directa del flujo sobre la fragmentación en micro-funciones o micro-archivos redundantes.
   * Estructura del backend en 4 carpetas: `models/` (esquemas y BBDD), `routers/` (endpoints y routing), `services/` (lógica y prompts de LLM) y `main.py` (inicio y middleware).
3. **Tipado Estricto con Pydantic:**
   * Utiliza tipado estricto en todas las firmas de funciones y modelos de FastAPI (`Pydantic v2`).
   * No uses diccionarios genéricos (`dict`) si la estructura es predecible; prefiere esquemas Pydantic explícitos.
4. **Optimización de Tokens:**
   * Al interactuar con el LLM, mantén los prompts concisos y centrados en las variables pedagógicas necesarias.
   * Evita comentarios redundantes o formateos innecesarios en el código.
5. **Protocolo de Pausa Arquitectónica (*Stop & Consult*) y Freno Conductual:**
   * **Separación estricta de Revisión vs. Edición:** Ante cualquier orden o verbo que implique inspección, revisión, análisis, evaluación o reflexión (*"revisa"*, *"piensa"*, *"analiza"*, *"evalúa"*, *"comprueba"*), el Agente **TIENE PROHIBIDO** ejecutar herramientas de modificación de archivos en ese turno (`replace_file_content`, `multi_replace_file_content`, `write_to_file` o comandos que alteren el repositorio). El turno debe terminar obligatoriamente con la entrega del informe de diagnóstico o consulta.
   * **Cero ediciones sin orden explícita:** Aunque un documento (`decisiones.md`, `README.md`, `backlog.md`) o un archivo de código esté desactualizado tras una revisión, el Agente **NO PUEDE MODIFICARLO** hasta que el desarrollador emita una orden directa y explícita de implementación (*"modifica"*, *"aplica"*, *"haz los cambios"*, *"adelante"*).
   * **Prohibición de parches ad-hoc:** Si al implementar o testear surge una incompatibilidad técnica, un error de API no previsto o un caso de borde que requiera añadir lógica anidada compleja (ej. fallbacks multinivel, reintentos ad-hoc o excepciones anidadas), el Agente **TIENE PROHIBIDO** parchear el código sobre la marcha para "hacer que funcione". Debe pausar y presentar al menos dos opciones arquitectónicas contrastadas contra el principio YAGNI para tomar la decisión en equipo (*Human-in-the-Loop*).
6. **Gobernanza de cambios sensibles y cierre de auditoría (`[D-035]`):**
   * **Cuándo aplica:** Si la tarea afecta a estados de negocio (`Submission.estado`, `estado_feed_forward`), permisos/autenticación, trazabilidad (`ChangeLog` / `audit_metadata`) o al contrato HitL del LLM (`EvaluacionIA`), el agente debe tratarla como cambio sensible.
   * **Impacto multinivel:** Ante un cambio sensible, el agente evalúa el impacto en los cinco artefactos clave: código, tests, `decisiones.md`, `backlog.md` y `README.md`.
   * **Criterio de cierre (4 pilares):** Una funcionalidad sensible solo se considera cerrada cuando se cumplen simultáneamente:
     1. **Diseño:** Decisión o directriz arquitectónica clara registrada en `decisiones.md` (ADR).
     2. **Implementación:** Código actualizado, coherente con la decisión, en modelos/routers/servicios.
     3. **Evidencia:** Pruebas automatizadas (`pytest`) en verde en entorno limpio.
     4. **Documentación:** `README.md` y `backlog.md` sincronizados y cualquier deuda técnica residual explícita.
   * **Trazabilidad humana:** El agente nunca atribuye a la IA acciones persistidas de cambio de estado en BBDD cuando el flujo normativo exige autorización docente (`HitL`). La IA puede proponer y aportar contexto en `audit_metadata`; el `actor` que firma cambios formativos es siempre humano (profesor o alumno, según el caso).
7. **Estandarización de Commits y Trazabilidad:**
   * Todos los commits deben seguir estrictamente el formato *Conventional Commits* (`feat:`, `fix:`, `docs:`, `style:`, `test:`) incluyendo el contexto de la modificación entre paréntesis (scope).
   * Es **obligatorio** incluir en el mensaje del commit la referencia cruzada al registro arquitectónico (ej. `[D-035]`) o a la tarea del backlog (ej. `[v0.2-009]`) que motiva el cambio, garantizando la trazabilidad probatoria del portfolio.
8. **Defensa contra Context Overflow y Lost in the Middle:**
   * El agente debe estructurar grandes bloques de texto usando delimitadores `<xml>` para facilitar la atención del modelo.
   * Al construir prompts en el backend (`prompt_builder.py`), el agente aplicará **Prompt Anchoring**, repitiendo las reglas inquebrantables (como el retorno estricto de JSON o la Simetría Lingüística del alumno) estrictamente al final del prompt.
   * En sesiones de desarrollo prolongadas, si el orquestador humano exige un *"Context Reset"*, el agente generará un resumen de cierre para iniciar una sesión nueva en limpio.

---

## 🏛️ Decisiones Arquitectónicas Clave (ADRs)

* **[D-002] Human-in-the-Loop (HitL):** El motor LLM asiste y calcula, pero el profesor siempre valida y firma la nota final (`REVIEW` -> `GRADED`). El backend debe dar soporte a este flujo de estados.
* **[D-024] Contrato JSON Estructurado:** El motor debe retornar el esquema `EvaluacionIA` que contiene `transcription`, `rubricBreakdown`, `visualMarkers`, `qualitativeAnalysis`, `calificacion_cualitativa`, `siguiente_paso_accionable` y `confidence_score`.
* **[D-027] Modo Dual de Rúbrica:** Peticiones de corrección aceptan el campo `modo_evaluacion` que puede ser `COMBINADO` (rúbrica + saberes Xunta) o `AUDITORIA_CURRICULAR` (la IA además evalúa la coherencia pedagógica de la rúbrica docente contra la ley).
* **[D-028] Groq LPU Primario:** El backend por defecto utiliza `llama-3.3-70b-versatile` a través del cliente de Groq (aprovechando compatibilidad con el SDK de OpenAI), controlable mediante la variable `LLM_PROVIDER` del `.env`.

---

## 📂 Estructura del Proyecto

```
api-correccion/
├── backend/
│   ├── main.py                  # Punto de entrada de FastAPI y middleware
│   ├── models/                  # Esquemas Pydantic y modelos SQLAlchemy
│   │   └── __init__.py
│   ├── routers/                 # Enrutadores y endpoints de FastAPI
│   │   └── __init__.py
│   └── services/                # Prompt builders, cliente LLM e integraciones
│       └── __init__.py
├── smoke_test_llm.py            # Test standalone del contrato JSON
├── decisiones.md                # Registro de decisiones de arquitectura
└── backlog.md                   # Historias de usuario y criterios de aceptación
```

---

*Cualquier código añadido debe respetar estas directrices para mantener la consistencia y mantenibilidad del portfolio.*

---

## 📚 Contexto Normativo de Calificación (LEER ANTES DE TOCAR EL MOTOR DE EVALUACIÓN)

Esta API califica conforme a la normativa LOMLOE (Ley Orgánica de Modificación de la LOE) vigente en Galicia: Decreto 156/2022 y Orde do 26/05/2023 (Educación Secundaria Obligatoria — ESO); Decreto 157/2022 y Orde do 26/05/2023 (Bachillerato).

### Regla de oro: LEY vs. CONFIGURACIÓN DE CENTRO (D-040)
Nunca presentes una decisión de centro como si fuera obligación legal.

**Obligatorio por ley (no configurable):**
- Escala ESO: entero 1-10, sin decimales. Escala Bachillerato: entero 0-10, sin decimales.
- Cualitativa oficial SOLO en ESO: `IN`=1-4, `SU`=5, `BE`=6, `NT`=7-8, `SB`=9-10. (Bien se abrevia **BE**, nunca BI — D-042).
- Los **criterios de evaluación** son el referente único de calificación. Los **saberes básicos** son solo contenido de referencia.
- Las **competencias clave** se expresan en términos cualitativos, no como media numérica oficial.

**Configuración de centro/departamento (la ley NO lo fija):**
- Decimales por criterio, niveles de logro 1-4, pesos de criterios, fórmula de media (aritmética/ponderada) y regla de redondeo.

### Reglas de implementación fijadas
- **Etapa explícita (D-041):** usar el campo `etapa` (`ESO`/`BACH`) de `marcos_evaluacion`. No inferir la etapa del texto de `curso`.
- **Media ponderada (D-043):** la nota de prueba = media ponderada de criterios normalizados a base 10 (`score/maxScore*10`) por su `peso` (%). Los pesos suman 100 %.
- **Trazabilidad (D-044):** cada criterio lleva `criterio_codigo` y `competencias_clave` (CCL, CP, STEM, CD, CPSAA, CC, CE, CCEC).
- **Semántica HitL (D-045):** `calificacion_numerica` es orientativa con decimales; el agente NO redondea. El docente decide y redondea al aprobar (`nota_final`). El agente evalúa una sola evidencia; la agregación al trimestre la hace el backend.

### Valores válidos del contrato `EvaluacionIA`
- `calificacion_cualitativa`: `IN | SU | BE | NT | SB | NA` (usar `NA` en Bachillerato).
- `visualMarkers.type`: `ERROR | MEJORA | CORRECTO | error_excluido` (nunca `GRAMMAR_ERROR`).
- `etapa`: `ESO | BACH`.

### Adaptaciones NEAE (Necesidades Específicas de Apoyo Educativo) — D-023
Si hay adaptaciones (p. ej. `excluir_ortografia`), detectar las faltas, listarlas en `ortografia_detectada` y `errores_excluidos_por_adaptacion`, y NO penalizar por ellas.
