import json
import os
from pathlib import Path

# Configurar la ruta del archivo de pesos
# En Railway, se recomienda usar un volumen montado en /app/api/data
# En desarrollo local, usará api/data/rlhf_weights.json
WEIGHTS_DIR = os.getenv("WEIGHTS_STORAGE_PATH", os.path.join("api", "data"))
if not isinstance(WEIGHTS_DIR, str):
    WEIGHTS_DIR = os.path.dirname(WEIGHTS_DIR)
else:
    WEIGHTS_DIR = os.path.dirname(WEIGHTS_DIR) if WEIGHTS_DIR.endswith('.json') else WEIGHTS_DIR

# Asegurar que la carpeta existe
os.makedirs(WEIGHTS_DIR, exist_ok=True)

WEIGHTS_FILE = os.path.join(WEIGHTS_DIR, "rlhf_weights.json")

def get_current_weights():
    """Obtiene los pesos actuales aprendidos del gerente."""
    try:
        if os.path.exists(WEIGHTS_FILE):
            with open(WEIGHTS_FILE, "r") as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"⚠️  Error al leer {WEIGHTS_FILE}: {e}. Usando pesos por defecto.")
    
    # Pesos base iniciales (Equitativos)
    return {"monto": 1.0, "antiguedad_dias": 1.0, "criticidad_operativa": 1.0}

def save_weights(weights):
    """Guarda la nueva política de pesos."""
    try:
        os.makedirs(WEIGHTS_DIR, exist_ok=True)
        with open(WEIGHTS_FILE, "w") as f:
            json.dump(weights, f, indent=2)
        print(f"✅ Pesos guardados en {WEIGHTS_FILE}")
    except IOError as e:
        print(f"❌ Error al guardar pesos: {e}")

def optimize_preferences(feedback_data):
    """
    Ajusta los pesos basándose en la retroalimentación humana (DPO simplificado).
    Calcula el vector de preferencia analizando qué atributos tenía la factura movida.
    """
    weights = get_current_weights()
    learning_rate = 0.05 # Tasa de aprendizaje
    
    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    try:
        idx_original = dias.index(feedback_data.get('dia_original'))
        idx_nuevo = dias.index(feedback_data.get('dia_nuevo'))
    except ValueError:
        return weights
        
    # Si el índice nuevo es menor, significa que el usuario PRIORIZÓ el pago
    is_prioritized = idx_nuevo < idx_original
    
    factura = feedback_data.get('detalles_factura', {})
    
    # Ajuste del Reward Model: Premiar los atributos de lo que el humano prioriza
    if is_prioritized:
        if factura.get("monto", 0) > 50000:
            weights["monto"] += learning_rate
        if factura.get("antiguedad_dias", 0) > 30:
            weights["antiguedad_dias"] += learning_rate
        if factura.get("criticidad_operativa", 0) >= 3:
            weights["criticidad_operativa"] += learning_rate
    else:
        # Si la retrasó, reducimos ligeramente la importancia de sus atributos dominantes
        weights["monto"] = max(0.1, weights["monto"] - (learning_rate / 2))
            
    save_weights(weights)
    return weights