import { useState, useEffect } from "react";
import {
  Calendar as CalendarIcon,
  GripVertical,
  AlertTriangle,
} from "lucide-react";
import Chatbot from "./Chatbot"; // <-- Importamos el Copiloto IA

const Calendar = () => {
  // Estado para las facturas distribuidas por días de la semana
  const [schedule, setSchedule] = useState({
    Lunes: [],
    Martes: [],
    Miercoles: [],
    Jueves: [],
    Viernes: [],
  });

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // 1. Cargamos las facturas del motor analítico
    const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
    fetch(`${API_URL}/api/invoices`)
      .then((res) => res.json())
      .then((data) => {
        const invoices = data.data.slice(0, 20); // Tomamos 20 para el demo
        // 2. Simular una asignación inicial algorítmica ingenua (repartir entre los días)
        const initialSchedule = {
          Lunes: [],
          Martes: [],
          Miercoles: [],
          Jueves: [],
          Viernes: [],
        };
        const days = Object.keys(initialSchedule);

        invoices.forEach((inv, index) => {
          const day = days[index % days.length];
          initialSchedule[day].push(inv);
        });

        setSchedule(initialSchedule);
        setLoading(false);
      })
      .catch((err) => console.error(err));
  }, []);

  // --- LÓGICA DE DRAG AND DROP ---
  const handleDragStart = (e, invoiceId, sourceDay) => {
    e.dataTransfer.setData("invoiceId", invoiceId);
    e.dataTransfer.setData("sourceDay", sourceDay);
  };

  const handleDragOver = (e) => {
    e.preventDefault(); // Necesario para permitir el drop
  };

  const handleDrop = async (e, targetDay) => {
    e.preventDefault();
    const invoiceId = e.dataTransfer.getData("invoiceId");
    const sourceDay = e.dataTransfer.getData("sourceDay");

    if (sourceDay === targetDay) return; // No hacer nada si se suelta en el mismo día

    // 1. Actualizar la UI (React State)
    let movedInvoice = null;
    const newSchedule = { ...schedule };

    newSchedule[sourceDay] = newSchedule[sourceDay].filter((inv) => {
      if (inv.id_factura === invoiceId) {
        movedInvoice = inv;
        return false;
      }
      return true;
    });

    if (movedInvoice) {
      newSchedule[targetDay].push(movedInvoice);
      setSchedule(newSchedule);

      // 2. ENVIAR FEEDBACK AL MODELO RLHF (El núcleo de tu arquitectura)
      const feedbackPayload = {
        id_factura: invoiceId,
        dia_original: sourceDay,
        dia_nuevo: targetDay,
        motivo: "Re-priorización manual de Tesorería",
        detalles_factura: movedInvoice,
      };

      try {
        const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
        await fetch(`${API_URL}/api/capture-feedback`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(feedbackPayload),
        });
        console.log("Huella Digital capturada exitosamente.");
      } catch (error) {
        console.error("Error al enviar feedback RLHF:", error);
      }
    }
  };

  if (loading)
    return <div className="p-8 text-gray-500">Cargando calendario...</div>;

  return (
    <div className="p-8 relative">
      <div className="flex items-center gap-3 mb-8 border-b pb-4">
        <CalendarIcon className="w-8 h-8 text-blue-600" />
        <h1 className="text-3xl font-bold text-gray-800">
          Calendario de Pagos Semanal
        </h1>
      </div>
      <p className="mb-6 text-gray-600">
        Arrastra las obligaciones para ajustar la prelación. Cada movimiento
        entrena al modelo (RLHF).
      </p>

      <div className="grid grid-cols-5 gap-4">
        {Object.keys(schedule).map((day) => (
          <div
            key={day}
            className="bg-gray-100 rounded-lg p-4 min-h-[400px]"
            onDragOver={handleDragOver}
            onDrop={(e) => handleDrop(e, day)}
          >
            <h2 className="font-semibold text-lg mb-4 text-gray-700 border-b-2 border-blue-200 pb-2">
              {day}
            </h2>

            <div className="space-y-3">
              {schedule[day].map((invoice) => (
                <div
                  key={invoice.id_factura}
                  draggable
                  onDragStart={(e) =>
                    handleDragStart(e, invoice.id_factura, day)
                  }
                  className="bg-white p-3 rounded shadow-sm border border-gray-200 cursor-move hover:shadow-md transition-shadow relative"
                >
                  <div className="flex items-start justify-between mb-2">
                    <span className="text-xs font-bold text-blue-600">
                      {invoice.id_factura}
                    </span>
                    <GripVertical className="w-4 h-4 text-gray-400" />
                  </div>
                  <p className="text-sm font-medium text-gray-800 line-clamp-1">
                    {invoice.proveedor}
                  </p>
                  <p className="text-lg font-bold text-gray-900 my-1">
                    ${invoice.monto.toLocaleString()}
                  </p>

                  <div className="flex items-center justify-between mt-2">
                    <span className="text-xs bg-gray-100 px-2 py-1 rounded text-gray-600 truncate max-w-[100px]">
                      {invoice.grupo_pago}
                    </span>
                    {invoice.score_urgencia > 80 && (
                      <AlertTriangle
                        className="w-4 h-4 text-red-500"
                        title="Alta Urgencia PCA"
                      />
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* --- INTEGRACIÓN DEL COPILOTO IA --- */}
      <Chatbot schedule={schedule} />
    </div>
  );
};

export default Calendar;
