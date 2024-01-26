from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from atom.schemas.todo_schema import ToDoCreate, ToDoShow, ToDoUpdate
from atom.models.database import get_db
from atom.crud.todo_crud import (
    create_todo_by_user,
    get_all_todos_by_owner,
    update_todo_item_by_owner,
    get_todo_item_by_owner,
    delete_todo_item_by_owner,
)
from typing import List

router = APIRouter()

"""
    This module defines the routing for todo item-related operations in the application.
    It includes endpoints for creating, retrieving, updating, and deleting item.
"""


@router.post("/api/v1/users/{user_id}/todos")
def create_todo_item_by_user(
    user_id: str, item_data: ToDoCreate, db: Session = Depends(get_db)
):
    """
    Create a new todo item.
    This endpoint accepts user_id, todo item data and creates a new todo item in the database. If the specified user does not exist, it returns a 404 error.

    Parameters: user_id: unique user id,  item_data: An instance of ToDoCreate schema containing the data for the new todo item.
    db: A SQLAlchemy Session instance for database interaction.
    Returns:
        The newly created Todo item.
    """
    item = create_todo_by_user(user_id, item_data, db)
    if not item:
        raise HTTPException(status_code=404, detail="User not found")
    return item


@router.get("/api/v1/users/{user_id}/todos", response_model=List[ToDoShow])
def read_user_todos_items(user_id: str, db: Session = Depends(get_db)):
    """
    Retrieve all todo items for a specific user.
    This endpoint returns a list of todo items belonging to the specified user.
    Args:
        user_id: The unique identifier of the user whose todo items are to be retrieved.
        db: A SQLAlchemy Session instance for database interaction.
    Returns:
        A list of Todo items for the specified user.
    """
    return get_all_todos_by_owner(user_id, db)


@router.get("/api/v1/users/{user_id}/todos/{todo_id}")
def read_item_todo_by_user(user_id: str, todo_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a specific todo item created by a user.

    This endpoint fetches a single todo item specified by the todo ID and user ID. If the item is not found, it returns a 404 error.

    Args:
        user_id: The unique identifier of the user who owns the todo item.
        todo_id: The unique identifier of the todo item to retrieve.
        db: A SQLAlchemy Session instance for database interaction.

    Returns:
        A response indicating the todo item was successfully read.
    """
    read_one_item = get_todo_item_by_owner(user_id, todo_id, db)
    if not read_one_item:
        raise HTTPException(status_code=404, detail="Task not found")
    return read_one_item


@router.put("/api/v1/users/{user_id}/todos/{todo_id}", response_model=ToDoUpdate)
def update_todo_item_by_user(
    user_id: str, todo_id: str, todo_data: ToDoUpdate, db: Session = Depends(get_db)
):
    """
    Update a specific todo item owned by a user.
    This endpoint updates an existing todo item based on the provided data. If the todo item is not found or not owned by the user, it returns a 404 error.
    Args:
        user_id: The unique identifier of the user who owns the todo item.
        todo_id: The unique identifier of the todo item to update.
        todo_data: An instance of ToDoUpdate schema containing the updated data for the todo item.
        db: A SQLAlchemy Session instance for database interaction.

    Returns:
        The updated Todo item.
    """
    updated_todo_item = update_todo_item_by_owner(user_id, todo_id, todo_data, db)
    if not updated_todo_item:
        raise HTTPException(
            status_code=404, detail="Task not found or not owned by user"
        )
    return updated_todo_item


@router.delete("/api/v1/users/{user_id}/todos/{todo_id}")
def delete_todo_item_by_user(user_id: str, todo_id: str, db: Session = Depends(get_db)):
    """
    Delete a specific todo item owned by a user.

    This endpoint deletes a todo item specified by the todo ID and user ID. If the item is not found, it returns a 404 error.

    Args:
        user_id: The unique identifier of the user who owns the todo item.
        todo_id: The unique identifier of the todo item to delete.
        db: A SQLAlchemy Session instance for database interaction.

    Returns:
        A response indicating the todo item was successfully deleted.
    """
    deleted_todo_item = delete_todo_item_by_owner(user_id, todo_id, db)
    if not deleted_todo_item:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task was successfully deleted"}
