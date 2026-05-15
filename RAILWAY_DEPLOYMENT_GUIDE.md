# 🚀 Guía de Despliegue en Railway - Cognitive Treasury

## Prerequisitos

- Cuenta en [Railway.app](https://railway.app)
- Git y código pusheado en un repositorio (GitHub, GitLab, Bitbucket)
- Variables de entorno listas

---

## Paso 1: Conectar tu Repositorio a Railway

1. Ve a [railway.app](https://railway.app) e inicia sesión
2. Haz clic en **"+ New Project"**
3. Selecciona **"Deploy from GitHub"** (o tu proveedor)
4. Autoriza el acceso a tu repositorio
5. Selecciona el repositorio `cognitive-treasury`
6. Railway detectará automáticamente que es un proyecto Python (por el `Procfile`) y construirá el contenedor

---

## Paso 2: Configurar Variables de Entorno en Railway

Una vez que el proyecto esté creado en Railway:

1. Ve a la pestaña **"Variables"** en el dashboard del servicio
2. Añade las siguientes variables:

```
GOOGLE_API_KEY=tu_clave_gemini_aqui
VITE_API_URL=https://tu-dominio-railway.railway.app
WEIGHTS_STORAGE_PATH=/app/api/data/rlhf_weights.json
```

### 🔑 Cómo obtener cada variable:

**GOOGLE_API_KEY:**

- Ve a [Google AI Studio](https://aistudio.google.com/apikey)
- Crea una nueva clave de API
- Cópiala en Railway

**VITE_API_URL:**

- Aparecerá en Railway como "Public URL" cuando el deploy termine
- Será algo como: `https://cognitive-treasury-prod.railway.app`
- Cópiala tal cual

**WEIGHTS_STORAGE_PATH:**

- Usa el valor por defecto: `/app/api/data/rlhf_weights.json`

---

## Paso 3: Persistencia de Datos (RLHF Weights)

> ⚠️ **Importante:** Por defecto, Railway destruye los archivos locales en cada deploy. Para mantener tus pesos aprendidos (RLHF), debes configurar un volumen:

### Opción A: Volumen Local (Recomendado para inicio)

1. En Railway, ve a **Settings** → **Volumes**
2. Haz clic en **"+ Add Volume"**
3. Configura:
   - **Source Path:** `/app/api/data`
   - **Mount Path:** `/app/api/data`
4. Railway mantendrá el archivo entre deploys

### Opción B: Base de Datos PostgreSQL (Recomendado a largo plazo)

1. En Railway, haz clic en **"+ New Service"**
2. Selecciona **"PostgreSQL"**
3. Se creará automáticamente una base de datos con variables de entorno
4. Actualiza `api/rlhf_engine.py` para usar `psycopg2` y PostgreSQL en lugar del archivo JSON
5. Ejemplo:

```python
import psycopg2
import os

db_url = os.getenv("DATABASE_URL")
conn = psycopg2.connect(db_url)
# ... código para leer/escribir pesos en la base de datos
```

---

## Paso 4: Desplegar

Railway auto-detectará cambios en tu repositorio:

1. Haz push a tu rama principal (e.g., `main`)
2. Ve al dashboard de Railway
3. El deploy comenzará automáticamente
4. Verás logs en tiempo real en la pestaña **"Logs"**

### Comandos útiles:

```bash
# Ver logs en vivo
railway logs

# Redeploy manualmente (si necesitas)
railway up

# Ver variables de entorno
railway variables
```

---

## Paso 5: Verificar que todo funciona

1. Ve a la **Public URL** de tu proyecto en Railway
2. Deberías ver: `{"status": "El backend está funcionando..."}`
3. Abre el panel en el navegador: `https://tu-dominio-railway.app/`
4. Prueba el Chatbot y el Drag & Drop

---

## Troubleshooting

### "Module not found: api.index"

- Railway no encontró Python en la raíz
- **Solución:** Verifica que existe `api/index.py`

### Error 502 Bad Gateway

- Generalmente significa que el servidor FastAPI no levantó
- **Solución:** Revisa los logs (`railway logs`) y busca errores de importación

### Pesos RLHF se pierden después de cada deploy

- Los pesos se guardaban en el filesystem local (efímero)
- **Solución:** Configura un Volumen (Opción A arriba) o migra a PostgreSQL (Opción B)

### Frontend no conecta con Backend

- La variable `VITE_API_URL` no está configurada
- **Solución:** Ve a Variables en Railway y añade la URL pública correcta

---

## Monitoreo y Logs

En el dashboard de Railway:

- **Logs:** Pestaña "Logs" para ver qué está pasando
- **Metrics:** CPU, memoria, network
- **Alerts:** Configura alertas si el servicio falla

---

## Próximos pasos (Opcional)

1. **Custom Domain:**
   - Ve a Settings → Domains
   - Conecta un dominio personalizado (e.g., `treasury.tuempresa.com`)

2. **Staging Environment:**
   - Crea otro proyecto para pruebas
   - Deploya desde una rama `staging`

3. **Scheduled Tasks:**
   - Si necesitas un job que se ejecute cada cierto tiempo
   - Configura un Cron trigger en Railway

---

## Soporte

- 📖 Documentación de Railway: https://docs.railway.app
- 💬 Comunidad Discord: https://discord.gg/railway
- 🐛 Problemas: Revisa los logs en Railway dashboard

---

**¡Tu proyecto está listo para producción! 🎉**
