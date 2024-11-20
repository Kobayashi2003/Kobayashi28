from typing import Dict, Any, List, Union
from celery import Task
from sqlalchemy.exc import SQLAlchemyError

from api import celery
from api.database import update

@celery.task(bind=True)
def edit_resources_task(self: Task, resource_type: str, updates: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Dict[str, Any]:
    """
    Celery task to edit one or multiple resources of a given type.

    Args:
        self (Task): The Celery task instance.
        resource_type (str): The type of resource to edit.
        updates (Union[Dict[str, Any], List[Dict[str, Any]]]): A single update dictionary or a list of update dictionaries.

    Returns:
        Dict[str, Any]: A dictionary containing the task status and results of the edit operations.
    """
    updates = [updates] if isinstance(updates, dict) else updates
    
    self.update_state(state='PROGRESS', meta={'status': 'Starting edit operation...'})
    
    results = []
    success_count = 0
    total_count = len(updates)

    for i, update_data in enumerate(updates, 1):
        id = update_data.pop('id', None)
        if not id:
            results.append({'id': None, 'status': 'FAILURE', 'result': 'No id provided for update'})
            continue

        result = perform_edit(self, resource_type, id, update_data)
        results.append({'id': id, **result})

        if result['status'] == 'SUCCESS':
            success_count += 1

        self.update_state(state='PROGRESS', meta={
            'status': f'Processed {i}/{total_count} resources. Success: {success_count}, Failure: {i - success_count}'
        })

    return {
        'status': 'COMPLETE',
        'result': {
            'total': total_count,
            'success': success_count,
            'failure': total_count - success_count,
            'details': results
        }
    }

def perform_edit(self: Task, resource_type: str, id: str, update_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Perform the edit operation for a single resource.

    Args:
        self (Task): The Celery task instance.
        resource_type (str): The type of resource to edit.
        id (str): The ID of the resource to edit.
        update_data (Dict[str, Any]): The data to update for the resource.

    Returns:
        Dict[str, str]: A dictionary containing the status and result of the edit operation.
    """
    self.update_state(state='PROGRESS', meta={'status': f'Editing {resource_type} with id {id}...'})

    try:
        result = update(resource_type, id, update_data)
        if result is None:
            return {'status': 'FAILURE', 'result': f'{resource_type.capitalize()} with id {id} not found or failed to update'}

        return {'status': 'SUCCESS', 'result': f'{resource_type.capitalize()} with id {id} updated successfully'}

    except SQLAlchemyError as exc:
        return {'status': 'FAILURE', 'result': f'Database error: {str(exc)}'}
    except Exception as exc:
        return {'status': 'FAILURE', 'result': f'Unexpected error: {str(exc)}'}