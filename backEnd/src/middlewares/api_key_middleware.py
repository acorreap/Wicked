from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from typing import List
from ..auth.service.API_key_service import ApiKeyService
from ..auth.schemas.API_key_schema import ApiKeySchema

class APIKeyMiddleware:
    def __init__(self, app: FastAPI, exempt_routes: List[str] = None):
        """
        Middleware para validar API Key.
        :param app: La aplicación FastAPI.
        :param exempt_routes: Lista de rutas que no requieren validación.
        """
        self.app = app
        self.service = ApiKeyService()
        self.exempt_routes = exempt_routes or []

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive, send)
            path = request.url.path

            # Permitir acceso sin validación si la ruta está en las rutas exentas
            if path in self.exempt_routes:
                await self.app(scope, receive, send)
                return

            # Validar la API Key
            api_key = request.headers.get("x-api-key")
            if not api_key:
                response = JSONResponse(
                    {"detail": "no encontrado"}, status_code=401
                )
                await response(scope, receive, send)
                return
            
            if not self.service.valid_api_key(api_key):
                response = JSONResponse(
                    {"detail": "API Key no válida o expirada"}, status_code=403
                )
                await response(scope, receive, send)
                return

        # Continuar con la solicitud si pasa la validación
        await self.app(scope, receive, send)
