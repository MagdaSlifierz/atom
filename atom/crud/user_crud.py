from sqlalchemy.orm import Session
from atom.schemas.user_schema import UserCreate, UserUpdate
from atom.models.user_model import User
from fastapi import HTTPException
from typing import Optional


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


def get_user_by_id(user_id: str, db: Session) -> Optional[User]:
    """
    Retrieve a user by their unique identifier.

    Parameters:
    - user_id (UUID4): The unique identifier of the user.
    - db (Session): The SQLAlchemy session for database operations.

    Returns:
    - User or None: The User entity if found, otherwise None.
    """
    user = db.query(User).filter(User.unique_user_id == user_id).first()
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


def update_user(user_id: str, user_update: UserUpdate, db: Session):
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
    existing_user_to_update = get_user_by_id(user_id, db)
    # Update user fields with new data
    if existing_user_to_update is None:
        # Handle the case where the user doesn't exist
        # For example, return None or raise an HTTPException
        raise HTTPException(status_code=404, detail="User not found")
    existing_user_to_update.first_name = user_update.first_name
    existing_user_to_update.last_name = user_update.last_name
    existing_user_to_update.email = user_update.email
    db.commit()
    db.refresh(existing_user_to_update)
    return existing_user_to_update


def delete_user(user_id: str, db: Session):
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
