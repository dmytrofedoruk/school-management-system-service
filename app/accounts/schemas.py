from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    username: Optional[str] = None
    fullname: Optional[str] = None

class UserRegisterResponse(BaseModel):
    id: int
    