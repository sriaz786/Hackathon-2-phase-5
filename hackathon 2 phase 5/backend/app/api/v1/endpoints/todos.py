from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.api import deps
from app.db.session import get_session
from app.models.todo import Todo
from app.models.user import User
from app.schemas.todo import TodoCreate, TodoRead, TodoUpdate

router = APIRouter()

@router.post("", response_model=TodoRead)
def create_todo(
    *,
    session: Session = Depends(get_session),
    todo_in: TodoCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new todo.
    """
    todo = Todo.from_orm(todo_in)
    todo.user_id = current_user.id
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@router.get("", response_model=List[TodoRead])
def read_todos(
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve todos.
    """
    # Filter by current user
    statement = select(Todo).where(Todo.user_id == current_user.id).offset(skip).limit(limit)
    todos = session.exec(statement).all()
    return todos

@router.get("/{id}", response_model=TodoRead)
def read_todo(
    id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Get todo by ID.
    """
    todo = session.get(Todo, id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return todo

@router.put("/{id}", response_model=TodoRead)
def update_todo(
    *,
    session: Session = Depends(get_session),
    id: int,
    todo_in: TodoUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Update todo.
    """
    todo = session.get(Todo, id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    todo_data = todo_in.dict(exclude_unset=True)
    previous_status = todo.status
    
    for key, value in todo_data.items():
        setattr(todo, key, value)
    
    session.add(todo)
    session.commit()
    session.refresh(todo)
    
    # Event Publishing & Recurrence Logic
    try:
        # Publish generic update event
        from app.events.publisher import publish_event
        publish_event("task-events", {
            "event_type": "task.updated",
            "task_id": todo.id,
            "user_id": todo.user_id,
            "status": todo.status
        })
        
        # Check for completion to trigger recurrence
        if previous_status != "completed" and todo.status == "completed":
            from app.services.recurring import process_recurrence
            process_recurrence(todo, session)
            
            # Publish specifically as completion
            publish_event("task-events", {
                "event_type": "task.completed",
                "task_id": todo.id,
                "user_id": todo.user_id
            })
            
    except Exception as e:
        print(f"Background task error: {e}") # Non-blocking for now
        
    return todo

@router.delete("/{id}", response_model=TodoRead)
def delete_todo(
    *,
    session: Session = Depends(get_session),
    id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete todo.
    """
    todo = session.get(Todo, id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    session.delete(todo)
    session.commit()
    return todo
