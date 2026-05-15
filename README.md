# 🏛️ Cognitive Treasury - Asistente Inteligente de Tesorería

> **Cognitive Treasury** es una plataforma de inteligencia artificial para optimizar decisiones de flujo de caja mediante aprendizaje por preferencias humanas (RLHF).

![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Node.js](https://img.shields.io/badge/Node.js-18+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🎯 Características Principales

✨ **Asistente Cognitivo** - Copiloto IA (Gemini) para análisis de flujo de caja
📅 **Calendario Inteligente** - Drag & drop para re-priorizar pagos
📊 **Panel de Impacto** - Visualización de proyecciones multivariantes (PCA)
🔍 **Auditoría XAI** - Explainable AI + Detección de anomalías (DBSCAN)
🧠 **Aprendizaje en Tiempo Real** - RLHF (Reinforcement Learning from Human Feedback) adaptativo

---

## 🚀 Despliegue Rápido en Railway

### Opción 1: Desplegar desde GitHub

1. Ve a [Railway.app](https://railway.app)
2. Haz clic en **"New Project" → "Deploy from GitHub"**
3. Conecta tu repositorio
4. Railway auto-detectará `Procfile` y levantará el servidor

### Opción 2: CLI de Railway

```bash
npm install -g @railway/cli
railway login
railway link
railway up
```

### Configuración Post-Despliegue

Después de desplegar, configura estas variables en Railway Dashboard:

```bash
GOOGLE_API_KEY=tu_clave_gemini
VITE_API_URL=https://your-railway-domain.railway.app
WEIGHTS_STORAGE_PATH=/app/api/data/rlhf_weights.json
```

👉 Ver guía completa: [RAILWAY_DEPLOYMENT_GUIDE.md](./RAILWAY_DEPLOYMENT_GUIDE.md)

---

## 🏠 Desarrollo Local

### Requisitos

- Python 3.10+
- Node.js 18+
- pip y npm

### Quick Start

```bash
# 1. Clonar y navegar
git clone https://github.com/tu-usuario/cognitive-treasury.git
cd cognitive-treasury

# 2. Backend (Terminal 1)
python -m venv venv
# Windows: .\venv\Scripts\Activate.ps1
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt api/requirements.txt

# Crear directorio de datos
mkdir -p api/data

# Ejecutar FastAPI
uvicorn api.index:app --reload --host 0.0.0.0 --port 8000

# 3. Frontend (Terminal 2)
npm install
npm run dev

# ✅ Abrir http://localhost:5173
```

📚 Guía detallada: [DEVELOPMENT_SETUP.md](./DEVELOPMENT_SETUP.md)

---

## 📁 Estructura del Proyecto

```
cognitive-treasury/
├── api/                       # Backend FastAPI
│   ├── index.py              # Punto de entrada (main app)
│   ├── chatbot.py            # Integración Gemini
│   ├── clustering.py         # Análisis de anomalías (DBSCAN)
│   ├── multivariate.py       # PCA y scoring de urgencia
│   ├── rlhf_engine.py        # Motor de aprendizaje
│   ├── data/                 # 📁 Datos persistentes
│   └── requirements.txt      # Dependencias Python
│
├── src/                       # Frontend React + Vite
│   ├── components/
│   │   ├── AuditBoard.jsx    # Dashboard de auditoría
│   │   ├── Calendar.jsx      # Calendario interactivo
│   │   ├── Chatbot.jsx       # Chat con Gemini
│   │   └── ImpactBoard.jsx   # Gráficos de proyección
│   ├── App.jsx               # Componente principal
│   └── main.jsx              # Punto de entrada
│
├── public/                    # Assets estáticos
├── Procfile                   # Instrucciones para Railway
├── railway.toml              # Config de Railway
├── Dockerfile                # Build con Docker
├── vite.config.js            # Config de Vite
├── package.json              # Deps de npm
├── requirements.txt          # Deps de Python (global)
└── .env.example              # Template de env vars
```

---

## 🔌 API Endpoints

| Método | Endpoint                | Descripción                           |
| ------ | ----------------------- | ------------------------------------- |
| GET    | `/`                     | Health check                          |
| GET    | `/api/invoices`         | Obtener facturas con urgencia         |
| POST   | `/api/capture-feedback` | Registrar decisión de re-priorización |
| GET    | `/api/audit-anomalies`  | Detectar anomalías y pesos actuales   |
| POST   | `/api/chat`             | Chat con copiloto IA                  |

📖 **Docs Interactivos:** `http://localhost:8000/docs`

---

## ⚙️ Configuración

### Variables de Entorno

Copia `.env.example` a `.env` y configura:

```bash
# Google AI (Gemini)
GOOGLE_API_KEY=your_api_key_here

# Frontend API URL
VITE_API_URL=http://localhost:8000          # local
VITE_API_URL=https://your-railway-app.railway.app  # producción

# Persistencia RLHF
WEIGHTS_STORAGE_PATH=/app/api/data/rlhf_weights.json
```

### Persistencia en Railway

Por defecto, los pesos RLHF se pierden en cada deploy. Para mantenerlos:

**Opción A: Volumen Local**

1. Ve a Railway → Settings → Volumes
2. Crea un volumen en `/app/api/data`

**Opción B: PostgreSQL** (recomendado para producción)

1. Añade servicio PostgreSQL en Railway
2. Modifica `api/rlhf_engine.py` para usar base de datos

---

## 🛠️ Tech Stack

### Backend

- **FastAPI** - Framework web asincrónico
- **Uvicorn** - ASGI server
- **Pandas** - Análisis de datos
- **Scikit-learn** - ML (PCA, DBSCAN)
- **Google Generative AI** - Integración Gemini
- **Python-dotenv** - Gestión de env vars

### Frontend

- **React** 19 - UI framework
- **Vite** - Build tool ultra-rápido
- **Tailwind CSS** - Estilos utilitarios
- **Recharts** - Visualización de gráficos
- **Lucide React** - Iconografía

### DevOps

- **Railway** - Cloud deployment
- **Docker** - Containerización
- **Procfile** - Orquestación

---

## 🔐 Seguridad

- ✅ CORS habilitado (configurable en producción)
- ✅ Variables sensibles en env vars
- ✅ Validación de entrada con Pydantic
- ✅ API docs solo en desarrollo (desactiva en prod)

---

## 📊 Arquitectura RLHF

1. **Usuario re-prioriza una factura** (Drag & Drop)
2. **Feedback se captura** en `/api/capture-feedback`
3. **Motor RLHF analiza** atributos (monto, antigüedad, criticidad)
4. **Pesos se actualizan** según preferencia humana
5. **Próximas sugerencias** usan nuevos pesos

```
Decisión Humana → Análisis de Atributos → Ajuste de Pesos → IA Mejorada
```

---

## 🐛 Troubleshooting

### Backend no levanta

```bash
# Verifica que FastAPI está instalado
pip install fastapi uvicorn

# Prueba el endpoint de health
curl http://localhost:8000/
```

### Frontend no conecta con backend

```bash
# Asegúrate de que VITE_API_URL es correcto
# En .env.development o .env.production
```

### GOOGLE_API_KEY error

```bash
# Obtén una clave en https://aistudio.google.com/apikey
# Configúrala en Railway → Variables
```

---

## 📝 Licencia

MIT © 2025 Cognitive Treasury

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📞 Soporte

- 📖 [Guía de Despliegue Railway](./RAILWAY_DEPLOYMENT_GUIDE.md)
- 🏠 [Setup de Desarrollo](./DEVELOPMENT_SETUP.md)
- 📚 [Docs API](http://localhost:8000/docs)
- 🚀 [Railway Docs](https://docs.railway.app)

---

**Hecho con ❤️ para optimizar decisiones financieras inteligentes**
