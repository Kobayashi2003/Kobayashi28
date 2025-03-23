import time
import random
from vndb import celery
from vndb.search import search_remote
from vndb.database import MODEL_MAP, formatId, exists, create, update, updatable 

@celery.task
def random_fetch_task():

    created = {}
    updated = {}

    def random_fetch(type: str):
        count = search_remote(type, {}, 'small', 1, 1, 'id', False, True)['count']
        ids = [formatId(type, id) for id in random.sample(range(1, count + 1), 5)]
        for id in ids:
            if not exists(type, id):
                if remote_results := search_remote(type, {'id':id}, 'large')['results']:
                    created[id] = (create(type, id, remote_results[0]) is not None)
                else:
                    created[id] = False
            elif updatable(type, id):
                if remote_results := search_remote(type, {'id':id}, 'large')['results']:
                    updated[id] = (update(type, id, remote_results[0]) is not None)
                else:
                    updated[id] = False
            else:
                updated[id] = False
            time.sleep(10)
    
    for type in ['vn', 'release','character', 'producer', 'staff', 'tag', 'trait']:
        random_fetch(type)
        time.sleep(60)
    
    results = {'created': created, 'updated': updated}
    print(results)
    return results

@celery.task
def random_update_task():

    updated = {}

    def random_update(type: str):
        model = MODEL_MAP[type]
        ids = [vn.id for vn in model.query.filter(model.deleted_at == None).order_by(model.id).limit(5).all()]
        for id in ids:
            if updatable(type, id):
                if remote_results := search_remote(type, {'id':id}, 'large')['results']:
                    updated[id] = (update(type, id, remote_results[0]) is not None)
                else:
                    updated[id] = False
            else:
                updated[id] = False
            time.sleep(10)

    for type in ['vn', 'release','character', 'producer', 'staff', 'tag', 'trait']:
        random_update(type)
        time.sleep(60)

    results = {'updated': updated}
    print(results)
    return results