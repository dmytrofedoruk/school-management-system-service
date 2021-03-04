from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class Departement(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None
    head_id: int


class CreateDepartementRequest(BaseModel):
    name: str
    description: Optional[str] = None
