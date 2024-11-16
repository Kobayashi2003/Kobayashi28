from api import celery
from api.database import backup_database_pg_dump, restore_database_pg_dump

@celery.task(bind=True)
def backup_task(self, filename=None):
    self.update_state(state='PROGRESS', meta={'status': 'Starting database backup...'})
    
    try:
        backup_file = backup_database_pg_dump(filename)
        
        return {
            'status': 'SUCCESS',
            'result': f'Database backup created: {backup_file}',
            'filename': backup_file
        }
    
    except Exception as e:
        self.update_state(state='FAILURE', meta={'status': f'Database backup failed: {str(e)}'})
        raise

@celery.task(bind=True)
def restore_task(self, filename):
    self.update_state(state='PROGRESS', meta={'status': 'Starting database restore...'})
    
    try:
        restore_database_pg_dump(filename)
        
        return {
            'status': 'SUCCESS',
            'result': f'Database restored from: {filename}'
        }
    
    except Exception as e:
        self.update_state(state='FAILURE', meta={'status': f'Database restore failed: {str(e)}'})
        raise