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