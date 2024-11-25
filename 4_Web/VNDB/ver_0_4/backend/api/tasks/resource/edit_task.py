from typing import Dict, Any, List, Union
from celery import Task

from api import celery
from api.database import update

@celery.task(bind=True)
def edit_resources_task(self: Task, resource_type: str, updates: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Dict[str, Any]:
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
    self.update_state(state='PROGRESS', meta={'status': f'Editing {resource_type} with id {id}...'})

    try:
        result = update(resource_type, id, update_data)
        if result is None:
            return {'status': 'FAILURE', 'result': f'{resource_type.capitalize()} with id {id} not found or failed to update'}

        return {'status': 'SUCCESS', 'result': f'{resource_type.capitalize()} with id {id} updated successfully'}
    
    except Exception as exc:
        return {'status': 'FAILURE', 'result': f'Unexpected error: {str(exc)}'}