from fastapi import APIRouter
from .user_routes import router as user_routes
from .todo_routes import router as todo_routes

api_router = APIRouter()
api_router.include_router(user_routes, tags=["User"])
api_router.include_router(todo_routes, tags=["ToDoItems"])
