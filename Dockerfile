# Stage 1: Build Frontend
FROM node:20-alpine AS frontend-builder

WORKDIR /app

# Copiar archivos de dependencias
COPY package.json package-lock.json ./

# Instalar dependencias
RUN npm ci

# Copiar código fuente del frontend
COPY src ./src
COPY public ./public
COPY vite.config.js tailwind.config.js postcss.config.js index.html ./

# Compilar el build de production
RUN npm run build

# Stage 2: Build Backend + Servidor ASGI
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt
COPY requirements.txt ./

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código del backend
COPY api ./api

# Copiar el build del frontend desde el stage anterior
COPY --from=frontend-builder /app/dist ./api/static

# Crear directorio para datos persistentes
RUN mkdir -p /app/api/data

# Exponer puerto
EXPOSE 8000

# Comando de inicio con expansión de variable de entorno
CMD ["sh", "-c", "uvicorn api.index:app --host 0.0.0.0 --port ${PORT:-8000}"]
