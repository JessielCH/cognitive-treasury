import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

// Componentes Placeholder (los desarrollaremos en el siguiente paso)
const Dashboard = () => (
  <div className="p-4">
    <h1 className="text-2xl font-bold">Panel de Proyecciones (Impact Board)</h1>
    <p>Visualización PCA y What-If</p>
  </div>
);
const Calendar = () => (
  <div className="p-4">
    <h1 className="text-2xl font-bold">Calendario Interactivo</h1>
    <p>Motor de recolección RLHF (Arrastrar y Soltar)</p>
  </div>
);
const Auditoria = () => (
  <div className="p-4">
    <h1 className="text-2xl font-bold">Trazabilidad de IA</h1>
    <p>Detección de Pagos Emergentes (DBSCAN)</p>
  </div>
);

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50 text-gray-900 font-sans flex">
        {/* Sidebar de Navegación Lateral */}
        <aside className="w-64 bg-slate-900 text-white p-6">
          <h2 className="text-xl font-extrabold mb-8 text-blue-400">
            Cognitive Treasury
          </h2>
          <nav className="space-y-4">
            <Link
              to="/"
              className="block hover:text-blue-300 transition-colors"
            >
              Dashboard Proyectivo
            </Link>
            <Link
              to="/calendar"
              className="block hover:text-blue-300 transition-colors"
            >
              Calendario de Pagos
            </Link>
            <Link
              to="/audit"
              className="block hover:text-blue-300 transition-colors"
            >
              Auditoría y Clustering
            </Link>
          </nav>
        </aside>

        {/* Área Principal de Contenido */}
        <main className="flex-1 bg-white shadow-inner">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/calendar" element={<Calendar />} />
            <Route path="/audit" element={<Auditoria />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
