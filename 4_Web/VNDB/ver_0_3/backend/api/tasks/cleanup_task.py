from api import celery
from ..database import cleanup, cleanup_all

@celery.task(bind=True)
def cleanup_task(self, type=None):
    self.update_state(state='PROGRESS', meta={'status': 'Starting database cleanup...'})
    
    try:
        if type:
            deleted = cleanup(type)
            result = {type: deleted}
        else:
            result = cleanup_all()
        
        total_removed = sum(result.values())
        
        return {
            'status': 'SUCCESS',
            'result': result,
            'total_removed': total_removed
        }
    
    except ValueError as e:
        self.update_state(state='FAILURE', meta={'status': f'Invalid type: {str(e)}'})
        raise
    except Exception as e:
        self.update_state(state='FAILURE', meta={'status': f'Database cleanup failed: {str(e)}'})
        raise