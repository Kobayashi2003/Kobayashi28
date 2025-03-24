import time
import random
from .common import hourly_task
from imgserve.database import IMAGE_MODEL, exists, create

@hourly_task()
def random_fetch_schedule():

    created = {}

    def random_fetch(type: str):
        model = IMAGE_MODEL[type]
        max_id = model.query.order_by(model.id.desc()).first()
        max_id = max_id.id if max_id else 0

        if max_id == 0:
            return
        
        ids = random.sample(range(1, max_id + 1), min(10, max_id))
        for id in ids:
            if not exists(type, id):
                try:
                    result = create(type, id)
                    created[f"{type}:{id}"] = (result is not None)
                except Exception as e:
                    print(f"Error creating {type}:{id}: {e}")
                    created[f"{type}:{id}"] = False
            else:
                created[f"{type}:{id}"] = False
            time.sleep(5)

    for type in ['cv', 'sf', 'cv.t', 'sf.t', 'ch']:
        random_fetch(type)
        time.sleep(60)

    print({'created': created})


@hourly_task()
def random_update_schedule():
    updated = {}

    def random_update(source_type: str, target_type: str):
        source_model = IMAGE_MODEL[source_type]
        
        source_items = source_model.query.all()
        source_ids = [item.id for item in source_items]
        
        missing_in_target = []
        for id in source_ids:
            if not exists(target_type, id):
                missing_in_target.append(id)
        
        if missing_in_target:
            selected_ids = random.sample(missing_in_target, min(10, len(missing_in_target)))
            for id in selected_ids:
                try:
                    result = create(target_type, id)
                    updated[f"{target_type}:{id}"] = (result is not None)
                except Exception as e:
                    print(f"Error creating {target_type}:{id}: {e}")
                    updated[f"{target_type}:{id}"] = False
                time.sleep(5)

    for source_type, target_type in [('cv.t', 'cv'), ('cv', 'cv.t'), ('sf.t', 'sf'), ('sf', 'sf.t')]:
        random_update(source_type, target_type)
        time.sleep(60)

    print({'updated': updated})