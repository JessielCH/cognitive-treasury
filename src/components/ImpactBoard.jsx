import { useState, useEffect } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { Activity } from "lucide-react";

const ImpactBoard = () => {
  const [invoices, setInvoices] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Llamada al backend de FastAPI
    fetch("http://localhost:8000/api/invoices")
      .then((res) => res.json())
      .then((data) => {
        // Tomamos solo el top 10 más urgente para el gráfico
        setInvoices(data.data.slice(0, 10));
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching data:", err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="p-8">
      <div className="flex items-center gap-3 mb-8 border-b pb-4">
        <Activity className="w-8 h-8 text-blue-600" />
        <h1 className="text-3xl font-bold text-gray-800">
          Panel de Proyecciones (Impact Board)
        </h1>
      </div>

      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <h2 className="text-xl font-semibold mb-6 text-gray-700">
          Top 10 Obligaciones por Score de Urgencia (PCA)
        </h2>

        {loading ? (
          <div className="h-96 flex items-center justify-center text-gray-500 animate-pulse">
            Calculando proyecciones multivariantes...
          </div>
        ) : (
          <div className="h-96 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={invoices}
                margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
              >
                <CartesianGrid
                  strokeDasharray="3 3"
                  vertical={false}
                  stroke="#e5e7eb"
                />
                <XAxis dataKey="id_factura" tick={{ fill: "#6b7280" }} />
                <YAxis yAxisId="left" orientation="left" stroke="#3b82f6" />
                <YAxis yAxisId="right" orientation="right" stroke="#ef4444" />
                <Tooltip
                  contentStyle={{
                    borderRadius: "8px",
                    border: "none",
                    boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.1)",
                  }}
                />
                <Legend />
                <Bar
                  yAxisId="left"
                  dataKey="monto"
                  name="Monto ($)"
                  fill="#3b82f6"
                  radius={[4, 4, 0, 0]}
                />
                <Bar
                  yAxisId="right"
                  dataKey="score_urgencia"
                  name="Score Urgencia (PCA)"
                  fill="#ef4444"
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </div>
  );
};

export default ImpactBoard;
