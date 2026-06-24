import asyncio
from app.ai_responder import generar_respuesta

async def main():
    producto = {
        "title": "iPhone 13 128GB Negro",
        "price": 500000,
        "description": "iPhone 13 nuevo en caja, sin uso, garantía oficial de 1 año."
    }
    
    pregunta = "¿El celular viene con cargador?"
    
    print("Pregunta:", pregunta)
    print("Generando respuesta...")
    
    respuesta = await generar_respuesta(pregunta, producto)
    
    print("Respuesta de la IA:", respuesta)

asyncio.run(main())