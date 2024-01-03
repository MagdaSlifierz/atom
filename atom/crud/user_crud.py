from sqlalchemy.orm import Session
from atom.schemas.user_schema import UserCreate
from atom.models.user_model import User
from atom.core.hashing import Hasher


def create_new_user(user: UserCreate, db: Session):
    user = User(
        first_name=user.user_first_name,
        last_name=user.user_last_name,
        email=user.user_email,
        password=Hasher.get_password_hash(user.user_password)

    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
