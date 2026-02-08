from sqlmodel import Session, select
from datetime import datetime
from app.models.todo import Todo
from app.events.publisher import publish_event
import logging

logger = logging.getLogger(__name__)

def check_and_publish_reminders(db: Session):
    """
    Finds tasks with pending reminders and publishes them to the 'reminders' topic.
    """
    now = datetime.utcnow()
    
    # Query for tasks where reminder_time is passed, not yet sent, and task is not completed
    statement = select(Todo).where(
        Todo.reminder_time <= now,
        Todo.reminder_sent == False,
        Todo.status != "completed"
    )
    
    tasks = db.exec(statement).all()
    
    if not tasks:
        logger.info("No pending reminders found.")
        return

    logger.info(f"Found {len(tasks)} pending reminders.")

    for task in tasks:
        try:
            # Publish event
            reminder_payload = {
                "reminder_id": f"rem-{task.id}-{int(now.timestamp())}",
                "task_id": task.id,
                "user_id": task.user_id,
                "message": f"Reminder: Task '{task.title}' is due on {task.due_date}",
                "due_date": str(task.due_date)
            }
            
            publish_event("reminders", reminder_payload, event_type="task.reminder")
            
            # Mark as sent
            task.reminder_sent = True
            db.add(task)
            
        except Exception as e:
            logger.error(f"Failed to publish reminder for task {task.id}: {e}")
            # Continue to next task, don't break loop
            
    try:
        db.commit()
        logger.info("Processed reminders and updated DB state.")
    except Exception as e:
        logger.error(f"Failed to commit reminder state updates: {e}")
        db.rollback()
