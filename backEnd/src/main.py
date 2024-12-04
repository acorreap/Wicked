from fastapi import FastAPI
from .api import api_router
from .core.events import startup_event, shutdown_event


app = FastAPI()

app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)


app.include_router(api_router)
