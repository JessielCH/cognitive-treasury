import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Usaremos Gemini 1.5 Flash por su velocidad y capacidad de contexto
model = genai.GenerativeModel('gemini-2.5-flash')

def ask_treasury_copilot(user_message: str, calendar_context: dict) -> str:
    """Envía la pregunta a Gemini adjuntando el estado actual del flujo de caja."""
    
    # Preparamos el contexto para que Gemini entienda qué está viendo el usuario
    context_str = json.dumps(calendar_context, indent=2)
    
    prompt = f"""
    Eres el "Copiloto de Tesorería Cognitiva", un asistente experto en flujos de caja y priorización de liquidez.
    El usuario está viendo un calendario interactivo con facturas asignadas por días.
    
    ESTADO ACTUAL DEL CALENDARIO (JSON):
    {context_str}
    
    REGLAS DE TU COMPORTAMIENTO:
    1. Si te piden "semaforizar", clasifica las facturas así: ROJO (Criticidad 4-5 o Antigüedad > 60 días), AMARILLO (Criticidad 3 o Antigüedad 30-60 días), VERDE (Resto).
    2. Si te preguntan por gastos diarios, suma los montos ("monto") de cada factura por día (Lunes, Martes, etc.) y da el total.
    3. Si te preguntan "qué pasa si este escenario se hace real", analiza la liquidez, destaca qué pagos críticos quedaron para el viernes y si hay riesgo de mora en facturas rojas.
    4. Sé directo, profesional, usa viñetas para ser claro y responde siempre en español.
    
    PREGUNTA DEL GERENTE DE FINANZAS:
    {user_message}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error de conexión con el núcleo cognitivo (Gemini): {str(e)}"