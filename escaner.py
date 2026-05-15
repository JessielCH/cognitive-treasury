import os
import google.generativeai as genai
from dotenv import load_dotenv

# Cargar la API Key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("Buscando modelos gratuitos compatibles con tu API Key...\n")

# Preguntarle a Google qué modelos tienes habilitados para chat
modelos_validos = []
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        # Limpiamos el texto para que te dé el nombre exacto
        nombre_limpio = m.name.replace("models/", "")
        modelos_validos.append(nombre_limpio)
        print(f"✅ Habilitado: {nombre_limpio}")

print("\nCopia UNO de los nombres de arriba (ej. 'gemini-1.5-flash-latest' o 'gemini-2.5-flash')")