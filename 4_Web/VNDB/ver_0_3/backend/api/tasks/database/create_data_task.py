from datetime import datetime, timezone

from api import celery
from api.database import create, exists

@celery.task(bind=True)
def create_data_task(self, create_type, id, data):
    self.update_state(state='PROGRESS',  meta={'status': 'Creating...'})

    create_result = {}

    try:
        if not exists(create_type, id):
            create(create_type, id, data)
            create_result[f'{create_type}'] = True
        else:
            create_result[f'{create_type}'] = False

        if not exists(f'local_{create_type}', id):
            create(f'local_{create_type}', id, {'last_updated': datetime.now(timezone.utc)})
            create_result[f'local_{create_type}'] = True
        else:
            create_result[f'local_{create_type}'] = False

        return {'status': 'SUCCESS', 'result': create_result}

    except Exception as exc:
        self.update_state(state='FAILURE', meta={'status': f'Update operation failed: {str(exc)}'})
        raise
    