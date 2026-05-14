import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import ImpactBoard from "./components/ImpactBoard";
import Calendar from "./components/Calendar";
import AuditBoard from "./components/AuditBoard"; // <-- NUEVA IMPORTACIÓN

// Mantenemos Auditoria como placeholder hasta la Fase 3
function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50 text-gray-900 font-sans flex">
        {/* Barra Lateral (Sidebar) */}
        <aside className="w-64 bg-slate-900 text-white p-6 shadow-xl z-10">
          <h2 className="text-xl font-extrabold mb-8 text-blue-400 tracking-tight">
            Cognitive Treasury
          </h2>
          <nav className="space-y-3">
            <Link
              to="/"
              className="block py-2 px-4 rounded hover:bg-slate-800 hover:text-blue-300 transition-all"
            >
              Dashboard Proyectivo
            </Link>
            <Link
              to="/calendar"
              className="block py-2 px-4 rounded hover:bg-slate-800 hover:text-blue-300 transition-all"
            >
              Calendario de Pagos
            </Link>
            <Link
              to="/audit"
              className="block py-2 px-4 rounded hover:bg-slate-800 hover:text-blue-300 transition-all"
            >
              Auditoría y Clustering
            </Link>
          </nav>
        </aside>

        {/* Área Principal */}
        <main className="flex-1 bg-gray-50 overflow-y-auto">
          <Routes>
            <Route path="/" element={<ImpactBoard />} />
            <Route path="/calendar" element={<Calendar />} />
            <Route path="/audit" element={<AuditBoard />} />{" "}
            {/* <-- ACTUALIZADO */}
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
