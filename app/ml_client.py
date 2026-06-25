import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def get_item_info(item_id: str, access_token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.mercadolibre.com/items/{item_id}",
            headers={"Authorization": f"Bearer {access_token}"}
        )
    return response.json()

async def get_publicaciones(user_id: str, access_token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.mercadolibre.com/users/{user_id}/items/search",
            headers={"Authorization": f"Bearer {access_token}"}
        )
    items = response.json()
    ids = items.get("results", [])
    
    publicaciones = []
    for item_id in ids[:5]:
        item_response = await client.get(
            f"https://api.mercadolibre.com/items/{item_id}",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        publicaciones.append(item_response.json())
    
    return publicaciones

async def responder_pregunta(question_id: str, respuesta: str, access_token: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.mercadolibre.com/answers",
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "question_id": question_id,
                "text": respuesta
            }
        )
    return response.json()