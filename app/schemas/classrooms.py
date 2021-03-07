from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class Classroom(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None
    teacher_id: int


class CreateClassroomRequest(BaseModel):
    name: str
    description: Optional[str] = None
