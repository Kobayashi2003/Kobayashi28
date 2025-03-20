import time
import random
from vndb.search import search_remote
from vndb.database import MODEL_MAP, exists, create, update, updatable
from .common import hourly_task, clear_caches

@hourly_task
@clear_caches
def random_fetch_task():

    created = {}
    updated = {}

    def random_fetch(type: str):
        count = search_remote(type, {}, 'small', 1, 1, 'id', False, True)['count']
        ids = [str(id) for id in random.sample(range(1, count + 1), 10)]
        for id in ids:
            if not exists(type, id):
                remote_result = search_remote(type, {'id':id}, 'large')
                created[id] = (create(type, id, remote_result) is not None)
            elif updatable(type, id):
                remote_result = search_remote(type, {'id':id}, 'large')
                updated[id] = (update(type, id, remote_result) is not None)
            else:
                updated[id] = False

    for type in ['vn', 'release','character', 'producer', 'staff', 'tag', 'trait']:
        random_fetch(type)
        time.sleep(60)

    return {'created': created, 'updated': updated}

@hourly_task
@clear_caches
def random_update_task():
    updated = {}

    def random_update(type: str):
        model = MODEL_MAP[type]
        ids = [vn['id'] for vn in model.query.filter(model.deleted_at == None).order_by(model.id).limit(10).all()]
        for id in ids:
            if updatable(type, id):
                remote_result = search_remote(type, {'id':id}, 'large')
                updated[id] = (update(type, id, remote_result) is not None)
            else:
                updated[id] = False

    for type in ['vn', 'release','character', 'producer', 'staff', 'tag', 'trait']:
        random_update(type)
        time.sleep(60)

    return {'updated': updated}