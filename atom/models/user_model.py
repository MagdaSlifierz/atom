from sqlalchemy import Column, Integer, String
from atom.models.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, nullable=False)
    user_first_name = Column(String, nullable=False)
    user_last_name = Column(String, nullable=False)
    user_email = Column(String, unique=True, nullable=False)
    user_password = Column(String, nullable=False)

    todos = relationship("Todo", back_populates="owner")
