import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def _llamar_gemini(prompt: str) -> str:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"No se pudo obtener el pronóstico: {str(e)}"

def pronostico_productos(datos: list) -> str:
    prompt = f"""
Eres un analista de datos para un restaurante boliviano llamado Chicken Lindo.
Analiza los siguientes productos más vendidos y genera EXACTAMENTE 3 pronósticos.

Datos de productos (nombre, cantidad vendida, ingresos en Bs.):
{datos}

Genera 3 pronósticos numerados sobre tendencias de ventas, productos con mayor 
potencial y recomendaciones de stock. Máximo 2 líneas por pronóstico.
Sé específico con los datos. No uses markdown ni asteriscos.
"""
    return _llamar_gemini(prompt)

def pronostico_clientes(datos: list) -> str:
    prompt = f"""
Eres un analista de datos para un restaurante boliviano llamado Chicken Lindo.
Analiza el historial de compras por cliente y genera EXACTAMENTE 3 pronósticos.

Datos de clientes (nombre, número de tickets, total gastado en Bs.):
{datos}

Genera 3 pronósticos numerados sobre fidelización de clientes, clientes con mayor 
valor y comportamiento de compra. Máximo 2 líneas por pronóstico.
Sé específico con los datos. No uses markdown ni asteriscos.
"""
    return _llamar_gemini(prompt)

def pronostico_ventas(datos: list) -> str:
    prompt = f"""
Eres un analista de datos para un restaurante boliviano llamado Chicken Lindo.
Analiza las ventas diarias y genera EXACTAMENTE 3 pronósticos.

Datos de ventas por día (fecha, total vendido en Bs., número de tickets):
{datos}

Genera 3 pronósticos numerados sobre tendencia de ingresos, días de mayor demanda 
y proyección de ventas futuras. Máximo 2 líneas por pronóstico.
Sé específico con los datos. No uses markdown ni asteriscos.
"""
    return _llamar_gemini(prompt)