from api import celery
from api.database import delete_savedata

@celery.task(bind=True)
def delete_savedata_task(self, id):
    self.update_state(state='PROGRESS', meta={'status': 'Deleting savedata...'})
    
    result = delete_savedata(id)

    return {
        "status": "SUCCESS" if result else "NOT_FOUND",
        "result": result
    }