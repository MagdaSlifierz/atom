from sqlalchemy.orm import Session
from atom.schemas.user_schema import UserCreate, UserUpdate
from atom.models.user_model import User
from atom.core.hashing import Hasher
from fastapi import HTTPException
from typing import Optional


def create_new_user(user: UserCreate, db: Session):
    user_to_save = User(
        user_id=user.user_id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=Hasher.get_password_hash(user.password)

    )
    db.add(user_to_save)
    db.commit()
    db.refresh(user_to_save)
    return user_to_save


def read_all_users(db: Session):
    users = db.query(User).all()
    return users


def get_user_by_id(user_id: int, db: Session) -> Optional[User]:
    user = db.query(User).filter(User.user_id == user_id).first()
    return user


def get_user_by_email(email: str, db: Session):
    user_email = db.query(User).filter(User.email == email).first()
    return user_email


'''
1. user_update.__dict__:

__dict__ is a special attribute in Python that returns a dictionary containing the attributes and values of an object.
user_update.__dict__ returns a dictionary representation of the attributes of the UserUpdate object.
The purpose of using __dict__ here is to dynamically iterate over the fields of the UserUpdate object without explicitly 
knowing them.
2. getattr and setattr:

getattr(object, attribute) is a built-in Python function that gets the value of the named attribute from the object.
setattr(object, attribute, value) is a built-in Python function that sets the value of the named attribute on the object.
In the context of the code, field is a string representing the attribute name, and getattr(user_update, field) gets the 
current value of the attribute from the UserUpdate object.
setattr(existing_user, field, value) sets the corresponding attribute in the existing_user object with the new value.
The overall purpose of this approach is to create a flexible and dynamic update mechanism. It allows you to update fields 
in existing_user based on the fields present in the UserUpdate object without explicitly listing each field in the code. This can be particularly useful when dealing with a large number of fields or when the fields can change dynamically.
'''


def update_user(user_id: int, user_update: UserUpdate, db: Session):
    # get the user from the database reuse method get_user_by_id
    existing_user = get_user_by_id(user_id, db)
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    # existing_user.update(user_update.__dict__)
    # Update user fields with new data
    for field, value in user_update.dict(exclude_unset=True).items():
        # Check if the field is the password and hash it
        if field == "password":
            value = Hasher.get_password_hash(value)
        setattr(existing_user, field, value)
    db.commit()
    db.refresh(existing_user)
    return existing_user


def delete_user(user_id: int, db: Session):
    user_to_delete = get_user_by_id(user_id, db)
    if user_to_delete:
        db.delete(user_to_delete)
        db.commit()
    return user_to_delete
