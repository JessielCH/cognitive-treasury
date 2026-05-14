import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from .multivariate import generate_synthetic_data

def detect_anomalies():
    """Detecta pagos atípicos o emergentes usando DBSCAN."""
    
    # 1. Generar datos normales
    df = generate_synthetic_data(num_records=80)
    
    # 2. Inyectar anomalías simuladas (Pagos de altísimo impacto y urgencia)
    anomalias_fijas = pd.DataFrame({
        "id_factura": ["SENTENCIA-001", "MULTA-SRI-002"],
        "proveedor": ["Corte Nacional de Justicia", "Servicio de Rentas Internas"],
        "monto": [850000.0, 1200000.0], # Montos extremadamente altos
        "antiguedad_dias": [2, 5],      # Muy recientes (inusual para montos altos)
        "criticidad_operativa": [5, 5],
        "grupo_pago": ["Emergentes (Legal)", "Emergentes (Legal)"]
    })
    df = pd.concat([df, anomalias_fijas], ignore_index=True)

    # 3. Preparar variables para el modelo
    features = ['monto', 'antiguedad_dias']
    x = df[features].values
    x_scaled = StandardScaler().fit_transform(x)

    # 4. Aplicar DBSCAN
    # eps = 0.5 (radio de búsqueda), min_samples = 5 (vecinos mínimos para ser 'normal')
    db = DBSCAN(eps=0.5, min_samples=5).fit(x_scaled)
    df['cluster'] = db.labels_
    
    # 5. Filtrar resultados (DBSCAN marca el ruido/anomalías con el label -1)
    anomalies = df[df['cluster'] == -1].copy()
    
    # Formatear para el frontend
    return {
        "total_analyzed": len(df),
        "anomaly_count": len(anomalies),
        "anomalies": anomalies.to_dict(orient="records")
    }