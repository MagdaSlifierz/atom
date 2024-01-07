from sqlalchemy.orm import Session
from atom.schemas.user_schema import UserCreate, UserUpdate
from atom.models.user_model import User
from fastapi import HTTPException
from typing import Optional
from pydantic import UUID4


def create_new_user(user: UserCreate, db: Session):
    """
        Create a new user in the database.

        This function takes a UserCreate object and a SQLAlchemy Session, creates a new User
        entity from the UserCreate data, and saves it to the database.

        Parameters:
        - user (UserCreate): A Pydantic model containing the data for the new user.
        - db (Session): The SQLAlchemy session for database operations.
        Returns:
        - User: The newly created User entity.
    """
    user_to_save = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
    )
    db.add(user_to_save)
    db.commit()
    db.refresh(user_to_save)
    return user_to_save


def read_all_users(db: Session):
    """
       Retrieve all users from the database.

       This function queries the database for all User entities and returns them.

       Parameters:
       - db (Session): The SQLAlchemy session for database operations.

       Returns:
       - List[User]: A list of User entities.
    """
    users = db.query(User).all()
    return users


def get_user_by_id(user_id: UUID4, db: Session) -> Optional[User]:
    """
       Retrieve a user by their unique identifier.

       Parameters:
       - user_id (UUID4): The unique identifier of the user.
       - db (Session): The SQLAlchemy session for database operations.

       Returns:
       - User or None: The User entity if found, otherwise None.
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    return user


def get_user_by_email(email: str, db: Session):
    """
       Retrieve a user by their email address.

       Parameters:
       - email (str): The email address of the user.
       - db (Session): The SQLAlchemy session for database operations.

       Returns:
       - User or None: The User entity if found, otherwise None.
    """
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


def update_user(user_id: UUID4, user_update: UserUpdate, db: Session):
    """
        Update an existing user's information.

        This function updates the information of an existing user based on the provided
        UserUpdate object. It dynamically updates only the fields that are provided in
        the UserUpdate object.

        Parameters:
        - user_id (UUID4): The unique identifier of the user to be updated.
        - user_update (UserUpdate): A Pydantic model containing the updated user data.
        - db (Session): The SQLAlchemy session for database operations.

        Returns:
        - User: The updated User entity.
    """
    # get the user from the database reuse method get_user_by_id
    existing_user = get_user_by_id(user_id, db)
    # existing_user.update(user_update.__dict__)
    # Update user fields with new data
    for field, value in user_update.dict(exclude_unset=True).items():
        # Check if the field is the password and hash it
        # if field == "password":
        #     value = Hasher.get_password_hash(value)
        setattr(existing_user, field, value)
    db.commit()
    db.refresh(existing_user)
    return existing_user


def delete_user(user_id: UUID4, db: Session):
    """
       Delete a user from the database.

       This function deletes the user associated with the provided user ID from the database.

       Parameters:
       - user_id (UUID4): The unique identifier of the user to be deleted.
       - db (Session): The SQLAlchemy session for database operations.

       Returns:
       - User or None: The deleted User entity if found and deleted, otherwise None.
    """
    user_to_delete = get_user_by_id(user_id, db)
    if user_to_delete:
        db.delete(user_to_delete)
        db.commit()
    return user_to_delete
