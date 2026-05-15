#!/bin/bash
# Script de inicialización para Railway
# Asegura que los directorios necesarios existan

echo "🚀 Inicializando Cognitive Treasury..."

# Crear directorio de datos para pesos RLHF
mkdir -p api/data

# Instalar dependencias de Python
echo "📦 Instalando dependencias de Python..."
pip install --no-cache-dir -r requirements.txt

# Instalar dependencias de Node (opcional para el frontend)
echo "📦 Instalando dependencias de Node..."
npm ci

# Compilar el frontend (opcional, si quieres servir archivos estáticos)
# echo "🏗️  Compilando frontend..."
# npm run build

echo "✅ Inicialización completada."
