from fastapi import APIRouter, Request
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Programmatic Subscription (optional, if not using declarative subscription via k8s)
@router.get("/dapr/subscribe")
def subscribe():
    subscriptions = [
        {
            'pubsubname': 'pubsub',
            'topic': 'task-events',
            'route': 'events/task-processed'
        },
        {
            'pubsubname': 'pubsub',
            'topic': 'reminders',
            'route': 'events/reminder-triggered'
        }
    ]
    return subscriptions

@router.post("/events/task-processed")
async def handle_task_event(request: Request):
    try:
        body = await request.json()
        logger.info(f"Received task event: {body}")
        # Logic to handle task event (e.g. update local state)
        return {"status": "SUCCESS"}
    except Exception as e:
        logger.error(f"Error handling task event: {e}")
        return {"status": "DROP"}

@router.post("/events/reminder-triggered")
async def handle_reminder(request: Request):
    try:
        body = await request.json()
        logger.info(f"Received reminder: {body}")
        # Logic to send notification
        return {"status": "SUCCESS"}
    except Exception as e:
        logger.error(f"Error handling reminder: {e}")
        return {"status": "DROP"}
