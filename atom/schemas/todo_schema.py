from pydantic import BaseModel

from typing import Optional

from datetime import datetime
from typing import Optional
from .user_schema import ShowUser

"""
This module defines the pydantic schema for todo items.
"""


class ToDoCreate(BaseModel):
    """
    Pydantic schema for creating a new todo item .
    """

    todo_name: str
    owner_id: str
    todo_done_or_not: Optional[bool]


class ToDoShow(BaseModel):
    """
    Pydantic schema for displaying todo item information.
    This schema is used to define how todo data is presented, especially after retrieval
    from the database.
    """

    todo_id: str
    todo_name: str
    todo_done_or_not: bool
    todo_created_at: datetime
    todo_updated_at: datetime
    owner: Optional[ShowUser]


class ToDoUpdate(BaseModel):
    """
    Pydantic schema for todo item to perform after updating .
    """

    todo_name: str
    todo_done_or_not: Optional[bool]
