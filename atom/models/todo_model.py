from sqlalchemy import Integer, Column, Boolean, String, DateTime, ForeignKey
from atom.models.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship
import uuid

"""
    This module Represents a Todo entity within the database.
"""


class Todo(Base):
    """
    Todo item entity model representing a todo item in the database.
    Attributes include todo ID, todo name, if item was done or not, time of creating and updating as well as connection
    to relationship with the user

    The table name is set to 'todos'
    """

    __tablename__ = "todos"

    todo_id = Column(
        String, primary_key=True, nullable=False, default=lambda: str(uuid.uuid4())
    )
    todo_name = Column(String, nullable=False)
    todo_done_or_not = Column(Boolean, default=False)
    todo_created_at = Column(DateTime, default=datetime.now)
    todo_updated_at = Column(DateTime, default=datetime.now)
    # it is fore for which tabel - user and witch field user_id
    owner_id = Column(String, ForeignKey("users.user_id"))

    # relationship with the clas user, back_p to todos variable in user class
    owner = relationship("User", back_populates="todos")
