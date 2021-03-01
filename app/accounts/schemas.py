from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    email: EmailStr
    password: str
    username: Optional[str] = None
    fullname: Optional[str] = None
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None


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
