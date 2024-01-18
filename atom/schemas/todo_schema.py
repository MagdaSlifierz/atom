from pydantic import BaseModel

from typing import Optional

from datetime import datetime
from typing import Optional
from .user_schema import ShowUser


class ToDoCreate(BaseModel):
    todo_name: str
    owner_id: str
    todo_done_or_not: Optional[bool]


class ToDoShow(BaseModel):
    todo_id: str
    todo_name: str
    todo_done_or_not: bool
    todo_created_at: datetime
    todo_updated_at: datetime
    owner: Optional[ShowUser]


class ToDoUpdate(BaseModel):
    todo_name: str
    todo_done_or_not: Optional[bool]
