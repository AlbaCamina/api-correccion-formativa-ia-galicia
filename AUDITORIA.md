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

| Módulo / área | Diseño (ADR) | Implementación | Evidencia (tests) | Documentación (`README`/`backlog`) | Estado | Notas principales |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Feed-forward (`estado_feed_forward`) | ✅ D-026/D-035 | ✅ `main` | ✅ tests nuevos | ✅ README + backlog al día | Auditado | Flujo de estados y endpoints cerrados, sin deuda crítica. |
| `ChangeLog` + `audit_metadata` | ✅ D-002/D-035 | ✅ `main` | ✅ tests nuevos | ✅ README + backlog al día | Auditado | Separación diff/ctx clara; actor humano, IA en metadatos. |
| Gobernanza de cambios sensibles | ✅ D-035 | ✅ AGENTS Regla 6 | N/A (norma) | ✅ glosario + docs | Auditado | Política de 4 pilares aplicada como norma general. |
| Alembic (migraciones reales) | ✅ mencionada en ADR/backlog | ✅ `main` | ✅ tests en verde | ✅ backlog al día | Auditado | Migración 326ff2789e2e generada, validada, integrada y aplicada localmente sin incidencias. |
| Permisos 403 en feed-forward | ✅ previsto en backlog (`[v0.2-008]`) | ✅ `main` | ✅ test_feed_forward_unauthorized | ✅ README al día | Auditado | Implementado test_feed_forward_unauthorized para transiciones a realizado/verificado. |
| Flujo principal de evaluación (`evaluation_router`, REVIEW/GRADED, HitL) | ✅ D-002/D-024 | ✅ `main` | ✅ tests en verde | ✅ README + backlog al día | Auditado | Implementado ciclo HitL PATCH /approve con logs en ChangeLog, aislamiento 403 en GET /evaluaciones y listados GET /submissions filtrados, con tests automáticos en verde. |
| Autenticación y roles (profesor/alumno, JWT) | ⚠ parcial | ⚠ parcial | ⚠ tests de permiso no completos | ⚠ README/backlog señalan evolución futura | Parcial | Hoy se ha planificado evolución para alumno en feed-forward, falta auditoría completa de auth. |
| Trazabilidad extremo a extremo (cambio ↔ ticket ↔ ADR ↔ test) | ⚠ conceptual (D-035) | ⚠ parcial | ⚠ pendiente revisar enlaces en varios PR | ⚠ AUDITORIA.md recién creado | Parcial | Marco definido, pero aún no se ha hecho un recorrido completo sobre un caso de extremo a extremo. |
| Evidencias para auditoría externa (AI Act / AESIA, ensayos, logs operativos) | ❌ no definida | ⚠ parcial (logs básicos) | ❌ sin ensayos formales | ⚠ docs centradas en parte técnica | No iniciado | Si se busca auditoría formal externa, hará falta checklist específico y evidencias adicionales. |
