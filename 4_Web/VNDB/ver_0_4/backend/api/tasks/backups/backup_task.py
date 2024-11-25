from typing import Dict, Union
from celery import Task
from sqlalchemy.exc import SQLAlchemyError

from api import celery
from api.database import create_backup 

@celery.task(bind=True)
def backup_task(self: Task) -> Dict[str, Union[str, None]]:

    self.update_state(state='PROGRESS', meta={'status': 'Starting database backup...'})

    try:
        backup_id = create_backup()
        self.update_state(state='PROGRESS', meta={'status': 'Backup completed successfully.'})
        return {"status": "SUCCESS", "result": f"Database backup created successfully: {backup_id}"}

    except Exception as e:
        return {"status": "ERROR", "result": str(e)}