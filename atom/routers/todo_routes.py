from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from atom.schemas.todo_schema import ToDoCreate, ToDoShow, ToDoUpdate
from atom.models.database import get_db
from atom.crud.todo_crud import create_todo_by_owner, get_all_todos_by_owner, update_todo_item_by_owner
from typing import List

router = APIRouter()


@router.post("/todo")
def create_item_api(item_data: ToDoCreate, db: Session = Depends(get_db)):
    item = create_todo_by_owner(item_data, db)
    if not item:
        raise HTTPException(status_code=404, detail="User not found")
    return item


@router.get("/users/{user_id}/todos", response_model=List[ToDoShow])
def read_user_todos(user_id: str, db: Session = Depends(get_db)):
    return get_all_todos_by_owner(user_id, db)


@router.put("/users/{user_id}/update_todo/{todo_id}", response_model=ToDoUpdate)
def update_user_todo_item(user_id: str, todo_id: str, todo_data: ToDoUpdate, db: Session = Depends(get_db)):
    updated_todo_item = update_todo_item_by_owner(user_id, todo_id, todo_data, db)
    if not updated_todo_item:
        return HTTPException(status_code=404, detail="Task not found or not owned by user")
    return updated_todo_item
