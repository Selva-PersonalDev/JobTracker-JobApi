from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional, List


class JobApplicationCreate(BaseModel):
    company: str
    role: str
    location: Optional[str] = None


class JobApplicationUpdate(BaseModel):
    status: str


class JobApplication(BaseModel):
    id: UUID
    company: str
    role: str
    location: Optional[str]
    status: str
    created_at: datetime


class StatusHistory(BaseModel):
    application_id: UUID
    old_status: str
    new_status: str
    changed_at: datetime
