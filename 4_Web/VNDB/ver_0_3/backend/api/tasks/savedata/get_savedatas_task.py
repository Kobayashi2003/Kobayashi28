from api import celery
from api.database import get_savedata, get_savedatas

@celery.task(bind=True)
def get_savedatas_task(self, vnid):
    self.update_state(state='PROGRESS', meta={'status': 'Retrieving savedatas...'})

    savedatas = get_savedatas(vnid)

    return {
        "status": "SUCCESS" if savedatas else "NOT_FOUND",
        "result": savedatas if savedatas else None
    }