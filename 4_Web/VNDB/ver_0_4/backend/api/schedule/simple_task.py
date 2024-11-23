from datetime import datetime
from flask import current_app

from api import scheduled_task

# @scheduled_task(trigger='interval', id='simple_task', seconds=1)
@scheduled_task(trigger='cron', id='cleanup_task', minute='*/1')
def simple_task():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"This is a simple scheduled print task. Current time: {current_time}"
    print(message)
    current_app.logger.info(message)