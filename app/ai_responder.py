import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

async def generar_respuesta(pregunta: str, info_producto: dict):
    titulo = info_producto.get("title", "producto")
    descripcion = info_producto.get("description", "sin descripción")
    precio = info_producto.get("price", "no disponible")

    mensaje = f"""
    Sos un asistente de ventas de MercadoLibre. 
    Respondé la pregunta del comprador de forma amable, clara y breve.
    
    Producto: {titulo}
    Precio: {precio}
    Descripción: {descripcion}
    
    Pregunta del comprador: {pregunta}
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=mensaje
    )

    return response.text