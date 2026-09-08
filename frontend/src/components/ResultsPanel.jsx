import { useState, useEffect } from 'react';
import '../index.css';

const getList = (value) => (Array.isArray(value) ? value : []);

const ResultsPanel = ({ submissionId, onReset }) => {
  const [evaluacion, setEvaluacion] = useState(null);
  const [error, setError] = useState(null);
  const [isPolling, setIsPolling] = useState(true);

  useEffect(() => {
    let intervalId;
    let isActive = true;

    const stopPolling = () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    };

    const pollResult = async () => {
      try {
        const res = await fetch(`http://localhost:8000/api/v1/evaluaciones/${submissionId}`);
        if (res.ok) {
          const data = await res.json();

          if (isActive) {
            setEvaluacion(data);
            setIsPolling(false);
          }

          stopPolling();
        } else if (res.status !== 404) {
          const errorData = await res.json().catch(() => ({}));
          throw new Error(errorData.detail || 'Error al obtener la evaluación');
        }
      } catch (err) {
        if (isActive) {
          setError(err.message || 'No se pudo conectar con el servidor de evaluación.');
          setIsPolling(false);
        }

        stopPolling();
      }
    };

    pollResult();
    intervalId = setInterval(pollResult, 3000);

    return () => {
      isActive = false;
      stopPolling();
    };
  }, [submissionId]);

  if (isPolling) {
    return (
      <div className="glass-panel" style={{ textAlign: 'center', animation: 'fadeIn 0.5s ease', padding: '3rem' }}>
        <div className="spinner" style={{ width: '40px', height: '40px', borderWidth: '4px', marginBottom: '1.5rem' }}></div>
        <h2 style={{ background: 'linear-gradient(to right, #a5b4fc, #6366f1)', WebkitBackgroundClip: 'text', color: 'transparent' }}>
          Analizando con IA...
        </h2>
        <p style={{ color: 'var(--text-secondary)' }}>El motor multimodal está leyendo y evaluando el examen en segundo plano.</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="glass-panel" style={{ textAlign: 'center' }}>
        <h2 style={{ color: 'var(--color-danger)' }}>Error al obtener resultados</h2>
        <p>{error}</p>
        <button onClick={onReset} style={{ marginTop: '1rem', background: '#444', color: '#fff', border: 'none', padding: '0.8rem 1.5rem', borderRadius: '8px' }}>Volver a capturar</button>
      </div>
    );
  }

  if (!evaluacion || !evaluacion.resultado_ia) {
    return (
      <div className="glass-panel" style={{ textAlign: 'center' }}>
        <h2 style={{ color: 'var(--color-danger)' }}>Resultado no disponible</h2>
        <p>La evaluación recibida no contiene un resultado válido.</p>
        <button onClick={onReset} style={{ marginTop: '1rem', background: '#444', color: '#fff', border: 'none', padding: '0.8rem 1.5rem', borderRadius: '8px' }}>Volver a capturar</button>
      </div>
    );
  }

  const { resultado_ia } = evaluacion;
  const analysis = resultado_ia.qualitativeAnalysis || {};
  const improvementNeeds = analysis.improvementNeeds || {};
  const strengths = getList(analysis.strengths);
  const immediateImprovements = getList(improvementNeeds.immediate);
  const mediumLongTermImprovements = getList(improvementNeeds.mediumLongTerm);
  const rubricBreakdown = getList(resultado_ia.rubricBreakdown);
  const visualMarkers = getList(resultado_ia.visualMarkers);
  const confidence = Number(resultado_ia.confidence_score);

  return (
    <div className="results-container" style={{ animation: 'fadeIn 0.5s ease', display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {/* Header Results */}
      <div className="glass-panel" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 style={{ margin: 0, color: '#fff' }}>Resultados de la Evaluación</h2>
          <p style={{ margin: 0, color: 'var(--text-secondary)' }}>
            Confianza de IA: <strong style={{ color: confidence > 0.75 ? 'var(--color-success)' : 'var(--color-warning)' }}>
              {Number.isFinite(confidence) ? `${(confidence * 100).toFixed(0)}%` : 'No disponible'}
            </strong>
          </p>
        </div>
        <div style={{ textAlign: 'right' }}>
          <div style={{ fontSize: '2.5rem', fontWeight: 'bold', color: 'var(--accent-primary)', lineHeight: '1' }}>
            {resultado_ia.calificacion_numerica ?? '—'}
          </div>
          <span style={{ fontSize: '1rem', color: 'var(--text-secondary)', textTransform: 'uppercase' }}>
            {resultado_ia.calificacion_cualitativa || 'Nota Sugerida'}
          </span>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem' }}>
        {/* Resumen Docente */}
        <div className="glass-panel">
          <h3 style={{ color: '#fff', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            🎓 Resumen para el Docente
          </h3>
          <p style={{ color: 'var(--text-primary)', fontSize: '0.95rem' }}>
            {analysis.teacherSummary || 'No se recibió un resumen docente.'}
          </p>
        </div>

        {/* Siguiente Paso Accionable */}
        <div className="glass-panel" style={{ borderLeft: '4px solid var(--accent-primary)' }}>
          <h3 style={{ color: '#fff', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            🎯 Siguiente Paso Accionable
          </h3>
          <p style={{ color: 'var(--text-primary)', fontSize: '0.95rem' }}>
            {resultado_ia.siguiente_paso_accionable || 'No se indicó un siguiente paso.'}
          </p>
        </div>
      </div>

      {resultado_ia.transcription && (
        <div className="glass-panel">
          <h3 style={{ color: '#fff', marginBottom: '1rem' }}>📝 Transcripción</h3>
          <p style={{ color: 'var(--text-primary)', whiteSpace: 'pre-wrap' }}>
            {resultado_ia.transcription}
          </p>
        </div>
      )}

      <div className="glass-panel">
        <h3 style={{ color: '#fff', marginBottom: '1rem' }}>📊 Desglose de Rúbrica</h3>
        {rubricBreakdown.length === 0 ? (
          <p style={{ color: 'var(--text-secondary)' }}>No se recibió un desglose de criterios.</p>
        ) : (
          <div style={{ display: 'grid', gap: '1rem' }}>
            {rubricBreakdown.map((item, index) => (
              <div key={`${item.criterio_codigo || item.category || 'criterio'}-${index}`} style={{ background: 'rgba(255, 255, 255, 0.04)', border: 'var(--border-glass)', borderRadius: 'var(--radius-md)', padding: '1rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', gap: '1rem', flexWrap: 'wrap' }}>
                  <h4 style={{ color: '#fff', margin: 0 }}>{item.category || `Criterio ${index + 1}`}</h4>
                  <strong style={{ color: 'var(--accent-primary)' }}>{item.score ?? '—'} / {item.maxScore ?? '—'}</strong>
                </div>
                {(item.criterio_codigo || getList(item.competencias_clave).length > 0) && (
                  <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginTop: '0.5rem' }}>
                    {item.criterio_codigo && `Código: ${item.criterio_codigo}`}
                    {item.criterio_codigo && getList(item.competencias_clave).length > 0 && ' · '}
                    {getList(item.competencias_clave).length > 0 && `Competencias: ${getList(item.competencias_clave).join(', ')}`}
                  </p>
                )}
                {(item.peso !== undefined || item.nivel_logro !== undefined) && (
                  <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginTop: '0.5rem' }}>
                    {item.peso !== undefined && `Peso: ${item.peso}%`}
                    {item.peso !== undefined && item.nivel_logro !== undefined && ' · '}
                    {item.nivel_logro !== undefined && `Nivel de logro: ${item.nivel_logro}`}
                  </p>
                )}
                {item.reasoning && <p style={{ color: 'var(--text-primary)', fontSize: '0.95rem', marginTop: '0.75rem' }}>{item.reasoning}</p>}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Fortalezas y Mejoras */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1.5rem' }}>
        <div className="glass-panel" style={{ background: 'rgba(16, 185, 129, 0.05)', border: '1px solid rgba(16, 185, 129, 0.2)' }}>
          <h3 style={{ color: 'var(--color-success)', marginBottom: '1rem' }}>Fortalezas</h3>
          <ul style={{ paddingLeft: '1.2rem', color: 'var(--text-primary)' }}>
            {strengths.map((s, i) => (
              <li key={i} style={{ marginBottom: '0.5rem' }}>{s}</li>
            ))}
          </ul>
        </div>

        <div className="glass-panel" style={{ background: 'rgba(239, 68, 68, 0.05)', border: '1px solid rgba(239, 68, 68, 0.2)' }}>
          <h3 style={{ color: 'var(--color-danger)', marginBottom: '1rem' }}>Mejoras Inmediatas</h3>
          <ul style={{ paddingLeft: '1.2rem', color: 'var(--text-primary)' }}>
            {immediateImprovements.map((s, i) => (
              <li key={i} style={{ marginBottom: '0.5rem' }}>{s}</li>
            ))}
          </ul>
        </div>

        <div className="glass-panel" style={{ background: 'rgba(245, 158, 11, 0.05)', border: '1px solid rgba(245, 158, 11, 0.2)' }}>
          <h3 style={{ color: 'var(--color-warning)', marginBottom: '1rem' }}>Mejoras a Medio y Largo Plazo</h3>
          <ul style={{ paddingLeft: '1.2rem', color: 'var(--text-primary)' }}>
            {mediumLongTermImprovements.map((s, i) => (
              <li key={i} style={{ marginBottom: '0.5rem' }}>{s}</li>
            ))}
          </ul>
        </div>
      </div>

      {visualMarkers.length > 0 && (
        <div className="glass-panel">
          <h3 style={{ color: '#fff', marginBottom: '1rem' }}>🔎 Observaciones Visuales</h3>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>
            Se detectaron {visualMarkers.length} observación{visualMarkers.length === 1 ? '' : 'es'} visual{visualMarkers.length === 1 ? '' : 'es'}.
          </p>
          <ul style={{ paddingLeft: '1.2rem', color: 'var(--text-primary)' }}>
            {visualMarkers.map((marker, index) => (
              <li key={`${marker.type || 'observacion'}-${index}`}>
                {marker.type || 'Observación'} {marker.message || marker.reason || marker.description ? `— ${marker.message || marker.reason || marker.description}` : ''}
              </li>
            ))}
          </ul>
        </div>
      )}

      <div style={{ display: 'flex', justifyContent: 'center', marginTop: '1rem' }}>
        <button onClick={onReset} style={{
          background: 'var(--bg-glass)',
          border: 'var(--border-glass)',
          color: '#fff',
          padding: '1rem 2rem',
          fontSize: '1.1rem',
          borderRadius: '8px',
          cursor: 'pointer',
          transition: 'all 0.2s ease',
          boxShadow: 'var(--shadow-glass)'
        }}>
          ⬅️ Volver a Capturar
        </button>
      </div>
    </div>
  );
};

export default ResultsPanel;
