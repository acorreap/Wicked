from fastapi import FastAPI
from .api import api_router
from .core.events import startup_event, shutdown_event
from .middlewares.api_key_middleware import APIKeyMiddleware

app = FastAPI()

app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

sin_ruta = ["/apiKey/create"]

app.add_middleware(APIKeyMiddleware)
app.include_router(api_router)
