# 🎯 Demo Técnica (Colega): API de Corrección Formativa con IA - Galicia

> **Misión:** Desarrollo de un Copiloto Formativo para docentes, diseñado bajo los principios de *Zero Data Retention* (AI Act) y alineado estrictamente con la normativa autonómica LOMLOE.

---

## 1. Stack Tecnológico y Evolución Arquitectónica

El proyecto huye del concepto "chatbot generalista" para convertirse en una API transaccional, profesional y auditable (ver [AUDITORIA.md](./AUDITORIA.md)).

*   **Backend Actual (v0.2):** Python + FastAPI.
*   **Base de Datos (Evolución):**
    *   *v0.0 (Prototipo):* Memoria RAM volátil.
    *   *v0.2 (Actual MVP):* **PostgreSQL (Docker)**. Arquitectura *Stateful* para garantizar trazabilidad (registrado en [decisiones.md](./decisiones.md)).
*   **Frontend (Roadmap v0.3):** PWA (React) con arquitectura *Client-Side First*. Todo el pre-procesamiento de imágenes y OCR se delegará al navegador del docente para no enviar fotografías íntegras de exámenes de menores al servidor.

---

## 2. Tecnologías de IA Implementadas

El core de evaluación no depende de la lectura de texto libre por la IA, sino de un **Contrato JSON Estricto** (ADR [D-024 en decisiones.md](./decisiones.md)).

*   **Proveedor y Hardware:** Groq (`llama-3.3-70b-versatile`).
*   **Inferencia mediante LPUs:** Descartamos el uso de GPUs tradicionales para generación secuencial de texto en favor de **LPUs (Language Processing Units)**. Esto nos proporciona velocidades de inferencia superiores a 800 tokens/segundo, logrando la latencia mínima necesaria para corrección en tiempo real.
*   **JSON Mode Predictivo:** La IA está capada estructuralmente; solo puede devolver cálculos y metadatos anclados a la rúbrica del docente, evitando alucinaciones o respuestas literarias.

---

## 3. Cumplimiento Normativo (Dual)

El sistema ha sido diseñado desde el inicio para satisfacer simultáneamente dos legislaciones estrictas:

1.  **AI Act (Europa) - Privacidad:**
    *   Arquitectura sin estado para los datos sensibles (Zero Data Retention).
    *   *Duda Abierta 1 (S3):* Para escalado multimodal, proponemos Object Storage (Supabase/AWS) con URLs prefirmadas de 2 minutos. ¿Es el estándar más robusto para pasar auditorías?
    *   *Duda Abierta 2 (Frontend):* Planteamos que el recorte de cabeceras de exámenes con datos de menores se haga en local vía Canvas (Navegador) para que esa imagen nunca viaje al servidor. ¿Os parece un blindaje suficiente?
    *   *Duda Abierta 3 (Asincronía):* Actualmente usamos `BackgroundTasks`. Para producción, ¿recomiendas dar el salto a `Celery+Redis` o es *over-engineering* para llamadas a la API de Groq?
2.  **LOMLOE (Decretos 156/157 2022 - Galicia):**
    *   El motor no hace promedios aritméticos libres, califica bajo Competencias Clave y Criterios de Evaluación obligatorios.
    *   Devuelve los niveles de logro cualitativos oficiales (IN, SU, BE, NT, SB) para la ESO.

---

## 4. Gobernanza y Human-in-the-Loop (HitL) (ver [backlog.md](./backlog.md))

Demostración técnica en **Swagger UI**:

1.  **Autenticación JWT:** Seguridad y control de acceso (Endpoint `/auth/login`).
2.  **Evaluación Restringida:** Endpoint `/evaluate`. El motor genera el cálculo y los comentarios, pero el estado de la entrega nace como `PENDIENTE` (estado interno `REVIEW`).
3.  **Firma Docente:** Endpoint `PATCH /approve`. El sistema rechaza cualquier validez oficial de la nota hasta que el humano revisa la propuesta de la IA y transiciona el estado a `GRADED`.

---

## 5. Calidad y Cobertura de Código

El backend no es solo funcional, sino que cuenta con un arnés de seguridad automatizado:
*   **Suite de Pruebas:** Ejecución de 31 tests unitarios y de integración mediante `pytest`.
*   **Blindaje:** Garantizan que las reglas de negocio (escalas LOMLOE, privacidad, estados de bloqueo del HitL) no se rompan ante futuras refactorizaciones o actualizaciones de dependencias.

> **Comando de ejecución (WSL):**
> ```bash
> source venv/bin/activate
> pytest backend/tests/ -v
> ```

---
*Documento vivo — Generado para la revisión técnica (27/07/2026).*

