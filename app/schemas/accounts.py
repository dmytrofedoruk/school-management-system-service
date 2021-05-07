from enum import IntEnum
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr


class RoleEnum(IntEnum):
    ADMIN = 1
    FACULTY_DEAN = 2
    HEAD_DEPARTEMENT = 3
    TEACHER = 4
    STUDENT = 5


class User(BaseModel):
    id: int
    email: EmailStr
    password: str
    code: str = None
    is_validated: bool
    username: Optional[str] = None
    fullname: Optional[str] = None
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None
    role_mappings: List[RoleEnum]

# ======================= REGISTER SCHEMA =======================


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    username: Optional[str] = None
    fullname: Optional[str] = None


class UserRegisterResponse(BaseModel):
    id: int


class UserRegisterWithRole(UserRegisterRequest):
    role_mappings: List[RoleEnum]


# ======================= LOGIN SCHEMA =======================\
class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserLoginResponse(BaseModel):
    token_type: str
    access_token: str
