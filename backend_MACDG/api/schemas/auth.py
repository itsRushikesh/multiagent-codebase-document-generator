from pydantic import BaseModel, EmailStr
from typing import Literal, List

class UserSignup(BaseModel):
    email: EmailStr
    password: str
    role: Literal['User', 'Admin']

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


