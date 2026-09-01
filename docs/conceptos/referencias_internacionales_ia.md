# 📚 Referencias Internacionales y Normativa de Estudio sobre IA

**Proyecto:** API de Corrección Formativa con IA (`api-correccion-formativa-ia-galicia`)  
**Propósito:** Este documento recopila las referencias oficiales, textos legales internacionales y guías de estudio técnico relativas a la implementación y gobernanza de la Inteligencia Artificial en sistemas de alto riesgo y al cumplimiento de la privacidad desde el diseño.

---

## 1. Gobernanza de Inteligencia Artificial (Unión Europea)

*   **Texto Oficial de la Ley Europea de IA (EU AI Act):**
    *   **Referencia Formal:** *Regulation (EU) 2024/1689 of the European Parliament and of the Council of 13 June 2024 laying down harmonised rules on artificial intelligence and amending Regulations (EC) No 300/2008, (EU) No 167/2013, (EU) No 168/2013, (EU) 2018/858, (EU) 2018/1139 and (EU) 2019/2144 and Directives 2014/90/EU, (EU) 2016/797 and (EU) 2020/1828 (Artificial Intelligence Act) (Text with EEA relevance).*
    *   **Código de Documento:** `PE/24/2024/REV/1`
    *   **Contexto en el Proyecto:** Este texto fundamenta la catalogación de la API como "Sistema de Alto Riesgo" (Anexo III, relativo a educación y formación profesional). De aquí derivan las reglas inquebrantables de la arquitectura: la obligatoriedad de la supervisión humana (*Human-in-the-Loop*, Art. 14), el registro de logs/trazabilidad (*ChangeLog*, Art. 12) y las obligaciones de transparencia algorítmica (Art. 50).

## 2. Privacidad y Protección de Datos (RGPD)

*   **EDPB Guidelines on Data Protection by Design and by Default:**
    *   **Enlace de Estudio:** [EDPB Guidelines 4/2019 (PDF)](https://www.edpb.europa.eu/system/files_en?file=consultation/edpb_guidelines_201904_dataprotection_by_design_and_by_default.pdf)
    *   **Organismo:** *European Data Protection Board* (Comité Europeo de Protección de Datos).
    *   **Contexto en el Proyecto:** Estas directrices son la "biblia" técnica para la exigencia del Artículo 25 del RGPD (Privacidad por Diseño y por Defecto). Justifican académica y legalmente implementaciones de tu arquitectura como la anonimización y recorte fotográfico local en la PWA (Cámara de Exclusión Pre-Nube) antes de la subida, así como las directrices de *Zero Data Retention* con los proveedores de LLM.

## 3. Manuales y Buenas Prácticas Internacionales (Educación y Gobernanza)

Además de la normativa de obligado cumplimiento, estas directrices internacionales son el estándar de la industria ("Good Practices") para auditar y diseñar sistemas éticos:

*   **UNESCO: Guidance for Generative AI in Education and Research (2023)**
    *   **Enlace de Estudio:** [UNESCO Digital Library - GenAI Guidance](https://unesdoc.unesco.org/ark:/48223/pf0000386693)
    *   **Contexto en el Proyecto:** Es el primer manual global sobre IA generativa en educación. Respalda directamente tu decisión arquitectónica de mantener la *Agencia Humana* (el profesor toma la decisión final) y tus medidas estrictas de privacidad y protección de datos para menores, que la UNESCO marca como prioridad número uno. También complementa la guía anterior *"AI and Education: Guidance for Policy-makers (2021)"*.

*   **NIST: AI Risk Management Framework (AI RMF 1.0 - 2023)**
    *   **Enlace de Estudio:** [NIST AI RMF 1.0 (PDF)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf)
    *   **Organismo:** *National Institute of Standards and Technology* (Gobierno de EE. UU.)
    *   **Contexto en el Proyecto:** Es el marco de gestión de riesgos voluntario más respetado a nivel mundial. Tus implementaciones de auditoría (el uso del archivo `AUDITORIA.md` y la matriz de trazabilidad `ChangeLog`) encajan perfectamente dentro de sus funciones *Govern* (establecer procesos de responsabilidad) y *Measure/Manage* (evaluar y mitigar riesgos en sistemas complejos).

*   **OECD: Recomendaciones del Consejo sobre Inteligencia Artificial (OECD AI Principles - 2024 Update)**
    *   **Enlace de Estudio:** [OECD AI Principles & Observatory](https://oecd.ai/en/ai-principles)
    *   **Organismo:** *Organización para la Cooperación y el Desarrollo Económicos*
    *   **Contexto en el Proyecto:** El primer estándar intergubernamental. Los principios de la OCDE dictan que los sistemas de IA deben ser robustos, transparentes y contar con *Accountability* (rendición de cuentas). El hecho de que tu motor LLM justifique sus notas con un `confidence_score` y un desglose criterial estructurado en JSON se alinea directamente con su principio de "Transparencia y Explicabilidad".

---
*Nota: Este documento es un "Living Document" orientado al estudio y consulta. Puedes ir añadiendo aquí futuros enlaces a directrices, papers de IEEE u otras resoluciones de las agencias de protección de datos que cimienten las decisiones arquitectónicas del proyecto.*
