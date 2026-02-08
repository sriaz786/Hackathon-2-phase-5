from datetime import datetime, timedelta
from typing import Optional
from sqlmodel import Session
from app.models.todo import Todo
from app.events.publisher import publish_event
import logging

logger = logging.getLogger(__name__)

def calculate_next_due_date(current_due: datetime, rule: str) -> Optional[datetime]:
    if not current_due:
        current_due = datetime.utcnow()
    
    if rule == "daily":
        return current_due + timedelta(days=1)
    elif rule == "weekly":
        return current_due + timedelta(weeks=1)
    elif rule == "monthly":
        # Simplified monthly logic (add 30 days) - can be enhanced for exact calendar months
        return current_due + timedelta(days=30)
    else:
        return None

def process_recurrence(task: Todo, db: Session):
    """
    Checks if a completed task is recurring and creates the next instance.
    """
    if not task.recurrence_rule:
        return

    logger.info(f"Processing recurrence for task {task.id} with rule {task.recurrence_rule}")

    next_due = calculate_next_due_date(task.due_date, task.recurrence_rule)
    
    if not next_due:
        logger.warning(f"Could not calculate next due date for rule: {task.recurrence_rule}")
        return

    new_task = Todo(
        title=task.title,
        description=task.description,
        user_id=task.user_id,
        status="pending",
        due_date=next_due,
        recurrence_rule=task.recurrence_rule
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    logger.info(f"Generated new recurring task {new_task.id} due on {new_task.due_date}")
    
    # Publish event
    publish_event("task-events", {
        "event_type": "task.created",
        "task_id": new_task.id,
        "user_id": new_task.user_id,
        "origin": "recurrence"
    })
