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
| Motor multimodal (OpenAI Vision + Workload Routing)                   | ✅ D-051 / D-052                 | ✅ main (v0.3-004)                 | ✅ smoke_test_vision.py verde     | ✅ README + decisiones.md        | 🟢 Auditado | Pipeline validado el 12/08/2026. Workload Routing: Visión→OpenAI (Structured Outputs), Texto→Groq. Cualitativa ESO determinista en backend. |
| Recorte de cabecera PII y Censura manual (Client-Side Redaction)      | ✅ D-022 / D-034                 | ✅ `CameraCapture.jsx` (`[v0.5-002]`) | ✅ `CameraCapture.test.jsx` verde | ✅ backlog actualizado         | 🟢 Auditado | Implementada cámara nativa y subida local. Censura vía Canvas API validada manualmente y con Vitest. Zero Data Retention asegurado en PWA. |
| Scaffold Frontend React + Vite + PWA (`[v0.5-001]`)                  | ✅ D-058 / D-007 / D-008         | ✅ rama v0.5-frontend-pwa         | ✅ `app.test.jsx` en verde       | ✅ backlog `[v0.5-001]` cerrado | 🟢 Auditado | HTTPS local con `@vitejs/plugin-basic-ssl`. Service Worker generado. Verificado en PC y móvil. Vitest configurado. |
| Sistema de diseño UI (Glassmorphism + tokens CSS)                     | ✅ D-059                         | ✅ `frontend/src/index.css`       | ❌ sin tests visuales/WCAG       | ✅ glosario + D-059             | Parcial     | Variables CSS centralizadas. Contraste WCAG AA pendiente de verificación antes de despliegue público. |
| Evidencias para auditoría externa (AI Act/Auditoría)                      | ❌ no definida                   | ⚠ logs básicos                    | ❌ sin ensayos formales           | ⚠ docs centradas en lo técnico | No iniciado | Requiere checklist específico si se busca auditoría externa formal.                                                       |

---

## 5. Corrección de rumbo pre-code-freeze (24/07/2026)

**Evento:** Al diseñar la historia `[v0.3-001]` de la Épica v0.3 (Issue #14), el agente propuso inicialmente mover la función `recortar_folio` a `backend/services/image_service.py` como servicio Python. Esta propuesta contradecía los ADRs **D-022** y **D-034** ya adoptados, que establecen que el recorte de cabecera ocurre **exclusivamente en el cliente** (PWA/Canvas), nunca en el backend.

**Causa raíz:** El script `scratch/pillow_crop_test.py` fue creado como prueba de concepto del *algoritmo* de recorte (ratio 0.20, división 794×1123 → 224+899 px) para validar la matemática antes de portarla a JavaScript. Su naturaleza exploratoria fue malinterpretada como punto de partida para un servicio de backend.

**Correcciones aplicadas (pre-code-freeze, solo documentación):**
- Issue #14 en GitHub: historia `[v0.3-001]` reescrita — función `cropHeader()` en `frontend/src/utils/imageCrop.js` (JavaScript), tests en Vitest/Jest con 5 casos de aceptación.
- `AUDITORIA.md`: nueva fila para el módulo de recorte con estado "No iniciado" y stack correcto (cliente, no backend).
- `Pillow>=10.3.0` en `requirements.txt`: se mantiene provisionalmente (puede ser necesaria en `v0.3-002` para optimizar imágenes antes de enviarlas a Groq Vision), pero **no** para el recorte de cabecera. Decisión definitiva sobre mantener/retirar Pillow aplazada a la planificación técnica de `v0.3-002` (post-revisión técnica, lunes 28/07 en adelante).
- `scratch/pillow_crop_test.py` permanece intacto como evidencia histórica del PoC del algoritmo (ignorado por git).

**Invariante reafirmada (D-022 + D-031 + D-034):** El nombre del alumno **jamás alcanza el servidor Python**, en ninguna versión del producto. La seudonimización es client-side y Zero Data Retention absoluto.