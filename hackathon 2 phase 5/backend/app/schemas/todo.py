from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "pending"
    due_date: Optional[datetime] = None
    recurrence_rule: Optional[str] = None
    reminder_time: Optional[datetime] = None

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[datetime] = None
    recurrence_rule: Optional[str] = None
    reminder_time: Optional[datetime] = None

class TodoRead(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    reminder_sent: bool
    
    class Config:
        orm_mode = True
