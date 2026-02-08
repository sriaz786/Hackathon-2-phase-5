from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class AiAuditLog(SQLModel, table=True):
    __tablename__ = "ai_audit_logs"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    action: str
    input_data: Optional[str] = None
    result: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
