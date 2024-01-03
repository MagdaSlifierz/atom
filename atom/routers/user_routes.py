from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends

from atom.schemas.user_schema import UserCreate
from atom.models.database import get_db
from atom.crud.user_crud import create_new_user

router = APIRouter()


# UserCreate schema will validate that it has a email in proper format, and a password
@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_new_user(user=user, db=db)
    return user
