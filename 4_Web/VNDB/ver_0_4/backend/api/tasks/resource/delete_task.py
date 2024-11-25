from typing import Optional, Dict, Any
from celery import Task

from api import celery
from api.database import delete, delete_all, delete_all_related, convert_model_to_dict 

@celery.task(bind=True)
def delete_related_resources_task(
    self: Task,
    resource_type: str,
    resource_id: str,
    related_resource_type: str
) -> Dict[str, Any]:
    self.update_state(state='PROGRESS', meta={'status': f'Deleting related {related_resource_type} for {resource_type} with id {resource_id}...'})

    try:
        deleted_count = delete_all_related(resource_type, resource_id, related_resource_type)

        if deleted_count == 0:
            return {'status': 'NOT_FOUND', 'result': f"No related {related_resource_type} found for {resource_type} with id {resource_id}"}

        return {'status': 'SUCCESS', 'result': f"Deleted {deleted_count} related {related_resource_type} for {resource_type} with id {resource_id}"}

    except ValueError as exc:
        self.update_state(state='FAILURE', meta={'status': f'Invalid resource type or related resource type: {str(exc)}'})
        return {'status': 'FAILURE', 'result': str(exc)}

    except Exception as exc:
        self.update_state(state='FAILURE', meta={'status': f'Delete related resources operation failed: {str(exc)}'})
        return {'status': 'FAILURE', 'result': str(exc)}

@celery.task(bind=True)
def delete_resources_task(self: Task, resource_type: str, id: Optional[str] = None) -> Dict[str, Any]:
    if id:
        return delete_single_resource(self, resource_type, id)
    else:
        return delete_all_resources(self, resource_type)

def delete_single_resource(self: Task, resource_type: str, id: str) -> Dict[str, Any]:
    self.update_state(state='PROGRESS', meta={'status': f'Deleting {resource_type} with id {id}...'})

    try:
        result = delete(resource_type, id)
        
        if not result:
            return {'status': 'NOT_FOUND', 'result': None}

        return {'status': 'SUCCESS', 'result': convert_model_to_dict(result)}

    except Exception as exc:
        self.update_state(state='FAILURE', meta={'status': f'Delete operation failed: {str(exc)}'})
        return {'status': 'FAILURE', 'result': str(exc)}

def delete_all_resources(self: Task, resource_type: str) -> Dict[str, Any]:
    self.update_state(state='PROGRESS', meta={'status': f'Deleting all {resource_type} resources...'})

    try:
        count = delete_all(resource_type)

        if not count:
            return {'status': 'NOT_FOUND', 'result': None} 

        return {'status': 'SUCCESS', 'result': f"Deleted {count} {resource_type} resources."}

    except Exception as exc:
        self.update_state(state='FAILURE', meta={'status': f'Bulk delete operation failed: {str(exc)}'})
        return {'status': 'FAILURE', 'result': str(exc)}