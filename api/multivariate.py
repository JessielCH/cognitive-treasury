import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from .rlhf_engine import get_current_weights # <-- Importar el lector de pesos

def generate_synthetic_data(num_records=50):
    # ... (Mantén tu código actual de esta función intacto) ...
    np.random.seed(42) 
    data = {
        "id_factura": [f"FAC-{i:04d}" for i in range(1, num_records + 1)],
        "proveedor": [f"Proveedor {chr(65 + (i % 26))}" for i in range(num_records)],
        "monto": np.round(np.random.uniform(5000, 150000, num_records), 2),
        "antiguedad_dias": np.random.randint(5, 180, num_records),
        "criticidad_operativa": np.random.randint(1, 6, num_records),
        "grupo_pago": np.random.choice(
            ['Servicios Básicos', 'Inversión', 'Gasto Corriente', 'Emergentes (Legal)'], 
            num_records, p=[0.2, 0.3, 0.4, 0.1]
        )
    }
    return pd.DataFrame(data)

def calculate_pca_urgency(df):
    """Aplica PCA modulado por los pesos del RLHF."""
    features = ['monto', 'antiguedad_dias', 'criticidad_operativa']
    
    # 1. Estandarizar los datos puros
    x = df[features].values
    x_scaled = StandardScaler().fit_transform(x)
    
    # 2. Aplicar los pesos aprendidos (Cognitive Injection)
    weights = get_current_weights()
    weight_vector = np.array([weights["monto"], weights["antiguedad_dias"], weights["criticidad_operativa"]])
    
    # Multiplicamos la matriz escalada por los pesos
    x_weighted = x_scaled * weight_vector
    
    # 3. Aplicar PCA sobre los datos ponderados
    pca = PCA(n_components=1)
    df['score_pca_bruto'] = pca.fit_transform(x_weighted)
    
    # Normalizar el Score de 0 a 100
    min_score = df['score_pca_bruto'].min()
    max_score = df['score_pca_bruto'].max()
    # Evitar división por cero
    if max_score == min_score:
        df['score_urgencia'] = 50.0
    else:
        df['score_urgencia'] = np.round(((df['score_pca_bruto'] - min_score) / (max_score - min_score)) * 100, 1)
    
    df = df.drop(columns=['score_pca_bruto'])
    df = df.sort_values(by='score_urgencia', ascending=False)
    
    return df.to_dict(orient="records")