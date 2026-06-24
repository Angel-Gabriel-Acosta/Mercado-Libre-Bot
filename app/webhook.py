from fastapi import APIRouter
from app.ml_client import get_item_info, responder_pregunta
from app.ai_responder import generar_respuesta
import os

router = APIRouter()

ACCESS_TOKEN = os.getenv("ML_ACCESS_TOKEN")

@router.post("/preguntas")
async def recibir_pregunta(data: dict):
    try:
        resource = data.get("resource", "")
        question_id = resource.split("/")[-1]

        # Por ahora simulamos la pregunta
        pregunta_texto = "¿Hacen envíos al interior?"
        item_id = "MLA1417214745"

        info_producto = await get_item_info(item_id, ACCESS_TOKEN)
        respuesta = await generar_respuesta(pregunta_texto, info_producto)

        print(f"Pregunta: {pregunta_texto}")
        print(f"Respuesta IA: {respuesta}")

        return {"status": "ok", "respuesta": respuesta}

    except Exception as e:
        return {"status": "error", "detalle": str(e)}