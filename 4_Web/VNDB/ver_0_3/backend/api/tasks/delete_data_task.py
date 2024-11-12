from api import celery
from ..database import delete, exists

@celery.task(bind=True)
def delete_data_task(self, data_type, id):
    self.update_state(state='PROGRESS', meta={'status': 'Checking local database...'}) 

    local_type = f'local_{data_type}'

    try:
        if exists(local_type, id):
            delete(local_type, id)
            return {
                'status': 'SUCCESS',
                'result': f"{local_type} with ID {id} has been deleted"
            }
        else:
            return {
                'status': 'NOT_FOUND',
                'result': f"{local_type} with ID {id} not found in local database"
            }
    
    except Exception as e:
        self.update_state(state='FAILURE', meta={'status': f'Delete operation failed: {str(e)}'})
        raise