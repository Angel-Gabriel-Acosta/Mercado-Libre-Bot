import httpx
import os
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from app.database import guardar_usuario

load_dotenv()

router = APIRouter()

APP_ID = os.getenv("ML_APP_ID")
SECRET_KEY = os.getenv("ML_SECRET_KEY")
REDIRECT_URI = os.getenv("ML_REDIRECT_URI")

@router.get("/login")
def login():
    url = (
        f"https://auth.mercadolibre.com.ar/authorization"
        f"?response_type=code"
        f"&client_id={APP_ID}"
        f"&redirect_uri={REDIRECT_URI}"
    )
    return RedirectResponse(url)

@router.get("/callback")
async def callback(code: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.mercadolibre.com/oauth/token",
            data={
                "grant_type": "authorization_code",
                "client_id": APP_ID,
                "client_secret": SECRET_KEY,
                "code": code,
                "redirect_uri": REDIRECT_URI,
            },
        )

    tokens = response.json()
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")
    user_id = tokens.get("user_id")

    # Buscar nickname del usuario
    async with httpx.AsyncClient() as client:
        user_response = await client.get(
            f"https://api.mercadolibre.com/users/{user_id}",
            headers={"Authorization": f"Bearer {access_token}"}
        )
    user_data = user_response.json()
    nickname = user_data.get("nickname", "")

    # Guardar en base de datos
    guardar_usuario(user_id, access_token, refresh_token, nickname)

    # Redirigir al panel
    return RedirectResponse("/")