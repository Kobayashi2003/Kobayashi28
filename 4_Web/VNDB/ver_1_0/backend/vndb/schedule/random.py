from vndb.tasks.random import random_fetch_task, random_update_task
from .common import hourly_task 

@hourly_task()
def random_fetch_schedule():
    random_fetch_task.delay()

@hourly_task()
def random_update_schedule():
    random_update_task.delay()