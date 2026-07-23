# Auditoría interna en api-correccion-formativa-ia-galicia

## 1. Qué entendemos por auditoría interna

En este proyecto, **auditoría interna** no es un evento puntual al final, sino un estado continuo de preparación: cada módulo relevante debe poder responder, en cualquier momento, a estas cuatro preguntas básicas:

1. ¿Qué decisión arquitectónica se tomó y por qué? (`decisiones.md` / ADRs).
2. ¿Dónde está implementada esa decisión en el código? (modelos, routers, servicios).
3. ¿Qué pruebas demuestran que el comportamiento es el esperado? (`pytest`, tests en verde).
4. ¿Dónde está descrito y planificado el cambio? (`README.md`, `backlog.md` y deuda técnica).

Cuando esas cuatro preguntas tienen respuesta clara y consistente, consideramos que ese módulo está **auditado y listo** para revisión técnica o defensa de portfolio.

## 2. Criterio de módulo "auditado" vs. "pendiente"

Un área del sistema (por ejemplo, `feed-forward`, `evaluation_router`, autenticación, Alembic) se clasifica en uno de estos estados:

- **Auditado y cerrado:**  
  - Hay una ADR vigente en `decisiones.md` que describe el diseño.  
  - El código refleja esa decisión (estado actual en `main`).  
  - Existe cobertura de tests relevante en verde.  
  - `README.md` y `backlog.md` están sincronizados con ese comportamiento y cualquier deuda residual está explícita.

- **Parcial / pendiente de auditoría:**  
  Falta al menos uno de los elementos anteriores (decisión, implementación, evidencia, documentación). En este caso, la auditoría interna considera el área "en curso", no lista para revisión externa.

Este criterio corresponde a la política formal descrita en **[D-035] (Gobernanza de cambios sensibles y criterio de cierre de auditoría técnica)** y a la **Regla 6 de `AGENTS.md`**, que obligan a verificar los cuatro pilares para cambios sensibles.

## 3. En qué punto estamos hoy

A fecha de esta entrada:

- El bloque `feed-forward` + `ChangeLog` + gobernanza de cambios sensibles cumple los cuatro pilares (diseño, implementación, evidencia, documentación) y se considera **auditado y cerrado**.
- Otros bloques (Alembic, permisos 403, flujo principal de evaluación, etc.) están **parciales** y listados en el `backlog.md` como historias de evolución y deuda técnica (`[v0.2-008]` y siguientes).

Este documento existe para dar una visión rápida del estado global de auditoría técnica y evitar que la percepción del trabajo pendiente se convierta en ruido o sensación de "montaña infinita".

## 4. Estado global por módulo (snapshot)

| Módulo / área                                                         | Diseño (ADR)                    | Implementación                    | Evidencia (tests)                | Documentación                  | Estado      | Notas principales                                                                                                         |
| --------------------------------------------------------------------- | ------------------------------- | --------------------------------- | -------------------------------- | ------------------------------ | ----------- | ------------------------------------------------------------------------------------------------------------------------- |
| Feed-forward (estado_feed_forward)                                    | ✅ D-026/D-035                   | ✅ main                            | ✅ tests nuevos                   | ✅ README + backlog al día      | Auditado    | Flujo de estados y endpoints cerrados, sin deuda crítica.                                                                 |
| ChangeLog + audit_metadata                                            | ✅ D-002/D-035                   | ✅ main                            | ✅ tests nuevos                   | ✅ README + backlog al día      | Auditado    | Separación diff/ctx clara; actor humano, IA en metadatos.                                                                 |
| Gobernanza de cambios sensibles                                       | ✅ D-035                         | ✅ AGENTS Regla 6                  | N/A (norma)                      | ✅ glosario + docs              | Auditado    | Política de 4 pilares aplicada como norma general.                                                                        |
| Permisos 403 en feed-forward                                          | ✅ [v0.2-008]                    | ✅ main                            | ✅ test_feed_forward_unauthorized | ✅ README al día                | Auditado    | Cubre transiciones a realizado/verificado.                                                                                |
| Flujo principal de evaluación (HitL, REVIEW/GRADED)                   | ✅ D-002/D-024                   | ✅ main                            | ✅ tests en verde                 | ✅ README + backlog al día      | Auditado    | PATCH /approve con logs en ChangeLog, aislamiento 403, listados filtrados.                                                |
| Normativa LOMLOE etapa/escala (D-040 a D-046)                         | ✅ D-041/D-042/D-043/D-045/D-046 | ✅ main (issue 10, PR 11)          | ✅ tests en verde                 | ✅ backlog actualizado 20/07    | Auditado    | Media ponderada determinista en backend; escala BE corregida; migración default BACH pendiente de revisión manual en ESO. |
| Calificación cualitativa condicional (ESO vs BACH)                    | ✅ D-049                         | ✅ main ([v0.2-011])               | ✅ tests en verde                 | ✅ README + backlog al día      | 🟢 Auditado | Validador fuerza null en BACH y preserva enum oficial en ESO.                                                             |
| Asincronía MVP (BackgroundTasks, Celery diferido)                     | ✅ D-048                         | ✅ main (v0.4)                     | ✅ prueba de carga 5 exámenes     | ✅ backlog corregido (v0.4-002) | Auditado    | Resuelve inconsistencia previa entre v0.4-002 y v0.4-004.                                                                 |
| Alembic (migraciones reales)                                          | ✅ ADR/backlog                   | ✅ migración 326ff2789e2e aplicada | ⚠ evidencia indirecta            | ✅ backlog al día               | Parcial     | Tests usan SQLite + metadata.create_all(), no validan contra Postgres real. Riesgo de falso "verde".                      |
| Modo Dual de evaluación (RÚBRICA PURA/COMBINADO/AUDITORÍA_CURRICULAR) | ✅ D-027                         | ✅ main (v0.2-006)                 | ⚠ tests parciales                | ✅ backlog al día               | Parcial     | Falta test que cubra rechazo de contradicción etapa↔marco (400).                                                          |
| Autenticación y roles (profesor/alumno, JWT)                          | ⚠ parcial                       | ⚠ parcial                         | ⚠ tests de permiso incompletos   | ⚠ evolución futura señalada    | Parcial     | Falta auditoría completa de auth; extensión a alumno planificada en v0.5-006.                                             |
| Trazabilidad extremo a extremo (cambio↔ticket↔ADR↔test)               | ⚠ conceptual (D-035)            | ⚠ parcial                         | ⚠ enlaces PR sin revisar         | ⚠ AUDITORIA.md reciente        | Parcial     | Marco definido, falta recorrido completo de un caso end-to-end.                                                           |
| Motor multimodal (Groq Vision + fallback GPT-4o)                      | ✅ D-047                         | ❌ pendiente (v0.3)                | ❌ no aplica aún                  | ✅ backlog v0.3-004             | No iniciado | Decisión formalizada por adelantado; implementación bloqueada hasta iniciar v0.3.                                         |
| Evidencias para auditoría externa (AI Act/AESIA)                      | ❌ no definida                   | ⚠ logs básicos                    | ❌ sin ensayos formales           | ⚠ docs centradas en lo técnico | No iniciado | Requiere checklist específico si se busca auditoría externa formal.                                                       |