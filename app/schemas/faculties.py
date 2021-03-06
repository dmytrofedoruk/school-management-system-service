from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class Faculty(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None
    dean_id: int

class CreateFacultyRequest(BaseModel):
    name: str
    description: Optional[str] = None