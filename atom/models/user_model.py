import uuid

from sqlalchemy import Column, Integer, String
from atom.models.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

"""
    This module Represents a User entity within the database.
"""


class User(Base):
    """
    User entity model representing a user in the database.
    Attributes include user ID, first name, last name, email.
    The table name is set to 'users'
    """

    __tablename__ = "users"
    user_id = Column(
        String, primary_key=True, nullable=False, default=lambda: str(uuid.uuid4())
    )
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    # todos = relationship("Todo", back_populates="owner")
