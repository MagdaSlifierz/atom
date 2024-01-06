from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class ShowUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
