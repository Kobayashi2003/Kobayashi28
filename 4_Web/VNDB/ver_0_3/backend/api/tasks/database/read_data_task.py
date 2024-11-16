from api import celery
from api.database import get, get_all, exists
from api.utils import convert_model_to_dict

@celery.task(bind=True)
def read_data_task(self, read_type, id=None):
    self.update_state(state='PROGRESS',  meta={'status': 'Reading...'})

    try:
        result = get(read_type, id) if id else get_all(read_type)
        result = convert_model_to_dict(result)

        if not result:
            return {'status': 'NOT_FOUND','result': None}

        return {'status': 'SUCCESS','result': result}
    except Exception as exc:
        self.update_state(state='FAILURE', meta={'status': f'Read operation failed: {str(exc)}'})
        raise
