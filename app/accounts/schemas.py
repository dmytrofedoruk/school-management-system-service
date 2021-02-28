from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


# ======================= REGISTER SCHEMA =======================
class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    username: Optional[str] = None
    fullname: Optional[str] = None


class UserRegisterResponse(BaseModel):
    id: int


# ======================= LOGIN SCHEMA =======================
class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserLoginResponse(BaseModel):
    token_type: str
    access_token: str
