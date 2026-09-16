import { useRef, useState, useEffect } from 'react';
import { cropHeader } from '../utils/imageCrop';
import ResultsPanel from './ResultsPanel';

const CameraCapture = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [stream, setStream] = useState(null);
  const [imageCaptured, setImageCaptured] = useState(false);
  const [isDrawing, setIsDrawing] = useState(false);
  const [lastPos, setLastPos] = useState({ x: 0, y: 0 });
  const [censorshipMode, setCensorshipMode] = useState(false);
  const [etapa, setEtapa] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submissionResult, setSubmissionResult] = useState(null);
  const originalImageRef = useRef(null); // MVP: Guarda la foto intacta para poder deshacer

  // Libera el stream anterior al cambiarlo y el activo al desmontar el componente.
  useEffect(() => {
    return () => {
      stream?.getTracks().forEach((track) => track.stop());
    };
  }, [stream]);

  // Inyectar el stream en el video cuando React haya montado el <video>
  useEffect(() => {
    if (stream && videoRef.current && !videoRef.current.srcObject) {
      videoRef.current.srcObject = stream;
    }
  }, [stream]);

  const startCamera = async () => {
    try {
      let mediaStream;
      try {
        // Intenta usar la cámara trasera (ideal para móviles)
        mediaStream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: { ideal: "environment" } }
        });
      } catch {
        // Fallback: si es un portátil sin cámara trasera, coge la webcam estándar
        mediaStream = await navigator.mediaDevices.getUserMedia({
          video: true
        });
      }
      setStream(mediaStream);
      setImageCaptured(false);
    } catch (err) {
      console.error("Error al acceder a la cámara:", err);
      alert("No se pudo acceder a la cámara. Revisa los permisos.");
    }
  };

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
  };

  const captureFrame = () => {
    if (!videoRef.current || !canvasRef.current) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;

    // Ajustar dimensiones del canvas al video real
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Guardar copia de seguridad intacta para restaurar (MVP Undo)
    originalImageRef.current = canvas.toDataURL('image/jpeg', 1.0);

    stopCamera();
    setImageCaptured(true);
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const img = new Image();
    img.onload = () => {
      const canvas = canvasRef.current;
      // Compresión básica / Límite de tamaño (2048px máx)
      const MAX_SIZE = 2048;
      let width = img.width;
      let height = img.height;

      if (width > height && width > MAX_SIZE) {
        height *= MAX_SIZE / width;
        width = MAX_SIZE;
      } else if (height > MAX_SIZE) {
        width *= MAX_SIZE / height;
        height = MAX_SIZE;
      }

      canvas.width = width;
      canvas.height = height;

      const ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0, width, height);

      // Guardar copia de seguridad intacta para restaurar (MVP Undo)
      originalImageRef.current = canvas.toDataURL('image/jpeg', 1.0);

      stopCamera();
      setImageCaptured(true);
    };
    img.src = URL.createObjectURL(file);
  };

  const resetCapture = () => {
    setImageCaptured(false);
    setCensorshipMode(false);
    setSubmissionResult(null);
    setIsSubmitting(false);
    const canvas = canvasRef.current;
    if (canvas) {
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
  };

  // --- LÓGICA DE HERRAMIENTA DE CENSURA (CANVAS API) ---
  const getCoordinates = (e) => {
    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;

    let clientX = e.clientX;
    let clientY = e.clientY;

    if (e.touches && e.touches.length > 0) {
      clientX = e.touches[0].clientX;
      clientY = e.touches[0].clientY;
    }

    return {
      x: (clientX - rect.left) * scaleX,
      y: (clientY - rect.top) * scaleY
    };
  };

  const startDrawing = (e) => {
    if (!imageCaptured || !censorshipMode) return;
    e.preventDefault();
    setIsDrawing(true);
    setLastPos(getCoordinates(e));
  };

  const draw = (e) => {
    if (!isDrawing || !imageCaptured || !censorshipMode) return;
    e.preventDefault();

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const currentPos = getCoordinates(e);

    // Dibujar trazo grueso negro
    ctx.beginPath();
    ctx.moveTo(lastPos.x, lastPos.y);
    ctx.lineTo(currentPos.x, currentPos.y);
    ctx.strokeStyle = '#000000';
    ctx.lineWidth = 40; // Grosor del "rotulador" censor
    ctx.lineCap = 'round';
    ctx.stroke();

    setLastPos(currentPos);
  };

  const stopDrawing = () => {
    setIsDrawing(false);
  };

  const handleAutoCrop = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    try {
      const croppedCanvas = cropHeader(canvas, canvas.width, canvas.height, 0.20);

      // Actualizamos las dimensiones del lienzo original para reflejar el recorte
      canvas.width = croppedCanvas.width;
      canvas.height = croppedCanvas.height;

      const ctx = canvas.getContext('2d');
      // Dibujamos el resultado sobre el lienzo que ve el usuario
      ctx.drawImage(croppedCanvas, 0, 0);
    } catch (err) {
      console.error("Error recortando cabecera:", err);
      alert("Error al recortar la imagen.");
    }
  };

  const handleRestoreOriginal = () => {
    if (!originalImageRef.current || !canvasRef.current) return;

    const img = new Image();
    img.onload = () => {
      const canvas = canvasRef.current;
      canvas.width = img.width;
      canvas.height = img.height;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0);
    };
    img.src = originalImageRef.current;
  };

  const handleSubmit = async () => {
    if (!etapa) {
      alert("⚠️ Debes seleccionar una etapa educativa (ESO o BACH) antes de enviar.");
      return;
    }

    const canvas = canvasRef.current;
    if (!canvas) return;

    setIsSubmitting(true);

    try {
      // Extraer imagen censurada como Blob (Zero Data Retention)
      const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/jpeg', 0.8));

      const formData = new FormData();
      // Simulamos que file[] es soportado o mandamos un único archivo por ahora
      formData.append('file', blob, 'examen_capturado.jpg');
      formData.append('etapa', etapa);
      formData.append('rubrica_id', 1); // Mock: En producción vendría del contexto/login
      formData.append('modo_evaluacion', 'COMBINADO');

      const response = await fetch('http://localhost:8000/api/v1/submissions/upload-and-evaluate', {
        method: 'POST',
        body: formData,
        // Nota: en un entorno real incluiríamos headers de Auth:
        // headers: { 'Authorization': 'Bearer ' + token }
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.detail || 'Error en la subida al servidor');
      }

      const data = await response.json();
      console.log("🚀 Respuesta del backend:", data);

      setSubmissionResult({
        success: true,
        data: data
      });

    } catch (err) {
      console.error("Error subiendo el archivo:", err);
      setSubmissionResult({
        success: false,
        error: err.message
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  if (submissionResult) {
    if (submissionResult.success) {
      return (
        <ResultsPanel
          submissionId={submissionResult.data.submission_id}
          onReset={resetCapture}
        />
      );
    }

    return (
      <div className="glass-panel" style={{ textAlign: 'center', animation: 'fadeIn 0.5s ease' }}>
        <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>❌</div>
        <h2 style={{ color: 'var(--color-danger)' }}>Error en el Envío</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
          {submissionResult.error}
        </p>
        <button
          onClick={() => setSubmissionResult(null)}
          style={{ background: '#555', color: 'white', padding: '1rem 2rem', fontSize: '1.1rem', borderRadius: '8px', cursor: 'pointer', border: 'none' }}
        >
          Reintentar Envío
        </button>
      </div>
    );
  }

  return (
    <div className="camera-container" style={{ display: 'flex', flexDirection: 'column', gap: '1rem', alignItems: 'center' }}>
      <h2>Captura de Examen</h2>

      {!imageCaptured && (
        <div className="action-buttons" style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', justifyContent: 'center' }}>
          <button onClick={startCamera}>📸 Abrir Cámara</button>

          <label style={{ cursor: 'pointer', padding: '0.5rem 1rem', background: '#333', color: 'white', borderRadius: '4px' }}>
            📁 Subir Archivo
            <input
              type="file"
              accept="image/*"
              onChange={handleFileUpload}
              style={{ display: 'none' }}
            />
          </label>
        </div>
      )}

      {/* Contenedor del Video en Vivo */}
      {!imageCaptured && stream && (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1rem' }}>
          <video
            ref={videoRef}
            autoPlay
            playsInline
            muted
            style={{ maxWidth: '100%', maxHeight: '60vh', border: '1px solid #444', borderRadius: '8px' }}
          />
          <button onClick={captureFrame} style={{ background: 'var(--color-danger)', color: 'white', padding: '1rem 2rem', fontSize: '1.2rem', borderRadius: '50px' }}>
            Capturar Foto
          </button>
        </div>
      )}

      {/* Contenedor del Canvas (Imagen Capturada) */}
      <div className="canvas-wrapper" style={{ display: imageCaptured ? 'flex' : 'none', flexDirection: 'column', alignItems: 'center', gap: '1rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', background: '#222', padding: '0.3rem 0.8rem', borderRadius: '8px' }}>
          <span style={{ fontSize: '0.8rem', color: '#ccc' }}>Tachón Manual:</span>
          <button
            onClick={() => setCensorshipMode(!censorshipMode)}
            style={{
              background: censorshipMode ? 'var(--color-danger)' : '#444',
              color: 'white',
              padding: '0.3rem 0.6rem',
              fontSize: '0.8rem',
              border: 'none',
              borderRadius: '4px',
              fontWeight: 'bold'
            }}
          >
            {censorshipMode ? 'ON' : 'OFF'}
          </button>
        </div>

        {censorshipMode && (
          <p style={{ color: 'var(--color-warning)', fontSize: '0.85rem' }}>
            Aviso: pasa el dedo o el raton por encima para censurar el nombre.
          </p>
        )}

        <canvas
          ref={canvasRef}
          onMouseDown={startDrawing}
          onMouseMove={draw}
          onMouseUp={stopDrawing}
          onMouseOut={stopDrawing}
          onTouchStart={startDrawing}
          onTouchMove={draw}
          onTouchEnd={stopDrawing}
          style={{
            maxWidth: '100%',
            border: censorshipMode ? '2px solid var(--color-danger)' : '2px solid var(--accent-primary)',
            cursor: censorshipMode ? 'crosshair' : 'default',
            touchAction: censorshipMode ? 'none' : 'auto'
          }}
        />

        <div className="action-buttons" style={{ display: 'flex', gap: '0.8rem', flexWrap: 'wrap', justifyContent: 'center', width: '100%', padding: '1rem 0' }}>
          <div style={{ display: 'flex', flex: '1 1 100%', gap: '1rem', alignItems: 'center', background: 'rgba(255,255,255,0.05)', padding: '1rem', borderRadius: '8px', marginBottom: '1rem', border: '1px solid rgba(255,255,255,0.1)' }}>
            <label style={{ fontWeight: 'bold', color: 'var(--text-primary)' }}>Etapa Educativa (Obligatorio):</label>
            <select
              value={etapa}
              onChange={(e) => setEtapa(e.target.value)}
              style={{ flex: 1, padding: '0.8rem', borderRadius: '4px', background: '#333', color: 'white', border: '1px solid #555', fontSize: '1rem' }}
            >
              <option value="">-- Selecciona --</option>
              <option value="ESO">Educación Secundaria Obligatoria (ESO)</option>
              <option value="BACH">Bachillerato (BACH)</option>
            </select>
          </div>

          <button onClick={handleRestoreOriginal} disabled={isSubmitting} style={{ background: '#f59e0b', color: 'black', padding: '1rem', fontSize: '1rem', borderRadius: '8px', flex: '1 1 40%', border: 'none', opacity: isSubmitting ? 0.5 : 1 }}>🔄 Restaurar</button>
          <button onClick={handleAutoCrop} disabled={isSubmitting} style={{ background: '#3b82f6', color: 'white', padding: '1rem', fontSize: '1rem', borderRadius: '8px', flex: '1 1 40%', border: 'none', opacity: isSubmitting ? 0.5 : 1 }}>✂️ Recorte Cabecera</button>
          <button onClick={resetCapture} disabled={isSubmitting} style={{ background: '#555', color: 'white', padding: '1rem', fontSize: '1rem', borderRadius: '8px', flex: '1 1 40%', border: 'none', opacity: isSubmitting ? 0.5 : 1 }}>❌ Descartar</button>
          <button
            onClick={handleSubmit}
            disabled={isSubmitting}
            style={{
              background: 'var(--color-success)',
              color: 'black',
              fontWeight: 'bold',
              padding: '1.2rem',
              fontSize: '1.2rem',
              borderRadius: '8px',
              flex: '1 1 100%',
              border: 'none',
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              gap: '0.5rem',
              cursor: isSubmitting ? 'not-allowed' : 'pointer',
              opacity: isSubmitting ? 0.8 : 1
            }}
          >
            {isSubmitting ? (
              <>
                <span className="spinner"></span> Procesando y Subiendo...
              </>
            ) : (
              '✅ Confirmar y enviar'
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default CameraCapture;
