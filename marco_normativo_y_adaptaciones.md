# 🏛️ Marco Normativo de Evaluación y Adaptaciones Curriculares (NEAE / NEE)
**Proyecto:** API de Corrección Formativa con IA (`api-correccion-formativa-ia-galicia`)  
**Fecha:** Julio 2026  
**Ámbito Normativo Principal:** Galicia (Xunta de Galicia — Consellería de Educación) + LOMLOE / AI Act

---

## 📖 Resumen Ejecutivo

El presente documento unifica el estudio de **investigación normativa y pedagógica** con el **diseño arquitectónico y de base de datos** del módulo de equidad e inclusión de **API de Corrección Formativa con IA (`api-correccion-formativa-ia-galicia`)** (`[D-023]`). 

El objetivo primordial del módulo es garantizar el **derecho legal del alumnado con Necesidades Específicas de Apoyo Educativo (NEAE)** a una evaluación justa, equitativa y adaptada a sus características personales, impidiendo penalizaciones automáticas e injustas (por ejemplo, descuentos por faltas de ortografía en alumnado con dislexia) sin que la Inteligencia Artificial asuma roles de diagnóstico o viole la privacidad del menor.

---

## 🏛️ PARTE 1 — Investigación Normativa y Taxonomía Pedagógica

### 1.1. Doble Circuito Operativo de Calificación en Galicia (Materias vs. Competencias)

Antes de abordar las adaptaciones curriculares, QIA-Correction se cimienta sobre la legislación general de evaluación y la práctica real y cotidiana en las juntas de evaluación y en las herramientas oficiales de la Xunta de Galicia (Decretos 156/2022 y 157/2022, y Orden de 26 de mayo de 2023), operando bajo un **Doble Circuito de Calificación**:

1. **Circuito de Materias (Calificación Numérica Cotidiana, Trimestral y Final Ordinaria):**  
   En las evaluaciones trimestrales (1ª, 2ª, 3ª) y en la evaluación final ordinaria/extraordinaria, cada asignatura (*Matemáticas, Lengua Castellana, Bioloxía e Xeoloxía, Historia...*) se califica y cierra en las actas con **números enteros del 1 al 10** (adjuntando un decimal en Bachillerato). Para obtener ese número trimestral, a lo largo de las semanas y meses del curso el docente califica el día a día y las **pruebas o instrumentos evaluables** con una nota numérica cotidiana en su cuaderno de profesor (ej. *"Tienes un 7,2 en el mural de cartulina"*, *"Un 8,5 en la presentación de Canva"*, *"Un 6,4 en el control de saberes básicos"*). Estas notas numéricas cotidianas son indispensables para que el profesor pueda ponderar sus instrumentos de evaluación y para que el alumno (y su familia) comprendan con exactitud matemática y precisión su evolución real mes a mes.
   
   En la Secundaria y Bachillerato actual, una **prueba o instrumento evaluable (Omni-canalidad total)** abarca un abanico riquísimo de tres grandes soportes que QIA-Correction procesa con el mismo rigor:
   * **Soportes físicos y creativos:** Murales de cartulina infográficos colgados en la pared, maquetas, prácticas de laboratorio en papel o mapas conceptuales a mano (mediante captura fotográfica).
   * **Soportes digitales:** Presentaciones grupales o individuales diseñadas en *Canva*, *Google Slides* o *Genially*, redacciones online en plataformas escolares o cuestionarios interactivos.
   * **Soportes tradicionales:** Exámenes escritos, comentarios de texto manuscritos o resolución de problemas matemáticos en folio.
2. **Circuito de Competencias Clave (Cruce Matricial Inter-Materias):**  
   Las 8 Competencias Clave del currículo (*CCL, STEM, CD, CPSAA, CC, CE, CCEC, CP*) no son evaluadas aisladamente por un único profesor ni materia. Al final del curso, el sistema informático del centro (ej. XADE) realiza un **cruce e intersección matricial** de las calificaciones de los criterios de evaluación (`criterio_id`) acumulados en todas las asignaturas impartidas al alumno. De ese cruce global brota la calificación cualitativa oficial del informe competencial y de titulación: *Insuficiente (IN)*, *Suficiente (SU)*, *Bien (BI)*, *Notable (NT)* y *Sobresaliente (SB)*.
3. **El Rol Sincronizador de QIA-Correction:**  
   Al evaluar una prueba concreta en el día a día, el motor de IA devuelve simultáneamente la **nota numérica cotidiana (`nota_numerica`)** para alimentar el cuaderno del profesor y el cierre trimestral de la materia, y la **calificación cualitativa con desglose criterial (`competencias_criterios`)** para nutrir de forma transparente y auditable el registro inter-materias del colegio.

### 1.2. Autonomía Pedagógica y Criterios Transversales de Centro (Art. 120 LOMLOE / PEC / CCP)

El **Artículo 120 de la LOMLOE** y los Decretos autonómicos confieren autonomía pedagógica y organizativa a los centros docentes. La **Comisión de Coordinación Pedagógica (CCP)** y el **Claustro de Profesores** de cada instituto definen en su Proyecto Educativo de Centro (PEC) los **Criterios y Acuerdos Transversales de Evaluación**, de obligado cumplimiento en todos los departamentos didácticos:

1. **Acuerdo de Corrección Lingüística y Ortográfica de Centro:** Baremo común de penalización o valoración ortográfica y de expresión para materias no lingüísticas y lingüísticas (ej. restar 0,1 por falta en materias científicas hasta 1,5 puntos, y 0,25 en lingüísticas hasta 3 puntos).
2. **Criterio Transversal de Presentación y Formato:** Porcentaje de la nota (habitualmente 5% - 10%) reservado para legibilidad, orden, márgenes o rigor formal (tanto en pruebas escritas como en murales de cartulina o presentaciones digitales en *Canva*).
3. **Criterio de Uso y Corrección de la Lingua Galega:** Integración de la normalización lingüística en las materias impartidas en gallego según el Proyecto Lingüístico de Centro (PLC).

### 1.3. Marco Legal Específico de Atención a la Diversidad (LOMLOE y Decreto 229/2011)

Sobre el marco general anterior, la flexibilización y adaptación del currículo para estudiantes que lo precisen queda regulada por:

1. **Ley Orgánica 3/2020 (LOMLOE):** Consagra los principios del **Diseño Universal para el Aprendizaje (DUA)** y la equidad educativa como pilares fundamentales del currículo, estableciendo que la evaluación debe ser continua, formativa y adaptada a las necesidades de cada estudiante.
2. **Decreto 229/2011, de 2 de diciembre, por el que se regula la atención a la diversidad del alumnado de los centros docentes de la Comunidad Autónoma de Galicia:**  
   Es la norma principal de la Xunta de Galicia en la materia. Dictamina que las medidas de atención a la diversidad garantizarán el acceso, la permanencia y la progresión del alumnado, obligando a adaptar los instrumentos de evaluación a las dificultades específicas de aprendizaje o discapacidades.
3. **Orden de 8 de septiembre de 2021:**  
   Regula el procedimiento para la elaboración del Informe Psicopedagógico por parte del Departamento de Orientación del IES y la aplicación de adaptaciones de acceso y de evaluación. Especifica los criterios de flexibilización en pruebas escritas y tiempos.

### 1.4. Perfiles Frecuentes en el Aula y Medidas Específicas de Evaluación

En una clase estándar de 30 alumnos de ESO o Bachillerato en Galicia, el docente se encuentra habitualmente con los siguientes perfiles neurodivergentes o con dificultades específicas, para los cuales el Departamento de Orientación preceptúa medidas concretas:

| Perfil Diagnóstico | Siglas / Nivel | Dificultad Principal | Medida Normativa en Pruebas Escritas |
|---|---|---|---|
| **Dislexia / DEA** (Dificultades Específicas de Aprendizaje) | DEA / Medida Ordinaria | Inversión de letras, omisión de tildes, problemas fonológicos y de ortografía arbitraria | **No penalización por errores ortográficos o de puntuación.** Valoración exclusiva del contenido y razonamiento. Prioridad de comprensión global. |
| **TDAH** (Trastorno por Déficit de Atención e Hiperactividad) | NEAE / Medida Ordinaria o ACNS | Fatiga cognitiva rápida, descuidos por impulsividad, desorganización espacial en el folio | **Ampliación de tiempo (ej. +25%).** Fragmentación de preguntas complejas en sub-apartados. Resaltado visual de palabras clave en enunciados. |
| **TEA Grado 1** (Trastorno del Espectro Autista / Síndrome de Asperger) | NEE / ACNS o ACS | Literalidad en la interpretación del lenguaje, dificultad ante preguntas abiertas y ambiguas | **Enunciados directos y estructurados.** Evitar dobles negaciones, ironías o preguntas implícitas. Uso de apoyos visuales o esquemas. |
| **Altas Capacidades Intelectuales** | NEAE / ACIS | Disincronía, aburrimiento ante tareas mecánicas, pensamiento divergente | **Valoración de soluciones creativas o no estándares.** Posibilidad de profundización y enriquecimiento curricular en la respuesta. |

### 1.5. Diagnóstico de la Realidad Docente en Galicia: Necesidades, Dificultades y Soluciones QIA-Correction

El estudio de los comunicados sindicales en Galicia (*CIG-Ensino, ANPE Galicia, UGT-SP*), publicaciones docentes y foros de profesores de Educación Secundaria revela un diagnóstico unánime: **el profesorado no rechaza el espíritu pedagógico de la evaluación competencial (LOMLOE / Decretos 156/157/2022), sino el colapso burocrático y técnico que su implementación manual impone en las aulas**. 

A continuación se sintetizan las cuatro grandes dificultades del día a día en los IES gallegos y la respuesta tecnológica diseñada en QIA-Correction:

1. **La "Neolengua Burocrática" y la Explosión Combinatoria de Registros:**
   * *El Dolor Docente:* El paso de calificar contenidos aislados a evaluar una jerarquía arborescente de ítems (*Competencias Clave → Descriptores Operativos → Competencias Específicas → Criterios de Evaluación*) ha multiplicado exponencialmente la carga administrativa. En un departamento con 150 alumnos (5 grupos de 30), evaluar 4 criterios por examen exige 600 registros manuales y ponderaciones por prueba.
   * *Respuesta QIA-Correction:* El docente sube la foto o documento digital de la prueba evaluable. El motor LLM cruza automáticamente la entrega con la Programación del Departamento (`marcos_evaluacion en JSONB`) y devuelve al instante el desglose criterial y la nota numérica/cualitativa de cada alumno, eliminando el 100% de la fricción burocrática del registro.
2. **La Paradoja de las Rúbricas (Falta de Tiempo vs. Seguridad Jurídica):**
   * *El Dolor Docente:* El profesorado reconoce que evaluar mediante rúbricas es el método más equitativo y seguro para evitar reclamaciones ante la inspección educativa. Sin embargo, diseñar, calibrar y rellenar rúbricas manuales para cada instrumento de evaluación consume una cantidad inasumible de horas fuera del horario lectivo.
   * *Respuesta QIA-Correction:* Incorporamos el **Generador Asistido de Rúbricas (Copiloto Pre-Corrección en Capa 4)**. El profesor aporta el enunciado o describe la tarea en 10 segundos, y la IA propone automáticamente la tabla de evaluación en 4 niveles (*IN, SU, BI, NT/SB*) vinculada al decreto gallego, reduciendo el tiempo de preparación de horas a segundos.
3. **Incertidumbre en la Ponderación y el "Paso a la Calificación Final" (XADE):**
   * *El Dolor Docente:* Existe inseguridad jurídica a la hora de transformar las valoraciones cualitativas de los criterios en la calificación final de la materia en XADE o en los boletines trimestrales.
   * *Respuesta QIA-Correction:* Nuestro contrato JSON (`Structured Output` / `[D-024]`) devuelve de forma dual y sincronizada tanto la **Nota Numérica Cotidiana (`nota_numerica`)** para la gestión diaria del cuaderno del docente, como la **Calificación Cualitativa (`calificacion_cualitativa`)** justificada criterialmente con su índice de confianza (`confidence_score`), garantizando un respaldo probatorio total bajo el *AI Act* (*Human-in-the-Loop*).
4. **Parálisis y Riesgo de Error en Adaptaciones Curriculares Masificadas:**
   * *El Dolor Docente:* Con ratios de 30 alumnos y una media de 3 a 5 estudiantes con adaptaciones curriculares en cada aula (*Dislexia, TDAH, TEA, Altas Capacidades*), el docente se arriesga constantemente a penalizar por error a un alumno que tiene derecho legal a la exclusión de faltas ortográficas o a una escala de corrección diferente.
   * *Respuesta QIA-Correction:* La **Capa 5 (`adaptaciones_alumno en JSONB`)** actúa como filtro soberano de equidad. Separa automáticamente los errores excluidos por diagnóstico en marcadores grises neutros (*GRAY_NEUTRAL*) sin afectar a la nota final del contenido, protegiendo al menor y liberando al profesor de cálculos paralelos en tiempo real.

### 1.6. Situaciones de Aprendizaje (SdA), Equipotencialidad Criterial y Ponderación de Instrumentos en QIA-Correction

El modelo de evaluación competencial prescrito en los Decretos gallegos 156/157/2022 y la Orden de 26 de mayo de 2023 exige una transformación profunda en cómo se conciben las actividades, cómo se ponderan los ítems y cómo opera el cálculo matemático en los centros educativos:

1. **Las Situaciones de Aprendizaje (SdA) como Contenedor Padre (`Parent Container`):**
   * *Mandato Normativo:* Una Situación de Aprendizaje no es un tema del libro ni un examen aislado; es una propuesta metodológica o tarea reto contextualizada (en un entorno real o simulado cercano al alumnado) que moviliza e integra los saberes básicos para resolver un problema. Su trazabilidad es innegociable: `[Situación de Aprendizaje / Reto]` → moviliza `[Saberes Básicos]` → para desarrollar `[Competencias Específicas]` → que se miden mediante `[Criterios de Evaluación]` → vinculados al `[Perfil de Salida / Descriptores Operativos]`.
   * *Implementación en QIA-Correction:* En la `Capa 2` (Programación Didáctica), el docente estructura la base de datos creando la entidad `situacion_aprendizaje_id`. Todas las pruebas o instrumentos evaluables omni-canal realizadas por el estudiante durante esa unidad se asocian a dicho contenedor padre, permitiendo al sistema consolidar y certificar el nivel cualitativo de las competencias al finalizar el reto.
2. **Ponderación de Criterios vs. Instrumentos y Principio de Equipotencialidad:**
   * *Legalidad estricta (`Criterios > Instrumentos`):* Según la LOMLOE, la calificación no se pondera sobre instrumentos ("el examen vale el 60% y el cuaderno el 40%"), lo cual resulta contrario a derecho. Los instrumentos (el mural, la redacción en *Canva*, la prueba escrita) son únicamente **medios o soportes** de recogida de evidencias. Lo que posee calificación y peso oficial en la nota son los **Criterios de Evaluación (`criterio_id`)**.
   * *Equipotencialidad por defecto:* Salvo disposición explícita en contra por parte del departamento en su programación didáctica (`Capa 2`), todos los criterios de evaluación asociados a las competencias específicas se consideran **equipotenciales** (tienen idéntico valor en la nota de la materia). No obstante, la autonomía pedagógica permite que el departamento asigne porcentajes diferenciados en `JSONB` (`peso_en_materia`) a aquellos criterios nucleares o de desarrollo continuo a lo largo del curso.
3. **El Motor Matemático Invisible en 3 Pasos:**
   Para descargar al docente de cálculos aritméticos complejos y asegurar compatibilidad con la plataforma autonómica oficial **XADE (`Xestión Administrativa da Educación`)**, QIA-Correction opera en tres fases sincronizadas:
   * **Fase 1 (Nota Numérica Cotidiana por Instrumento):** Al corregir un instrumento concreto (ej. un mural de cartulina donde el Criterio 1.1 vale un 70% y el Criterio 3.2 un 30% local), el LLM evalúa ambos ítems (`8.0` y `6.0`) y calcula la **Nota Numérica Cotidiana (`nota_numerica: 7.4`)** que el docente registra en su cuaderno diario para retroalimentación inmediata del estudiante.
   * **Fase 2 (Acumulación en el Historial de Criterios):** En segundo plano, QIA-Correction almacena y actualiza el historial criterial del alumno (`registro_criterios_alumno`), acumulando las evidencias obtenidas en los distintos instrumentos omni-canal.
   * **Fase 3 (Cierre de Actas en XADE):** Al celebrarse las juntas de evaluación trimestral u ordinaria, el motor calcula automáticamente la nota media o formativa por cada `criterio_id` (aplicando la equipotencialidad o el porcentaje de la `Capa 2`) y entrega al docente el informe numérico y cualitativo listo para su traslación oficial a las actas de **XADE**.
   * **El Bucle de Refuerzo del Feed Forward en Pruebas Sucesivas (`[D-026]`):** Para que el "Siguiente Paso Accionable" no quede en el olvido ni sobrecargue al docente con correcciones extras, QIA-Correction activa un bucle de retorno automático. Cuando el estudiante entrega su **siguiente prueba evaluable** dentro de la misma Situación de Aprendizaje, el prompt del LLM recibe en contexto el campo `siguiente_paso_accionable` que el alumno tenía pendiente de la tarea anterior. Si el alumno aplicó la mejora en esta nueva entrega, la IA lo reconoce y le otorga una **felicitación explícita de refuerzo positivo** en su nuevo informe formativo (ej. *"¡Excelente progreso! En el mural anterior tenías pendiente mejorar la concordancia temporal y en esta redacción lo has dominado por completo"*), cambiando el estado en base de datos a `VERIFICADO_PRÓXIMA_PRUEBA`.

### 1.7. Cuadro de Auditoría de Coherencia y Cumplimiento Integral (Legal, Normativo, Administrativo y Técnico)

La arquitectura y diseño de QIA-Correction han sido sometidos a un contraste exhaustivo cruzando el marco jurídico estatal y autonómico, las regulaciones de ciberseguridad e inteligencia artificial, las directrices pedagógicas gallegas y el estado del arte técnico, arrojando una **coherencia integral hermética** en todas sus dimensiones:

| Dimensión | Requisito / Riesgo en el Ecosistema Educativo | Blindaje y Solución Implementada en QIA-Correction | Estado de Coherencia |
|---|---|---|---|
| **⚖️ LEGAL (RGPD / LOPDGDD)** | Protección absoluta de datos de menores de edad y salvaguarda de datos médicos o psicopedagógicos (NEAE/NEE). | **`[D-022]`**: Recorte local (*Client-Side*) en PWA mediante Canvas de los 3 cm de cabecera antes de subir al *Object Storage*.<br>**`[D-014]`**: Cláusula *Zero Data Retention* en llamadas a API LLM.<br>**`[D-023]`**: Seudonimización con `alumno_id` y alertas visuales grisáceas (*GRAY_NEUTRAL*) sin revelar diagnóstico médico al prompt. | 🟢 **100% BLINDADO** |
| **🇪🇺 LEGAL (*AI Act* / Europa)** | Prohibición de que una IA actúe como autora de decisiones sumativas o de actos administrativos sin supervisión humana real. | **`[D-024]`**: *Confidence Score* (`0.0 - 1.0`). Alerta preventiva obligatoria si `< 0.75` por caligrafía confusa o ambigüedad.<br>**`Soberanía del Acto Administrativo (HitL)`**: La IA asiste, propone y autocompleta, pero la aprobación (`GRADED`) y firma de actas es competencia exclusiva del profesor. | 🟢 **100% BLINDADO** |
| **🏛️ ADMINISTRATIVA (ENS / AMTEGA / XADE)** | Prohibición estricta del *Esquema Nacional de Seguridad* de inyectar datos por APIs no autorizadas directamente en XADE. | **`[D-025]`**: Cero contacto entre nube privada y servidores públicos. Conexión local por exportación de plantilla oficial Excel/CSV (`v0.5`) o autocompletado asistido por RPA en navegador (`v0.8/v1.0`), firmando el docente con Chave365/certificado digital. | 🟢 **100% BLINDADO** |
| **📚 NORMATIVA (Decretos 156/157/2022 Galicia)** | Evaluación competencial cualitativa, doble circuito numérico/cualitativo, SdA como eje motor y equipotencialidad criterial. | **Doble Circuito (`Sección 1.1`)**: Simultaneidad de nota numérica cotidiana (`nota_numerica`) con cruce cualitativo criterial (`calificacion_cualitativa: IN, SU, BI, NT, SB`).<br>**SdA como Contenedor Padre (`Sección 1.6`)**: Agrupa pruebas omni-canal y pondera **Criterios (`criterio_id`)** por equipotencialidad o porcentaje en `JSONB` de `Capa 2`. | 🟢 **100% BLINDADO** |
| **⚙️ TÉCNICA Y ARQUITECTURA** | Gestión relacional eficiente del currículo sin latencias, evitando la rigidez y sobrecarga de tablas relacionales monolíticas. | **Jerarquía en 5 Capas Relacionales (`JSONB`)**: Capa 1 (Decreto Xunta), Capa 2 (Programación/SdA), Capa 3 (Transversales PEC), Capa 4 (Rúbrica Copiloto), Capa 5 (Adaptaciones NEAE).<br>**`[D-026]`**: Seguimiento formativo del paso accionable (`estado_feed_forward`) sin sobrecarga sumativa. | 🟢 **100% BLINDADO** |

---

## 🛠️ PARTE 2 — Arquitectura, Diseño de Base de Datos e Integración en QIA-Correction

### 2.1. Jerarquía Normativa en 5 Capas Relacionales Dinámicas (`JSONB`)

Para combinar con exactitud milimétrica la normativa pública, las programaciones didácticas de cada departamento, las normas del centro, la creación de rúbricas del docente y las adaptaciones de los estudiantes sin saturar la burocracia escolar, el motor de **QIA-Correction** opera bajo una jerarquía de **5 Capas Relacionales Dinámicas (`JSONB`)** inyectadas en el prompt y procesadas por el LLM multimodal:

```
[CAPA 1: Marco Normativo General (Xunta de Galicia)]
   → Catálogo maestro oficial de Competencias Clave, Específicas y Criterios del Decreto 156/157/2022 (marcos_evaluacion en JSONB).
         ↓
[CAPA 2: Programación Didáctica del Departamento / IES]
   → La selección anual o trimestral que hace el departamento docente en su centro: qué Saberes Básicos (contenidos) y Criterios exactos se trabajan y ponderan en cada evaluación o unidad didáctica.
         ↓
[CAPA 3: Criterios Transversales y PEC del IES (Autonomía de Centro)]
   → Acuerdos del Claustro / CCP aplicables a todas las pruebas del colegio (ej. restar 0,1 por falta ortográfica o porcentaje dedicado a la presentación y formato formal).
         ↓
[CAPA 4: Rúbrica Asistida de la Prueba o Instrumento Evaluable (IA Copiloto + El Profesor)]
   → El docente aporta el enunciado o describe la tarea o prueba evaluable (mural de cartulina, redacción en Canva, examen manuscrito o exposición). El motor LLM cruza las Capas 1, 2 y 3 para proponer automáticamente una Rúbrica en 4 niveles de logro (IN, SU, BI, NT/SB) conectada a la ley (*Killer Feature de reducción burocrática*). El profesor la valida o ajusta en su PWA con un clic (Human-in-the-Loop).
         ↓
[CAPA 5: Adaptación Curricular del Alumno NEAE (JSONB individual)]
   → El escudo protector de equidad. Al corregir la prueba de cada alumno concreto, este filtro soberano SOBREESCRIBE o flexibiliza las Capas 3 y 4 para defender los derechos del estudiante con Dislexia/DEA, TDAH, TEA o Altas Capacidades según el Decreto 229/2011.
```

### 2.2. El Principio de Inyección Explicita (*AI Never Diagnoses*)

Para cumplir escrupulosamente con el **Reglamento Europeo de Inteligencia Artificial (EU AI Act)** y el **RGPD / LOPDGDD (Art. 7)**, QIA-Correction establece tres reglas arquitectónicas innegociables:
1. **La IA jamás infiere ni diagnostica adaptaciones:** El LLM multimodal no tiene permiso para deducir de la caligrafía o redacción que un alumno tiene dislexia o TDAH.
2. **El docente o el centro es el único soberano de la configuración:** El profesor asigna de forma explícita las reglas de adaptación en la ficha del alumno.
3. **Los datos de salud están aislados:** Los informes médicos u orientativos nunca se suben ni procesan en la nube; la IA únicamente recibe reglas de comportamiento técnico anonimizadas y asociadas a un `alumno_id`.

### 2.3. Modelo de Datos y Flexibilidad Relacional (`JSONB`)

Para evitar migraciones rígidas de esquema SQL cada vez que una CCAA modifique las medidas ordinarias o extraordinarias, la tabla `submissions` (o la relación con el alumno) incorpora el campo `adaptaciones_alumno` en formato **`JSONB` nullable** en PostgreSQL:

```json
// Ejemplo de estructura JSONB inyectada al evaluar el examen de un alumno con Dislexia y TDAH
{
  "codigo_adaptacion": "NEAE-DEA-001",
  "medidas_evaluacion": {
    "ignorar_penalizacion_ortografica": true,
    "ignorar_penalizacion_tildes_puntuacion": true,
    "valorar_contenido_sobre_forma": true,
    "tiempo_extra_porcentaje": 25,
    "estilo_feedback_requerido": "estructurado_en_pasos_cortos"
  },
  "observaciones_prompter": "El alumno presenta DEA (dislexia fonológica). No descontar puntuación por faltas de ortografía (b/v, h, g/j, s/x) ni ausencia de tildes. Notificar los errores en canal neutro para seguimiento docente, pero otorgar la nota de contenido íntegra."
}
```

### 2.4. Contrato JSON Enriquecido devuelto por el LLM (`[D-023]` + `[D-024]`)

Cuando el prompt del motor recibe el campo `adaptaciones_alumno`, el comportamiento de salida (`Structured Output`) modifica su balance de cálculo y separa los errores en dos listas distintas dentro del JSON final:

```json
{
  "evaluacion_id": "sub_99812_corr",
  "alumno_id": "ALU_GAL_0042",
  "nota_numerica": 8.5,
  "calificacion_cualitativa": "NT",
  "confidence_score": 0.92,
  "competencias_criterios": [
    {
      "criterio_id": "CE.ESO.4.LEN.2.1",
      "descriptor": "Capacidad de argumentación y síntesis",
      "nivel_logro": "Sobresaliente",
      "puntuacion_obtenida": 4.5,
      "puntuacion_maxima": 5.0
    }
  ],
  "desglose_lingüistico": {
    "errores_penalizados": [],
    "errores_excluidos_por_adaptacion": [
      {
        "tipo": "ortografia_arbitraria",
        "palabra_original": "haber si venimos",
        "correccion": "a ver si venimos",
        "motivo_exclusion": "Excluido de penalización según regla DEA / Dislexia (Decreto 229/2011 Galicia)",
        "coordenada_visual": { "x": 142, "y": 510, "page": 1 }
      },
      {
        "tipo": "omision_tilde",
        "palabra_original": "solucion",
        "correccion": "solución",
        "motivo_exclusion": "Excluido según regla DEA",
        "coordenada_visual": { "x": 310, "y": 620, "page": 1 }
      }
    ]
  },
  "marcadores_visuales": [
    {
      "tipo": "ERROR_EXCLUIDO_NEAE",
      "color_interfaz": "GRAY_NEUTRAL",
      "mensaje": "Falta de ortografía detectada pero NO penalizada (Adaptación Dislexia activa)"
    }
  ],
  "siguiente_paso_accionable": "Tu argumentación teórica sobre las causas del conflicto es excelente y muy clara. Como próximo reto de contenido, añade un ejemplo histórico concreto en el tercer párrafo para consolidar el nivel Sobresaliente."
}
```

### 2.5. Comportamiento en la Interfaz del Profesor (PWA Dual)

En el panel frontal de corrección (*Human-in-the-Loop*):
* **Marcadores visuales diferenciados:** Los errores conceptuales que restan nota se marcan con recuadros **rojos** o **naranjas**. Los errores ortográficos excluidos por adaptación NEAE se renderizan con recuadros **grises neutros** y un icono azul de información (`ℹ️ Adaptación activa`).
* **Soberanía docente total:** El profesor visualiza en la cabecera el *Badge* de la adaptación aplicada. Si considera que en una redacción de Lengua Castellana específica sí debía evaluarse una falta concreta, puede activar/desactivar la exclusión con un solo clic en el interruptor local, recalculándose el borrador antes de pulsar `Aprobar y Bloquear (GRADED)`.

---

## 🎯 Conclusión Arquitectónica

Al integrar la legislación gallega (`Decretos 156/157/2022` y `Decreto 229/2011`) con un modelo relacional dinámico (`JSONB`) y una IA que separa técnica de diagnóstico, **QIA-Correction** se posiciona como una herramienta líder en equidad educativa. Permite a los centros cumplir con la inspección y la ley de protección de datos al tiempo que humaniza la evaluación de los estudiantes neurodivergentes y general.

---

*Documento consolidado el 10/07/2026 — Antigravity para Alba Camiña García*  
*Referencia de Decisiones de Arquitectura: [D-023] y [D-024] en `decisiones.md`*