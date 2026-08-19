# Ejemplo de Post Base (Tono Esperado)

*Este es el estándar de calidad y tono que debes imitar al redactar.*

### 📢 POST Base — Pesadilla en Producción

Estás construyendo una API, todo funciona perfecto en local, te vas a dormir y al día siguiente... tu proveedor de Inteligencia Artificial te avisa de que apaga el modelo que usas. 💥

Esta semana me ha pasado no una, sino **dos veces** con la API de corrección formativa.

Primero, el modelo de visión que usaba en Groq fue sustituido. Intenté adaptarme usando *Workload Routing*. Pero ayer llegó el golpe final: correo oficial avisando de que el modelo de texto principal (`llama-3.3-70b`) también se apaga en 48 horas.

¿La lección? **Nunca acoples tu código a un proveedor de IA.**

He tenido que aplicar un protocolo de *Pausa Arquitectónica* urgente (mi ADR D-053) para pivotar toda la estrategia:
1️⃣ He unificado todo el motor LLM (texto y visión) en **OpenAI (`gpt-4o-mini`)**.
2️⃣ Como diseñé el cliente LLM (`llm_client.py`) con una capa de abstracción desde el principio, hacer esta migración total solo me ha costado cambiar dos variables en un archivo `.env` y borrar un SDK. 

Depender de APIs de terceros requiere arquitecturas resilientes. Si tu proveedor falla o cambia las reglas, tu código tiene que poder cambiar de cerebro en 5 minutos. 🧠🔌

¿Os ha pasado algo parecido con la inestabilidad de los modelos últimamente?

#SoftwareEngineering #AI #BackendDeveloper #FastAPI #OpenAI #TechDebt
