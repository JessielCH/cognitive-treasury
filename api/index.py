from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .multivariate import generate_synthetic_data, calculate_pca_urgency

app = FastAPI(title="Cognitive Treasury API", version="1.0")

# Configuración de CORS para permitir peticiones desde React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de datos
class PaymentScenario(BaseModel):
    scenario_id: str
    total_amount: float
    urgency_score: float

# --- RUTAS DE SISTEMA ---

@app.get("/")
def read_root():
    return {"status": "El backend está funcionando. Visita /docs o /redoc para la API."}

@app.get("/api/health")
def read_health():
    return {"status": "ok", "system": "Cognitive Treasury Motor - Active"}

# --- RUTAS CORE (ANÁLISIS Y RLHF) ---

@app.get("/api/invoices")
def get_invoices():
    """Genera datos sintéticos, calcula urgencia vía PCA y los envía al frontend."""
    df_raw = generate_synthetic_data(num_records=30)
    processed_data = calculate_pca_urgency(df_raw)
    return {"data": processed_data, "count": len(processed_data)}

@app.post("/api/capture-feedback")
def capture_decision_footprint(decision_data: dict):
    """Endpoint para capturar la Huella Digital de Decisión (RLHF)"""
    print(f"\n--- HUELLA DIGITAL CAPTURADA ---")
    print(f"Factura: {decision_data.get('id_factura')}")
    print(f"Movimiento: {decision_data.get('dia_original')} -> {decision_data.get('dia_nuevo')}")
    print(f"Motivo: {decision_data.get('motivo')}")
    print(f"--------------------------------\n")
    
    return {"status": "Feedback captured", "vector_recorded": True}