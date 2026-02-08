from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.services.scheduler import check_and_publish_reminders
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/scheduled-tasks")
def trigger_scheduler(session: Session = Depends(get_session)):
    """
    Triggered by Dapr Binding (Cron).
    """
    logger.info("Scheduler triggered by Dapr Binding.")
    try:
        check_and_publish_reminders(session)
        return {"status": "SUCCESS"}
    except Exception as e:
        logger.error(f"Scheduler failed: {e}")
        return {"status": "ERROR", "detail": str(e)}
