from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional

"""
This module defines the pydantic schema for user.
"""
class UserCreate(BaseModel):
    """
       Pydantic schema for user creation.

       This schema is used for validating data needed to create a new user.
    """
    first_name: str
    last_name: str
    email: EmailStr


class ShowUser(BaseModel):
    """
        Pydantic schema for displaying user information.

        This schema is used to define how user data is presented, especially after retrieval
        from the database. The orm_mode config enables it to work with ORM models.

        Config:
        - orm_mode (bool): Enable ORM mode for compatibility with SQLAlchemy models.
        This makes it easier to convert ORM model instances into Pydantic model instances,
        facilitating the serialization and validation of data coming from the database
    """
    user_id: UUID4
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    """
        Pydantic schema for updating user data.

        This schema allows partial updates of user data. Fields are optional, meaning
        they don't need to be included in the update request.
    """
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
