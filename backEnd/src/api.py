from fastapi import APIRouter, Depends
from .auth.controller.AuthController import user_router


api_router = APIRouter()

api_router.include_router(user_router, prefix="/auth", tags=["auth"])