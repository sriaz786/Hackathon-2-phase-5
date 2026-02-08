from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from app.api import deps
from app.db.session import get_session
from app.models.user import User
from app.core.ai_tools import AiTools
from app.core.ai_service import AiService

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("", response_model=ChatResponse)
def chat_with_ai(
    request: ChatRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Chat with the AI to manage todos.
    """
    try:
        # Initialize tools with current session and user
        tools = AiTools(session=session, user=current_user)
        
        # Process message
        response_text = AiService.process_chat(request.message, tools)
        
        return ChatResponse(response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
