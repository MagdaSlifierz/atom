from sqlalchemy.orm import Session
from atom.schemas.user_schema import UserCreate, ShowUser
from atom.models.user_model import User
from atom.core.hashing import Hasher


def create_new_user(user: UserCreate, db: Session):
    user1 = User(
        user_id=user.user_id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=Hasher.get_password_hash(user.password)

    )
    db.add(user1)
    db.commit()
    db.refresh(user1)
    return user1

def get_user(userEmail: ShowUser, db: Session):
    userEmail = db.query(User).filter(User.email == userEmail).first()
    return userEmail

