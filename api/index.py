from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# api/index.py

from multivariate import generate_synthetic_data, calculate_pca_urgency
from rlhf_engine import optimize_preferences, get_current_weights
from clustering import detect_anomalies
from chatbot import ask_treasury_copilot
# Si llegaste a crear predictive.py, inclúyelo también:
# from predictive import generate_executive_summary
app = FastAPI(title="Cognitive Treasury API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PaymentScenario(BaseModel):
    scenario_id: str
    total_amount: float
    urgency_score: float

# Modelo Pydantic para recibir el chat
class ChatRequest(BaseModel):
    message: str
    calendar_state: dict

@app.get("/")
def read_root():
    return {"status": "El backend está funcionando. Visita /docs o /redoc para la API."}

@app.get("/api/invoices")
def get_invoices():
    # Ahora enviamos también los pesos actuales para visualizarlos en el frontend
    df_raw = generate_synthetic_data(num_records=30)
    processed_data = calculate_pca_urgency(df_raw)
    current_weights = get_current_weights()
    return {
        "data": processed_data, 
        "count": len(processed_data),
        "active_weights": current_weights # <-- Enviamos la política actual
    }

# --- RUTA ACTUALIZADA PARA RLHF ---
@app.post("/api/capture-feedback")
def capture_decision_footprint(decision_data: dict):
    print(f"--- PROCESANDO HUELLA DIGITAL ---")
    print(f"Factura: {decision_data.get('id_factura')} | Movimiento: {decision_data.get('dia_original')} -> {decision_data.get('dia_nuevo')}")
    
    # 1. Ejecutar la optimización de preferencias
    new_weights = optimize_preferences(decision_data)
    
    print(f"Nuevos pesos aprendidos: {new_weights}")
    
    return {
        "status": "Feedback procesado y modelo ajustado", 
        "vector_recorded": True,
        "new_policy": new_weights
    }

# --- RUTA PARA AUDITORÍA Y CLUSTERING ---
@app.get("/api/audit-anomalies")
def get_audit_anomalies():
    """Ejecuta el pipeline de Explainable AI (XAI) y Clustering."""
    resultados = detect_anomalies()
    pesos_actuales = get_current_weights()
    
    return {
        "status": "Auditoría completada",
        "clustering": resultados,
        "current_policy_weights": pesos_actuales
    }

# --- RUTA PARA EL COPILOTO (GEMINI) ---
@app.post("/api/chat")
def chat_with_copilot(request: ChatRequest):
    """Endpoint para el asistente virtual usando Gemini."""
    respuesta = ask_treasury_copilot(request.message, request.calendar_state)
    return {"reply": respuesta}