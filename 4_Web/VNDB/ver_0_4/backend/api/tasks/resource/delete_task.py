from typing import Optional, Dict, Any

from api import celery
from api.database import delete, delete_all, exists

@celery.task(bind=True)
def delete_resources_task(self, resource_type: str, id: Optional[str] = None):
    if id:
        return delete_single_resource(self, resource_type, id)
    else:
        return delete_all_resources(self, resource_type)

def delete_single_resource(self, resource_type: str, id: str) -> Dict[str, Any]:
    self.update_state(state='PROGRESS', meta={'status': f'Deleting {resource_type} with id {id}...'})

    try:
        local_type = f'local_{resource_type}'
        
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
            return {'status': 'NOT_FOUND', 'result': f"{resource_type} with ID {id} not found or could not be deleted"}

    except Exception as exc:
        self.update_state(state='FAILURE', meta={'status': f'Delete operation failed: {str(exc)}'})
        return {'status': 'FAILURE', 'result': str(exc)}

def delete_all_resources(self, resource_type: str) -> Dict[str, Any]:
    self.update_state(state='PROGRESS', meta={'status': f'Deleting all {resource_type} resources...'})

    try:
        local_type = f'local_{resource_type}'
        
        # Delete all from local database
        local_count = delete_all(local_type)
        self.update_state(state='PROGRESS', meta={'status': f'Deleted {local_count} items from {local_type}'})
        
        # Delete all from main database
        main_count = delete_all(resource_type)
        self.update_state(state='PROGRESS', meta={'status': f'Deleted {main_count} items from {resource_type}'})
        
        return {
            'status': 'SUCCESS',
            'result': f"Deleted {main_count} {resource_type} resources and {local_count} local entries"
        }

    except Exception as exc:
        self.update_state(state='FAILURE', meta={'status': f'Bulk delete operation failed: {str(exc)}'})
        return {'status': 'FAILURE', 'result': str(exc)}