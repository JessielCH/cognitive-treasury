# 🏠 Guía de Desarrollo Local - Cognitive Treasury

## Configuración del Entorno Local

Antes de desplegar a Railway, asegúrate de que todo funciona localmente.

### Prerequisitos

- **Node.js** 18+ y npm (para el frontend)
- **Python** 3.10+ (para el backend)
- **Git**
- Un terminal o PowerShell

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/cognitive-treasury.git
cd cognitive-treasury
```

### Paso 2: Configurar el Backend (Python)

#### Windows (PowerShell)

```powershell
# Crear y activar entorno virtual
python -m venv venv
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
pip install -r api/requirements.txt

# (Opcional) Crear archivos de datos
mkdir -p api/data
```

#### macOS / Linux

```bash
# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
pip install -r api/requirements.txt

# (Opcional) Crear archivos de datos
mkdir -p api/data
```

### Paso 3: Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env.local

# Editar .env.local y agregar:
# GOOGLE_API_KEY=tu_clave_gemini_aqui
```

### Paso 4: Configurar el Frontend (Node.js)

```bash
# Instalar dependencias
npm install

# Opcional: Construir el frontend
npm run build
```

### Paso 5: Ejecutar el Proyecto Localmente

#### Terminal 1: Backend (FastAPI)

```powershell
# Windows
.\venv\Scripts\Activate.ps1
uvicorn api.index:app --reload --host 0.0.0.0 --port 8000

# macOS / Linux
source venv/bin/activate
uvicorn api.index:app --reload --host 0.0.0.0 --port 8000
```

El backend estará disponible en: http://localhost:8000

**Endpoints útiles:**

- 📖 Docs interactivos: http://localhost:8000/docs
- 🧪 Prueba alternativa: http://localhost:8000/redoc

#### Terminal 2: Frontend (Vite Dev Server)

```bash
npm run dev
```

El frontend estará disponible en: http://localhost:5173

---

## Pruebas Locales

### 1. Verificar que el Backend está funcionando

```bash
curl http://localhost:8000/
# Respuesta esperada:
# {"status":"El backend está funcionando..."}
```

### 2. Probar endpoint de facturas

```bash
curl http://localhost:8000/api/invoices
# Deberías ver un JSON con facturas y pesos actuales
```

### 3. Probar el Chatbot

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"¿Cuál es el monto total?", "calendar_state":{}}'
```

### 4. Abrir la UI en el navegador

- Ve a http://localhost:5173
- Prueba:
  - 📅 Drag & drop en el Calendario
  - 💬 Chat con el Copiloto IA
  - 📊 Visualización de datos en ImpactBoard
  - 🔍 Auditoría de anomalías

---

## Estructura de Carpetas

```
cognitive-treasury/
├── api/                          # Backend FastAPI
│   ├── index.py                 # Punto de entrada (app = FastAPI())
│   ├── chatbot.py               # Integración Gemini
│   ├── clustering.py            # DBSCAN
│   ├── multivariate.py          # Análisis PCA
│   ├── rlhf_engine.py           # Motor de aprendizaje
│   ├── rlhf_weights.json        # Pesos aprendidos (generado)
│   ├── data/                    # Datos persistentes
│   └── requirements.txt         # Deps de Python
│
├── src/                          # Frontend React
│   ├── components/
│   │   ├── AuditBoard.jsx       # Auditoría + XAI
│   │   ├── Calendar.jsx         # Calendario drag & drop
│   │   ├── Chatbot.jsx          # Asistente IA
│   │   └── ImpactBoard.jsx      # Gráficos
│   ├── App.jsx
│   ├── main.jsx
│   ├── index.css
│   └── App.css
│
├── public/                       # Archivos estáticos
├── Procfile                      # Instrucciones para Railway/Heroku
├── railway.toml                  # Config de Railway
├── Dockerfile                    # Build personalizado (opcional)
├── vite.config.js               # Config de Vite
├── tailwind.config.js           # Config de Tailwind
├── package.json                 # Deps de Node
├── requirements.txt             # Deps de Python (global)
└── .env.example                 # Plantilla de env vars
```

---

## Troubleshooting Local

### Error: "Module not found: api.rlhf_engine"

**Solución:** Verifica que estés en la carpeta raíz del proyecto y que el venv está activado.

```bash
cd cognitive-treasury
source venv/bin/activate  # o .\venv\Scripts\Activate.ps1 en Windows
```

### Error: "GOOGLE_API_KEY not found"

**Solución:** Crea un archivo `.env.local` con:

```
GOOGLE_API_KEY=your_key_here
```

### Frontend no ve el Backend

**Solución:** Asegúrate de que:

1. Backend está corriendo en `http://localhost:8000`
2. Frontend está en `http://localhost:5173`
3. CORS está habilitado en el backend (ya está configurado en `api/index.py`)

### Puerto 8000 ya está en uso

**Solución:** Usa otro puerto:

```bash
uvicorn api.index:app --host 0.0.0.0 --port 8001
```

Entonces cambia `VITE_API_URL` en `.env.development`:

```
VITE_API_URL=http://localhost:8001
```

---

## Deployment a Railway

Cuando estés listo para subir a producción:

1. Haz commit de tus cambios:

```bash
git add .
git commit -m "Preparar para Railway"
git push origin main
```

2. Ve a https://railway.app y sigue la guía [RAILWAY_DEPLOYMENT_GUIDE.md](./RAILWAY_DEPLOYMENT_GUIDE.md)

---

## Recursos Útiles

- 📚 [FastAPI Documentation](https://fastapi.tiangolo.com/)
- ⚛️ [React Documentation](https://react.dev/)
- ⚡ [Vite Documentation](https://vitejs.dev/)
- 🚀 [Railway Documentation](https://docs.railway.app)
- 🌐 [Python-dotenv](https://python-dotenv.readthedocs.io/)

---

**¡Listo para empezar! Happy coding! 🎉**
