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
        Attributes include todo ID as PK, unique ID todo name, if item was done or not, time of creating and updating
        connection to relationship with the user
    """

    __tablename__ = "todos"
    id = Column(Integer, nullable=False, primary_key=True)
    unique_todo_id = Column(String, nullable=False, default=lambda: str(uuid.uuid4()))
    todo_name = Column(String, nullable=False)
    todo_done_or_not = Column(Boolean, default=False)
    todo_created_at = Column(DateTime, default=datetime.now)
    todo_updated_at = Column(DateTime, default=datetime.now)
    # it is for which tabel - user and field id as primary_key
    owner_id = Column(Integer, ForeignKey("users.id"))

    # relationship with the clas user, back_p to todos variable in user class
    owner = relationship("User", back_populates="todos")
