from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.user import User

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: Optional[str] = None
    status: str = Field(default="pending") # pending, completed
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    due_date: Optional[datetime] = Field(default=None)
    recurrence_rule: Optional[str] = Field(default=None) # e.g., "daily", "weekly", "monthly"
    
    reminder_time: Optional[datetime] = Field(default=None)
    reminder_sent: bool = Field(default=False)

    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    user: Optional["User"] = Relationship(back_populates="todos")
