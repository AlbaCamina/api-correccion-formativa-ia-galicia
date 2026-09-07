import React, { useState, useEffect } from 'react';
import '../index.css';

const ResultsPanel = ({ submissionId, onReset }) => {
  const [evaluacion, setEvaluacion] = useState(null);
  const [error, setError] = useState(null);
  const [isPolling, setIsPolling] = useState(true);

  useEffect(() => {
    let intervalId;

    const pollResult = async () => {
      try {
        const res = await fetch(`http://localhost:8000/api/v1/evaluaciones/${submissionId}`);
        if (res.ok) {
          const data = await res.json();
          setEvaluacion(data);
          setIsPolling(false);
          clearInterval(intervalId);
        } else if (res.status !== 404) {
          // If it's not a 404 (Not Found yet), it's a real error
          throw new Error('Error al obtener la evaluación');
        }
      } catch (err) {
        // Ignoramos errores de red temporalmente mientras hacemos polling
        console.warn("Polling en progreso...", err);
      }
    };

    pollResult(); // first try
    intervalId = setInterval(pollResult, 3000);

    return () => clearInterval(intervalId);
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
        <h2 style={{ color: 'var(--color-danger)' }}>Error</h2>
        <p>{error}</p>
        <button onClick={onReset} style={{ marginTop: '1rem', background: '#444', color: '#fff', border: 'none', padding: '0.8rem 1.5rem', borderRadius: '8px' }}>Volver</button>
      </div>
    );
  }

  if (!evaluacion || !evaluacion.resultado_ia) return null;

  const { resultado_ia } = evaluacion;
  const analysis = resultado_ia.qualitativeAnalysis;

  return (
    <div className="results-container" style={{ animation: 'fadeIn 0.5s ease', display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {/* Header Results */}
      <div className="glass-panel" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 style={{ margin: 0, color: '#fff' }}>Resultados de la Evaluación</h2>
          <p style={{ margin: 0, color: 'var(--text-secondary)' }}>
            Confianza de IA: <strong style={{ color: resultado_ia.confidence_score > 0.75 ? 'var(--color-success)' : 'var(--color-warning)' }}>
              {(resultado_ia.confidence_score * 100).toFixed(0)}%
            </strong>
          </p>
        </div>
        <div style={{ textAlign: 'right' }}>
          <div style={{ fontSize: '2.5rem', fontWeight: 'bold', color: 'var(--accent-primary)', lineHeight: '1' }}>
            {resultado_ia.calificacion_numerica}
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
            {analysis.teacherSummary}
          </p>
        </div>

        {/* Siguiente Paso Accionable */}
        <div className="glass-panel" style={{ borderLeft: '4px solid var(--accent-primary)' }}>
          <h3 style={{ color: '#fff', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            🎯 Siguiente Paso Accionable
          </h3>
          <p style={{ color: 'var(--text-primary)', fontSize: '0.95rem' }}>
            {resultado_ia.siguiente_paso_accionable}
          </p>
        </div>
      </div>

      {/* Fortalezas y Mejoras */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1.5rem' }}>
        <div className="glass-panel" style={{ background: 'rgba(16, 185, 129, 0.05)', border: '1px solid rgba(16, 185, 129, 0.2)' }}>
          <h3 style={{ color: 'var(--color-success)', marginBottom: '1rem' }}>Fortalezas</h3>
          <ul style={{ paddingLeft: '1.2rem', color: 'var(--text-primary)' }}>
            {analysis.strengths.map((s, i) => (
              <li key={i} style={{ marginBottom: '0.5rem' }}>{s}</li>
            ))}
          </ul>
        </div>
        
        <div className="glass-panel" style={{ background: 'rgba(239, 68, 68, 0.05)', border: '1px solid rgba(239, 68, 68, 0.2)' }}>
          <h3 style={{ color: 'var(--color-danger)', marginBottom: '1rem' }}>Mejoras Inmediatas</h3>
          <ul style={{ paddingLeft: '1.2rem', color: 'var(--text-primary)' }}>
            {analysis.improvementNeeds.immediate.map((s, i) => (
              <li key={i} style={{ marginBottom: '0.5rem' }}>{s}</li>
            ))}
          </ul>
        </div>
      </div>

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
