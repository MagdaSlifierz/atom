from pydantic import BaseModel
from datetime import datetime
from typing import Optional

"""
This module defines the pydantic schema for todo items.
"""


class ToDoCreate(BaseModel):
    """
    Pydantic schema for creating a new todo item.
    """

    title: str
    completed: Optional[bool]


class ToDoShow(BaseModel):
    """
    Pydantic schema for displaying todo item information.
    This schema is used to define how todo data is presented, especially after retrieval
    from the database.
    """

    title: str
    completed: bool
    unique_id: str
    created_at: datetime
    updated_at: datetime


class ToDoUpdate(BaseModel):
    """
    Pydantic schema for todo item to perform after updating .
    """

    title: str
    completed: Optional[bool]
