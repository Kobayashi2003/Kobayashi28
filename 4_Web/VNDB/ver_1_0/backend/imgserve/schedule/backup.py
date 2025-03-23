from imgserve.tasks.backup import backup_database_task
from .common import weekly_task

@weekly_task(day_of_week=0, hour=0, minute=0)
def backup_database_schedule():
    backup_database_task.delay()