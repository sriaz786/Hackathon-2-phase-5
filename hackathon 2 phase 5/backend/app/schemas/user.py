from typing import Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    confirm_password: str

class UserLogin(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    username: str
    is_active: bool
    
    class Config:
        orm_mode = True
