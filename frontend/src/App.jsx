import './index.css';
import CameraCapture from './components/CameraCapture';
function App() {
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>CorrecciónIA</h1>
        <p>Entorno de Evaluación Formativa</p>
      </header>
      
      <main className="app-main">
        <div className="glass-panel">
          <CameraCapture />
        </div>
      </main>
    </div>
  );
}

export default App;
