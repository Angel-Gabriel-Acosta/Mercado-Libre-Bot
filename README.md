Bot de Mercado Libre con IA Grupo 12

Básicamente es un bot que conectás a tu cuenta de MercadoLibre y se encarga de responder las preguntas de los compradores solo, usando IA.

Que hace?

Cuando un comprador hace una pregunta en alguna de tus publicaciones, el bot la recibe, lee la info del producto y genera una respuesta automática.

Por ahora tiene estas funcionalidades:
- Conectás tu cuenta de ML con un click
- El bot responde preguntas automáticamente con IA
- Podés ver todas las preguntas y respuestas en un panel
- Antes de enviar podés revisar y editar la respuesta si querés
- Elegís el tono: formal, amigable o corto
- Estadísticas básicas de cuánto está respondiendo el bot
- Notificaciones por email cuando llega algo importante

Tecnologías usadas

- Python con FastAPI para el backend
- SQLite para guardar los datos
- Google Gemini para la IA
- La API oficial de MercadoLibre
- ngrok para desarrollo local

Cómo correrlo

```bash
# Clonar el repo
git clone https://github.com/Angel-Gabriel-Acosta/Mercado-Libre-Bot.git
cd Mercado-Libre-Bot

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env con tus credenciales (ver ejemplo abajo)
# Correr el servidor
uvicorn app.main:app --reload
```

## Variables de entorno

Crear un archivo `.env` en la raíz con esto:

ML_APP_ID=tu_app_id

ML_SECRET_KEY=tu_secret_key

ML_REDIRECT_URI=tu_redirect_uri

GEMINI_API_KEY=tu_api_key