from typing import Optional

from api import celery
from api.database import delete, delete_all, exists

@celery.task(bind=True)
def delete_resources_task(self, resource_type: str, id: Optional[str] = None):
    self.update_state(state='PROGRESS', meta={'status': 'Deleting resource...'})

    try:
        local_type = f'local_{resource_type}'

        if id:
            # Delete single item
            # Delete from local database if it exists
            if exists(local_type, id):
                delete(local_type, id)
                self.update_state(state='PROGRESS', meta={'status': f'Deleted from {local_type}'})
            
            # Delete from main database if it exists
            if exists(resource_type, id):
                delete(resource_type, id)
                self.update_state(state='PROGRESS', meta={'status': f'Deleted from {resource_type}'})
            
            if not exists(local_type, id) and not exists(resource_type, id):
                return {'status': 'SUCCESS', 'result': f"{resource_type} with ID {id} has been deleted"}
            else:
                return {'status': 'NOT_FOUND', 'result': None}
        else:
            # Bulk delete
            delete_all(local_type)
            delete_all(resource_type)
            
            return {
                'status': 'SUCCESS',
                'result': f"All {resource_type} resources have been deleted"
            }

    except Exception as exc:
        self.update_state(state='FAILURE', meta={'status': f'Delete operation failed: {str(exc)}'})
        return {'status': 'FAILURE', 'result': str(exc)}