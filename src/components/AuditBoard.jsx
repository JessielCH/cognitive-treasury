import { useState, useEffect } from "react";
import { ShieldAlert, BrainCircuit, AlertTriangle } from "lucide-react";

const AuditBoard = () => {
  const [auditData, setAuditData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/api/audit-anomalies")
      .then((res) => res.json())
      .then((data) => {
        setAuditData(data);
        setLoading(false);
      })
      .catch((err) => console.error(err));
  }, []);

  if (loading)
    return (
      <div className="p-8 animate-pulse text-gray-500">
        Ejecutando algoritmos de clustering (DBSCAN)...
      </div>
    );

  return (
    <div className="p-8">
      <div className="flex items-center gap-3 mb-8 border-b pb-4">
        <ShieldAlert className="w-8 h-8 text-blue-600" />
        <h1 className="text-3xl font-bold text-gray-800">
          Auditoría y Transparencia Cognitiva
        </h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Columna Izquierda: Explainable AI (XAI) */}
        <div className="lg:col-span-1 bg-white p-6 rounded-xl shadow-sm border border-gray-200">
          <div className="flex items-center gap-2 mb-4">
            <BrainCircuit className="w-6 h-6 text-indigo-500" />
            <h2 className="text-xl font-semibold text-gray-700">
              Estado de la Política RLHF
            </h2>
          </div>
          <p className="text-sm text-gray-500 mb-6">
            Pesos actuales aprendidos de las decisiones del Gerente de Finanzas.
          </p>

          <div className="space-y-4">
            {Object.entries(auditData.current_policy_weights).map(
              ([key, value]) => (
                <div key={key}>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="font-medium text-gray-700 capitalize">
                      {key.replace("_", " ")}
                    </span>
                    <span className="font-bold text-indigo-600">
                      {Number(value).toFixed(2)}x
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-indigo-500 h-2 rounded-full"
                      style={{ width: `${Math.min((value / 2) * 100, 100)}%` }}
                    ></div>
                  </div>
                </div>
              ),
            )}
          </div>
        </div>

        {/* Columna Derecha: Alertas de Clustering */}
        <div className="lg:col-span-2 bg-white p-6 rounded-xl shadow-sm border border-gray-200">
          <div className="flex items-center gap-2 mb-4">
            <AlertTriangle className="w-6 h-6 text-red-500" />
            <h2 className="text-xl font-semibold text-gray-700">
              Pagos Emergentes Detectados
            </h2>
          </div>
          <p className="text-sm text-gray-500 mb-6">
            El algoritmo DBSCAN analizó {auditData.clustering.total_analyzed}{" "}
            facturas y encontró {auditData.clustering.anomaly_count} anomalías
            que rompen el flujo normal.
          </p>

          <div className="space-y-3">
            {auditData.clustering.anomalies.map((anomalia, idx) => (
              <div
                key={idx}
                className="p-4 border-l-4 border-red-500 bg-red-50 rounded-r-lg flex justify-between items-center"
              >
                <div>
                  <h3 className="font-bold text-red-800">
                    {anomalia.id_factura}
                  </h3>
                  <p className="text-sm text-red-600 font-medium">
                    {anomalia.proveedor}
                  </p>
                  <p className="text-xs text-red-500 mt-1">
                    Antigüedad: {anomalia.antiguedad_dias} días | Criticidad:{" "}
                    {anomalia.criticidad_operativa}/5
                  </p>
                </div>
                <div className="text-right">
                  <p className="text-xl font-extrabold text-red-700">
                    ${anomalia.monto.toLocaleString()}
                  </p>
                  <span className="inline-block mt-1 text-xs font-bold bg-red-200 text-red-800 px-2 py-1 rounded uppercase">
                    {anomalia.grupo_pago}
                  </span>
                </div>
              </div>
            ))}

            {auditData.clustering.anomalies.length === 0 && (
              <div className="p-6 text-center text-gray-500 bg-gray-50 rounded-lg">
                No se detectaron pagos anómalos o emergentes en esta ejecución.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuditBoard;
