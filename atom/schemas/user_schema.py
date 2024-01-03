from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    user_first_name: str
    user_last_name: str
    user_email: EmailStr
    user_password: str

    # class Config:
    #     orm_mode = True
