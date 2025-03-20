import random
from vndb.search import search_remote
from vndb.database import VN, exists, create, update, updatable
from .common import hourly_task, clear_caches

@hourly_task
@clear_caches
def random_fetch():
    created = {}
    updated = {}
    count = search_remote('vn', {}, 'small', 1, 1, 'id', False, True)['count']
    ids = [f'v{id}' for id in random.sample(range(1, count + 1), 10)]
    for id in ids:
        if not exists('vn', id):
            remote_result = search_remote('vn', {'id':id}, 'large')
            created[id] = (create('vn', id, remote_result) is not None)
        elif updatable('vn', id):
            remote_result = search_remote('vn', {'id':id}, 'large')
            updated[id] = (update('vn', id, remote_result) is not None)
        else:
            updated[id] = False
    return {'created': created, 'updated': updated}

@hourly_task
@clear_caches
def random_update():
    updated = {}
    ids = [vn['id'] for vn in VN.query.filter(VN.deleted_at == None).order_by(VN.id).limit(10).all()]
    for id in ids:
        if updatable('vn', id):
            remote_result = search_remote('vn', {'id':id}, 'large')
            updated[id] = (update('vn', id, remote_result) is not None)
        else:
            updated[id] = False
    return {'updated': updated}