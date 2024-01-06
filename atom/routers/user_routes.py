from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from atom.schemas.user_schema import UserCreate, ShowUser, UserUpdate
from atom.models.database import get_db
from atom.crud.user_crud import create_new_user, get_user_by_id, read_all_users, update_user, delete_user
from typing import List

router = APIRouter()


# UserCreate schema will validate that it has a email in proper format, and a password
@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_new_user(user, db)
    return user


@router.get("/user/all", response_model=List[ShowUser])
def get_all_users(db: Session = Depends(get_db)):
    user_all = read_all_users(db)
    return user_all


@router.get('/user/{user_id}')
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put('/user/update/{user_id}')
def update_user_by_id(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    updated_user = update_user(user_id, user_update, db)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete('/user/delete/{user_id}')
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user_to_delete = delete_user(user_id, db)
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User was successfully deleted"}
