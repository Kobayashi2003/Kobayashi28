from api import celery
from api.database import get_savedata, get_savedatas

@celery.task(bind=True)
def get_savedata_task(self, savedata_id):
    self.update_state(state='PROGRESS', meta={'status': 'Retrieving savedata...'})

    savedata = get_savedata(savedata_id)

    return {
        "status": "SUCCESS" if savedata else "NOT_FOUND",
        "result": savedata if savedata else None
    }