from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Cognitive Treasury API", version="1.0")

# Evitar problemas de CORS durante el desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic para validación de datos
class PaymentScenario(BaseModel):
    scenario_id: str
    total_amount: float
    urgency_score: float

@app.get("/api/health")
def read_health():
    return {"status": "ok", "system": "Cognitive Treasury Motor - Active"}

@app.post("/api/simulate")
def simulate_cashflow(scenario: PaymentScenario):
    # Aquí integraremos posteriormente el motor PCA
    return {
        "message": "Simulación recibida", 
        "projected_liquidity": 1500000.00 - scenario.total_amount
    }

@app.post("/api/capture-feedback")
def capture_decision_footprint(decision_data: dict):
    # Endpoint para capturar la Huella Digital de Decisión (RLHF)
    return {"status": "Feedback captured", "vector_recorded": True}