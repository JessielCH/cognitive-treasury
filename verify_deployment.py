#!/usr/bin/env python3
"""
🔍 Script de verificación pre-despliegue para Railway
Valida que todo esté configurado correctamente antes de desplegar a Railway.
"""

import os
import sys
import json
from pathlib import Path

def check_file_exists(filepath, description):
    """Verifica si un archivo existe."""
    exists = os.path.exists(filepath)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {filepath}")
    return exists

def check_env_file():
    """Verifica configuración de variables de entorno."""
    print("\n📦 Verificando variables de entorno...")
    
    env_example_exists = check_file_exists(".env.example", "Archivo .env.example")
    
    # Verificar que .env existe (o al menos .env.local)
    env_local_exists = os.path.exists(".env.local") or os.path.exists(".env")
    env_status = "✅" if env_local_exists else "⚠️ "
    print(f"{env_status} Archivo .env (local): {'.env' if os.path.exists('.env') else '.env.local' if os.path.exists('.env.local') else 'No encontrado'}")
    
    return env_example_exists

def check_backend_structure():
    """Verifica la estructura del backend."""
    print("\n🔧 Verificando estructura del backend...")
    
    files = [
        ("api/index.py", "Punto de entrada FastAPI"),
        ("api/chatbot.py", "Módulo Chatbot"),
        ("api/clustering.py", "Módulo Clustering"),
        ("api/rlhf_engine.py", "Motor RLHF"),
        ("api/multivariate.py", "Análisis Multivariante"),
        ("api/requirements.txt", "Dependencias Python"),
        ("requirements.txt", "Dependencias Python (raíz)"),
    ]
    
    all_exist = True
    for filepath, description in files:
        exists = check_file_exists(filepath, description)
        all_exist = all_exist and exists
    
    return all_exist

def check_frontend_structure():
    """Verifica la estructura del frontend."""
    print("\n⚛️  Verificando estructura del frontend...")
    
    files = [
        ("src/App.jsx", "Componente principal"),
        ("src/main.jsx", "Punto de entrada React"),
        ("src/components/Chatbot.jsx", "Componente Chatbot"),
        ("src/components/AuditBoard.jsx", "Componente AuditBoard"),
        ("src/components/Calendar.jsx", "Componente Calendar"),
        ("src/components/ImpactBoard.jsx", "Componente ImpactBoard"),
        ("package.json", "Dependencias npm"),
        ("vite.config.js", "Config Vite"),
    ]
    
    all_exist = True
    for filepath, description in files:
        exists = check_file_exists(filepath, description)
        all_exist = all_exist and exists
    
    return all_exist

def check_railway_config():
    """Verifica configuración de Railway."""
    print("\n🚀 Verificando configuración de Railway...")
    
    files = [
        ("Procfile", "Archivo Procfile"),
        ("railway.toml", "Configuración Railway"),
        ("Dockerfile", "Dockerfile (opcional)"),
    ]
    
    all_exist = True
    for filepath, description in files:
        exists = check_file_exists(filepath, description)
        all_exist = all_exist and exists
    
    return all_exist

def check_documentation():
    """Verifica documentación."""
    print("\n📚 Verificando documentación...")
    
    files = [
        ("README.md", "README principal"),
        ("RAILWAY_DEPLOYMENT_GUIDE.md", "Guía de despliegue"),
        ("DEVELOPMENT_SETUP.md", "Setup de desarrollo"),
    ]
    
    all_exist = True
    for filepath, description in files:
        exists = check_file_exists(filepath, description)
        all_exist = all_exist and exists
    
    return all_exist

def check_python_packages():
    """Verifica que los paquetes Python críticos se pueden importar."""
    print("\n🐍 Verificando paquetes Python...")
    
    packages = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("pandas", "Pandas"),
        ("sklearn", "Scikit-learn"),
        ("pydantic", "Pydantic"),
    ]
    
    all_available = True
    for package, description in packages:
        try:
            __import__(package)
            print(f"✅ {description} está instalado")
        except ImportError:
            print(f"❌ {description} NO está instalado")
            print(f"   Instala con: pip install {package}")
            all_available = False
    
    return all_available

def check_git_setup():
    """Verifica que git está configurado."""
    print("\n📦 Verificando Git...")
    
    git_exists = os.path.exists(".git")
    status = "✅" if git_exists else "❌"
    print(f"{status} Repositorio Git: {'.git encontrado' if git_exists else '.git NO encontrado'}")
    
    return git_exists

def main():
    """Función principal."""
    print("=" * 60)
    print("🔍 Cognitive Treasury - Pre-deployment Verification")
    print("=" * 60)
    
    checks = [
        ("Archivos de Entorno", check_env_file),
        ("Estructura Backend", check_backend_structure),
        ("Estructura Frontend", check_frontend_structure),
        ("Configuración Railway", check_railway_config),
        ("Documentación", check_documentation),
        ("Paquetes Python", check_python_packages),
        ("Configuración Git", check_git_setup),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error en {name}: {e}")
            results.append((name, False))
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📋 RESUMEN")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\n📊 {passed}/{total} verificaciones completadas")
    
    if passed == total:
        print("\n✅ ¡Todo está listo! Puedes desplegar a Railway.")
        print("\nProximos pasos:")
        print("1. git add .")
        print("2. git commit -m 'Preparado para Railway'")
        print("3. git push origin main")
        print("4. Ve a https://railway.app y conecta tu repositorio")
        return 0
    else:
        print(f"\n❌ Hay {total - passed} problema(s) a resolver antes de desplegar.")
        print("\nPara más información, lee:")
        print("- DEVELOPMENT_SETUP.md")
        print("- RAILWAY_DEPLOYMENT_GUIDE.md")
        return 1

if __name__ == "__main__":
    sys.exit(main())
