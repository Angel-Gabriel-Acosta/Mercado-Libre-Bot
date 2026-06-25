import httpx
import os
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from app.database import registrar_usuario, login_usuario, guardar_ml_token, SessionLocal, Usuario

load_dotenv()

router = APIRouter()

APP_ID = os.getenv("ML_APP_ID")
SECRET_KEY = os.getenv("ML_SECRET_KEY")
REDIRECT_URI = os.getenv("ML_REDIRECT_URI")

@router.post("/registro")
async def registro(request: Request):
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    
    usuario = registrar_usuario(email, password)
    if not usuario:
        return RedirectResponse("/login?error=El email ya está registrado", status_code=303)
    
    request.session["user_id"] = usuario.id
    return RedirectResponse("/", status_code=303)

@router.post("/login")
async def login_post(request: Request):
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    
    usuario = login_usuario(email, password)
    if not usuario:
        return RedirectResponse("/login?error=Email o contraseña incorrectos", status_code=303)
    
    request.session["user_id"] = usuario.id
    return RedirectResponse("/", status_code=303)

@router.get("/ml/conectar")
def ml_conectar(request: Request):
    url = (
        f"https://auth.mercadolibre.com.ar/authorization"
        f"?response_type=code"
        f"&client_id={APP_ID}"
        f"&redirect_uri={REDIRECT_URI}"
    )
    return RedirectResponse(url)

@router.get("/callback")
async def callback(code: str, request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse("/login")

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
    ml_user_id = tokens.get("user_id")

    async with httpx.AsyncClient() as client:
        user_response = await client.get(
            f"https://api.mercadolibre.com/users/{ml_user_id}",
            headers={"Authorization": f"Bearer {access_token}"}
        )
    user_data = user_response.json()
    nickname = user_data.get("nickname", "")

    guardar_ml_token(user_id, ml_user_id, access_token, refresh_token, nickname)

    return RedirectResponse("/")

@router.get("/desconectar")
def desconectar(request: Request):
    request.session.clear()
    return RedirectResponse("/login")