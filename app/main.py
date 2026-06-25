from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel
from app.auth import router as auth_router
from app.webhook import router as webhook_router
from app.database import obtener_usuario_por_id, obtener_config, guardar_config, obtener_historial, guardar_historial, obtener_estadisticas
from app.ml_client import get_publicaciones
from app.ai_responder import generar_respuesta

app = FastAPI(title="ML Bot")
app.add_middleware(SessionMiddleware, secret_key="mlbot-secret-key-2024")
templates = Jinja2Templates(directory="app/templates")

app.include_router(auth_router, prefix="/auth")
app.include_router(webhook_router, prefix="/webhook")

async def get_usuario(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return obtener_usuario_por_id(user_id)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    usuario = await get_usuario(request)
    if not usuario:
        return RedirectResponse("/login")
    publicaciones = []
    if usuario.ml_access_token:
        try:
            publicaciones = await get_publicaciones(usuario.ml_user_id, usuario.ml_access_token)
        except:
            publicaciones = []
    return templates.TemplateResponse(request, "index.html", {
        "usuario": usuario,
        "publicaciones": publicaciones
    })

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    error = request.query_params.get("error", "")
    return templates.TemplateResponse(request, "login.html", {"error": error})

@app.get("/registro", response_class=HTMLResponse)
async def registro_page(request: Request):
    error = request.query_params.get("error", "")
    return templates.TemplateResponse(request, "registro.html", {"error": error})

@app.get("/configuracion", response_class=HTMLResponse)
async def configuracion_page(request: Request):
    usuario = await get_usuario(request)
    if not usuario:
        return RedirectResponse("/login")
    config = obtener_config(usuario.id)
    return templates.TemplateResponse(request, "configuracion.html", {"usuario": usuario, "config": config, "guardado": False})

@app.post("/configuracion", response_class=HTMLResponse)
async def configuracion_guardar(request: Request):
    usuario = await get_usuario(request)
    if not usuario:
        return RedirectResponse("/login")
    form = await request.form()
    tono = form.get("tono", "amigable")
    info_extra = form.get("info_extra", "")
    bot_activo = "bot_activo" in form
    modo_revision = "modo_revision" in form
    guardar_config(usuario.id, tono, info_extra, bot_activo, modo_revision)
    config = obtener_config(usuario.id)
    return templates.TemplateResponse(request, "configuracion.html", {"usuario": usuario, "config": config, "guardado": True})

@app.get("/demo", response_class=HTMLResponse)
async def demo_page(request: Request):
    usuario = await get_usuario(request)
    if not usuario:
        return RedirectResponse("/login")
    config = obtener_config(usuario.id)
    return templates.TemplateResponse(request, "demo.html", {"usuario": usuario, "config": config})

class DemoRequest(BaseModel):
    pregunta: str
    producto: str
    precio: str
    descripcion: str

@app.post("/demo/responder")
async def demo_responder(data: DemoRequest, request: Request):
    usuario = await get_usuario(request)
    if not usuario:
        return {"respuesta": "No autorizado"}
    config = obtener_config(usuario.id)
    info_producto = {
        "title": data.producto,
        "price": data.precio,
        "description": data.descripcion
    }
    respuesta = await generar_respuesta(data.pregunta, info_producto, tono=config.tono)
    guardar_historial(usuario.id, data.pregunta, respuesta, data.producto)
    return {"respuesta": respuesta}

@app.get("/historial", response_class=HTMLResponse)
async def historial_page(request: Request):
    usuario = await get_usuario(request)
    if not usuario:
        return RedirectResponse("/login")
    historial = obtener_historial(usuario.id)
    return templates.TemplateResponse(request, "historial.html", {"usuario": usuario, "historial": historial})

@app.get("/estadisticas", response_class=HTMLResponse)
async def estadisticas_page(request: Request):
    usuario = await get_usuario(request)
    if not usuario:
        return RedirectResponse("/login")
    stats = obtener_estadisticas(usuario.id)
    stats["usuario"] = usuario
    return templates.TemplateResponse(request, "estadisticas.html", stats)