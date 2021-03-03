from enum import IntEnum
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    email: EmailStr
    password: str
    username: Optional[str] = None
    fullname: Optional[str] = None
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None

class RoleEnum(IntEnum):
    ADMIN = 1
    FACULTY_DEAN = 2
    HEAD_DEPARTEMENT = 3
    TEACHER = 2
    STUDENT = 3


# ======================= REGISTER SCHEMA =======================
class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    username: Optional[str] = None
    fullname: Optional[str] = None
    role_id: RoleEnum


class UserRegisterResponse(BaseModel):
    id: int


# ======================= LOGIN SCHEMA =======================
class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserLoginResponse(BaseModel):
    token_type: str
    access_token: str
