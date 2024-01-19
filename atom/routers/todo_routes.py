from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from atom.schemas.todo_schema import ToDoCreate, ToDoShow, ToDoUpdate
from atom.models.database import get_db
from atom.crud.todo_crud import (
    create_todo_by_owner,
    get_all_todos_by_owner,
    update_todo_item_by_owner,
    get_todo_item_and_owner,
    delete_todo_item_by_owner,
)
from typing import List

router = APIRouter()


@router.post("/todos/")
def create_item_api(item_data: ToDoCreate, db: Session = Depends(get_db)):
    item = create_todo_by_owner(item_data, db)
    if not item:
        raise HTTPException(status_code=404, detail="User not found")
    return item


@router.get("/users/{user_id}/todos", response_model=List[ToDoShow])
def read_user_todos(user_id: str, db: Session = Depends(get_db)):
    return get_all_todos_by_owner(user_id, db)


@router.get("/users/{user_id}/todos/{todo_id}")
def read_item_todo_by_user(user_id: str, todo_id: str, db: Session = Depends(get_db)):
    read_one_item = get_todo_item_and_owner(user_id, todo_id, db)
    if not read_one_item:
        return HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task is successfully read it"}


@router.put("/users/{user_id}/todos/{todo_id}", response_model=ToDoUpdate)
def update_user_todo_item(
    user_id: str, todo_id: str, todo_data: ToDoUpdate, db: Session = Depends(get_db)
):
    updated_todo_item = update_todo_item_by_owner(user_id, todo_id, todo_data, db)
    if not updated_todo_item:
        return HTTPException(
            status_code=404, detail="Task not found or not owned by user"
        )
    return {"message": "Task was successfully updated"}


@router.delete("/users/{user_id}/todos/{todo_id}")
def delete_item_todo_by_user(user_id: str, todo_id: str, db: Session = Depends(get_db)):
    deleted_todo_item = delete_todo_item_by_owner(user_id, todo_id, db)
    if not deleted_todo_item:
        return HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task was successfully deleted"}
