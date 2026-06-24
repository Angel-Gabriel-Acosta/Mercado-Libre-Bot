from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.auth import router as auth_router
from app.webhook import router as webhook_router
from app.database import obtener_primer_usuario

app = FastAPI(title="ML Bot")
templates = Jinja2Templates(directory="app/templates")

app.include_router(auth_router, prefix="/auth")
app.include_router(webhook_router, prefix="/webhook")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    usuario = obtener_primer_usuario()
    return templates.TemplateResponse(request, "index.html", {"usuario": usuario})