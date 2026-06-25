import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

async def generar_respuesta(pregunta: str, info_producto: dict, tono: str = "amigable"):
    titulo = info_producto.get("title", "producto")
    precio = info_producto.get("price", "no disponible")
    descripcion = info_producto.get("description", "sin descripción")

    tonos = {
        "formal": "Respondé de forma formal y profesional.",
        "amigable": "Respondé de forma amigable y cercana.",
        "breve": "Respondé de forma muy corta y directa, máximo 2 oraciones."
    }

    instruccion_tono = tonos.get(tono, tonos["amigable"])

    mensaje = f"""
    Sos un asistente de ventas de MercadoLibre. {instruccion_tono}
    
    Producto: {titulo}
    Precio: ${precio}
    Descripción: {descripcion}
    
    Pregunta del comprador: {pregunta}
    """

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": mensaje}]
    )

    return response.content[0].text