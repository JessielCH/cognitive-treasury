import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def generate_synthetic_data(num_records=50):
    """Genera datos simulados de tesorería corporativa."""
    np.random.seed(42) # Para reproducibilidad en pruebas
    
    data = {
        "id_factura": [f"FAC-{i:04d}" for i in range(1, num_records + 1)],
        "proveedor": [f"Proveedor {chr(65 + (i % 26))}" for i in range(num_records)],
        "monto": np.round(np.random.uniform(5000, 150000, num_records), 2),
        "antiguedad_dias": np.random.randint(5, 180, num_records),
        "criticidad_operativa": np.random.randint(1, 6, num_records), # Escala 1-5
        "grupo_pago": np.random.choice(
            ['Servicios Básicos', 'Inversión', 'Gasto Corriente', 'Emergentes (Legal)'], 
            num_records, p=[0.2, 0.3, 0.4, 0.1]
        )
    }
    return pd.DataFrame(data)

def calculate_pca_urgency(df):
    """Aplica PCA para reducir variables y generar un Score de Urgencia."""
    # Variables a analizar
    features = ['monto', 'antiguedad_dias', 'criticidad_operativa']
    x = df[features].values
    
    # Estandarizar los datos (Media=0, Varianza=1)
    x_scaled = StandardScaler().fit_transform(x)
    
    # Aplicar PCA (1 Componente Principal)
    pca = PCA(n_components=1)
    df['score_pca_bruto'] = pca.fit_transform(x_scaled)
    
    # Normalizar el Score de 0 a 100 para la interfaz
    min_score = df['score_pca_bruto'].min()
    max_score = df['score_pca_bruto'].max()
    df['score_urgencia'] = np.round(((df['score_pca_bruto'] - min_score) / (max_score - min_score)) * 100, 1)
    
    # Limpiar columna temporal y ordenar
    df = df.drop(columns=['score_pca_bruto'])
    df = df.sort_values(by='score_urgencia', ascending=False)
    
    return df.to_dict(orient="records")