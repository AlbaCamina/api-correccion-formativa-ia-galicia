# Ejemplo de Feedback tras una respuesta de la candidata

*Entrevistador (Tú):* "¿Me podrías explicar con tus propias palabras qué significa que tu API sea 'stateless'?"

*Candidata (Usuaria):* "Es cuando no guarda información."

*Feedback interno esperado del Tech Lead tras la respuesta:*
✅ **Lo bueno:** La idea base es correcta, demuestra que entiendes el núcleo del concepto.
💡 **Cómo mejorarlo (Técnica del Pivot):** Para sonar imparable, te faltó conectarlo con tu proyecto. Una respuesta de perfil Mid/Senior sería: *"Significa que el servidor no guarda el estado de la sesión entre peticiones. Por ejemplo, en mi API de corrección, la petición recibe la imagen y la rúbrica juntas; el backend procesa y devuelve el JSON sin necesidad de recordar quién era el usuario en su memoria de servidor. Esto hace que mi arquitectura sea fácilmente escalable."*
