from api import celery
from api.database import delete_savedatas

@celery.task(bind=True)
def delete_savedatas_task(self, vnid):
    self.update_state(state='PROGRESS', meta={'status': 'Deleting savedatas...'})
    
    deleted_count = delete_savedatas(vnid)

    return {
        "status": "SUCCESS",
        "result": deleted_count
    }