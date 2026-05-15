# Información de Despliegue en Railway

# Este archivo contiene la configuración recomendada para Railway

## Configuración de Plataforma

**Platform:** Railway.app
**Build Method:** Buildpack (Python + Node.js) o Docker
**Environment:** Production

## Archivos Clave de Configuración

- `Procfile` - Define el comando de inicio para Railway
- `railway.toml` - Configuración específica de Railway
- `Dockerfile` - Dockerfile opcional para builds más personalizados
- `.env.example` - Variables de entorno necesarias

## Estructura del Proyecto

```
cognitive-treasury/
├── api/                    # Backend FastAPI
│   ├── index.py           # Punto de entrada principal
│   ├── chatbot.py         # Integración con Gemini
│   ├── clustering.py      # Análisis de clustering
│   ├── multivariate.py    # Análisis multivariante
│   ├── rlhf_engine.py     # Motor de aprendizaje RLHF
│   ├── data/              # 📁 Directorio para datos persistentes
│   └── rlhf_weights.json  # (Generado dinámicamente)
├── src/                    # Frontend React + Vite
│   ├── components/        # Componentes React
│   │   ├── AuditBoard.jsx
│   │   ├── Calendar.jsx
│   │   ├── Chatbot.jsx
│   │   └── ImpactBoard.jsx
│   └── ...
├── Procfile               # Instrucciones para Railway
├── railway.toml           # Configuración de Railway
├── Dockerfile             # (Opcional) Build personalizado
└── requirements.txt       # Dependencias de Python
```

## Comandos para el Despliegue

### Desde CLI de Railway

```bash
# Instalar CLI de Railway
npm i -g @railway/cli

# Login
railway login

# Conectar al proyecto
railway link

# Ver logs
railway logs

# Variables de entorno
railway variables

# Deploy manual
railway up
```

### Git Push (Auto-deploy)

```bash
git add .
git commit -m "Preparar para Railway"
git push origin main
```

## Próximos Pasos Post-Despliegue

1. ✅ Verifica que el backend está activo: `https://tu-railway-url/docs`
2. ✅ Prueba los endpoints: `/api/invoices`, `/api/chat`, `/api/audit-anomalies`
3. ✅ Configura el VITE_API_URL en el dashboard de Railway
4. ✅ Configura un volumen para persistencia de RLHF weights
5. ✅ (Opcional) Conecta PostgreSQL o Redis para estado persistente

## Referencias

- **Railway Docs:** https://docs.railway.app
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **Vite Docs:** https://vitejs.dev/
- **RLHF Pattern:** Feedback basado en preferencias humanas
