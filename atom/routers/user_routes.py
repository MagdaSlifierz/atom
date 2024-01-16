from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from atom.schemas.user_schema import UserCreate, ShowUser, UserUpdate
from atom.models.database import get_db
from atom.crud.user_crud import (
    create_new_user,
    get_user_by_id,
    read_all_users,
    update_user,
    delete_user,
)
from typing import List

"""
    This module defines the routing for user-related operations in the application.
    It includes endpoints for creating, retrieving, updating, and deleting user data.
"""
router = APIRouter()


# UserCreate schema will validate that it has a email in proper format, and a password
@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user in the system.

    This endpoint takes user data, creates a new user record in the database,
    and returns the created user information.

    Parameters:
    - user (UserCreate): A Pydantic model representing the user data for the new user.
    - db (Session, optional): The database session dependency.
    Returns:
    - A JSON representation of the created user.
    """
    user = create_new_user(user, db)
    return user


@router.get("/user/all", response_model=List[ShowUser])
def get_all_users(db: Session = Depends(get_db)):
    """
    Retrieve a list of all users.

    This endpoint fetches and return a list of all users in the sytem
    Parameters:
    - db (Session, optional): The database session dependency.
    Returns:
    - A list of users, ech represented as a JSON object.
    """
    user_all = read_all_users(db)
    return user_all


@router.get("/user/{user_id}")
def get_user(user_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a specific user by their user ID.

    Parameters:
    - user_id (UUID4): The unique identifier of the user.
    - db (Session, optional): The database session dependency.
    Returns:
    - A JSON representation of the user if found.
    Raises:
    - HTTPException: 404 error if the user is not found.
    """
    user = get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/user/update/{user_id}")
def update_user_by_id(
    user_id: str, user_update: UserUpdate, db: Session = Depends(get_db)
):
    """
    Update an existing user's information.

    This endpoint updates the data of the user specified by the user_id with the provided data.

    Parameters:
    - user_id (UUID4): The unique identifier of the user to be updated.
    - user_update (UserUpdate): A Pydantic model representing the data to be updated.
    - db (Session, optional): The database session dependency.
    Returns:
    - A JSON representation of the updated user.
    Raises:
    - HTTPException: 404 error if the user to update is not found.
    """
    updated_user = update_user(user_id, user_update, db)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/user/delete/{user_id}")
def delete_user_by_id(user_id: str, db: Session = Depends(get_db)):
    """
    Delete an existing user's information.

    This endpoint delete the data of the user specified by the user_id with the provided data.

    Parameters:
    - user_id (UUID4): The unique identifier of the user to be deleted.
    - db (Session, optional): The database session dependency.

    Returns:
    - A message that the user was deleted.

    Raises:
    - HTTPException: 404 error if the user to delete is not found.
    """
    user_to_delete = delete_user(user_id, db)
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User was successfully deleted"}
