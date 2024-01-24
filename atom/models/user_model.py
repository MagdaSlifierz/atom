from sqlalchemy import Column, Integer, String
from atom.models.database import Base
from sqlalchemy.orm import relationship
import uuid

"""
    This module Represents a User entity within the database.
"""


class User(Base):
    """
    User entity model representing a user in the database.
    Attributes include ID, user ID, first name, last name, email.
    This table has a relationship one user to many todos
    When user is deleted all todo items associate with the user are deleted
    The table name is set to 'users'
    """

    __tablename__ = "users"
    id = Column(Integer, nullable=False, primary_key=True)
    unique_user_id = Column(String, nullable=False, default=lambda: str(uuid.uuid4()))
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    todos = relationship("Todo", cascade="all, delete", back_populates="owner")
