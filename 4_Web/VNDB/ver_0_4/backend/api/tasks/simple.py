from datetime import datetime, timezone
from flask import current_app

from api import celery, scheduled_task

def _simple_task():
    current_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    message = f"This is a simple scheduled print task. Current time: {current_time}"
    print(message)
    current_app.logger.info(message)

@celery.task
def simple_task(): _simple_task()

@scheduled_task(trigger='interval', id='simple_task', seconds=5)
def scheduled_simple_task(): _simple_task()
