from celery import Celery
import time

celery = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@celery.task
def long_running_task(seconds):
    time.sleep(seconds)
    return f"Task completed after {seconds} seconds"