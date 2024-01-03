from fastapi import APIRouter
from .user_routes import router as user_routes

api_router = APIRouter()
api_router.include_router(user_routes, tags=["user"])
