try:
    from dapr.clients import DaprClient
except ImportError:
    # Mock DaprClient for Vercel environment where Dapr sidecar is not available
    class DaprClient:
        def __enter__(self): return self
        def __exit__(self, exc_type, exc_value, traceback): pass
        def publish_event(self, *args, **kwargs):
            logger.info(f"MOCK PUBLISH: {kwargs}")

import json
import logging

logger = logging.getLogger(__name__)

PUBSUB_NAME = "pubsub"

def publish_event(topic: str, data: dict, event_type: str = "com.hackathon.event"):
    """
    Publishes an event to the configured Dapr PubSub component.
    """
    try:
        with DaprClient() as client:
            client.publish_event(
                pubsub_name=PUBSUB_NAME,
                topic_name=topic,
                data=json.dumps(data),
                data_content_type='application/json',
                metadata={"cloudevent.type": event_type}
            )
            logger.info(f"Published event to {topic}: {data}")
    except Exception as e:
        logger.error(f"Failed to publish event to {topic}: {e}")
        # raise e  <-- Suppress error in Vercel to allow app to run

