from api import celery
from ..database import create, update, delete, get, get_all
from ..utils import convert_model_to_dict

@celery.task(bind=True)
def crud_task(self, operation, model_type, id, data):
    self.update_state(state='PROGRESS', meta={'status': f'Performing {operation} operation...'})
    
    try:
        result = None
        if operation == 'create':
            result = create(model_type, id, data)
        elif operation == 'read':
            result = get(model_type, id) if id else get_all(model_type)
        elif operation == 'update':
            result = update(model_type, id, data)
        elif operation == 'delete':
            result = delete(model_type, id)
        else:
            raise ValueError(f"Invalid operation: {operation}")

        result = convert_model_to_dict(result) if result else None

        return {
            'status': 'SUCCESS',
            'result': result
        }
    except Exception as e:
        self.update_state(state='FAILURE', meta={'status': f'{operation.capitalize()} operation failed: {str(e)}'})
        raise