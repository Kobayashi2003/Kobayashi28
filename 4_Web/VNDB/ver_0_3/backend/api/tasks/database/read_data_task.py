from typing import Optional

from api import celery
from api.database import get, get_all, exists
from api.utils import convert_model_to_dict

@celery.task(bind=True)
def read_data_task(self, read_type: str, id: Optional[str] = None, page: Optional[int] = None, limit: Optional[int] = None, sort: Optional[str] = None, order: str = 'asc'):
    self.update_state(state='PROGRESS', meta={'status': 'Reading...'})

    try:
        # Check if the item exists in the local_type table
        local_type = f'local_{read_type}'
        if id:
            if not exists(local_type, id):
                return {'status': 'NOT_FOUND', 'result': None}
        else:
            # For get_all, we'll filter the results to only include items that exist in the local_type table
            local_ids = set(item.id for item in get_all(local_type))
            if not local_ids:
                return {'status': 'NOT_FOUND', 'result': None}

        # Perform the read operation
        if id:
            result = get(read_type, id)
        else:
            result = get_all(read_type, page=page, limit=limit, sort=sort, order=order)
            # Filter results to only include items that exist in the local_type table
            result = [item for item in result if item.id in local_ids]

        result = convert_model_to_dict(result)

        if not result:
            return {'status': 'NOT_FOUND', 'result': None}

        return {'status': 'SUCCESS', 'result': result}
    except Exception as exc:
        self.update_state(state='FAILURE', meta={'status': f'Read operation failed: {str(exc)}'})
        raise
