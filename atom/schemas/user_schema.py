from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: EmailStr
    password: str

    # class Config:
    #     orm_mode = True

class ShowUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr