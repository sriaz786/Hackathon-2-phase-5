from fastapi import APIRouter
from app.api.v1.endpoints import auth, todos, chat, scheduler
from app.events import subscriber as events

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(todos.router, prefix="/todos", tags=["todos"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(scheduler.router, tags=["scheduler"]) # Root level or specific prefix? Binding usually posts to /
api_router.include_router(events.router, tags=["events"]) # Root level for /dapr/subscribe
