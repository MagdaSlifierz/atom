from sqlalchemy import Integer, Column, Boolean, String, DateTime, ForeignKey
from atom.models.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship
import uuid


class Todo(Base):
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
