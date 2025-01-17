from typing import List, Dict, Any, Optional
from datetime import datetime, timezone 

from sqlalchemy import asc, desc
from sqlalchemy.orm import joinedload, contains_eager 

from api import db
from .common import db_transaction
from ..models import MODEL_MAP, META_MODEL_MAP, ModelType, MetaModelType

def exists(type: str, id: str) -> bool:
    model = MODEL_MAP[type]
    item = db.session.query(model).options(joinedload(model.meta)).get(id)
    return item is not None and item.meta is not None and item.meta.is_active

def count_all(type: str) -> int:
    model = MODEL_MAP[type]
    return db.session.query(model).join(model.meta).filter(model.meta.has(is_active=True)).count()

def get(type: str, id: str) -> Optional[ModelType]:
    model = MODEL_MAP[type]
    
    item = (
        db.session.query(model)
        .options(joinedload(model.meta))
        .filter(model.id == id)
        .filter(model.meta.has(is_active=True))
        .first()
    )

    return item

def get_all(type: str, page: Optional[int] = None, limit: Optional[int] = None, sort: str = 'id', reverse: bool = False) -> List[ModelType]:
    model = MODEL_MAP[type]

    query = (
        db.session.query(model)
        .join(model.meta)
        .options(contains_eager(model.meta))
        .filter(model.meta.has(is_active=True))
    )

    order_func = desc if reverse else asc
    query = query.order_by(order_func(getattr(model, sort)))

    if page and limit:
        page = max(1, page) 
        limit = min(max(1, limit), 100)
        query = query.offset((page - 1) * limit).limit(limit)

    return query.all()

def create(type: str, id: str, data: Dict[str, Any]) -> Optional[ModelType]:
    model = MODEL_MAP[type]
    meta_model = META_MODEL_MAP[type]
    data.pop('id', None)

    if exists(type, id):
        return None

    # Use cleanup to ensure deletion of any existing inactive items
    cleanup(type, id)

    item = model(id=id, **data)
    metadata_item = meta_model(id=id)
    item.meta = metadata_item

    db.session.add(item)
    db.session.flush()

    return item

def update(type: str, id: str, data: Dict[str, Any]) -> Optional[ModelType]:
    item = get(type, id)
    if not item:
        return None

    for key, value in data.items():
        setattr(item, key, value)
            
    item.meta.last_modified_at = datetime.now(timezone.utc)
    
    db.session.flush()
    return item

def delete(type: str, id: str) -> Optional[ModelType]:
    item = get(type, id)
    if not item:
        return None 

    item.meta.is_active = False
    item.meta.last_modified_at = datetime.now(timezone.utc)

    db.session.flush()
    return item

def delete_all(type: str) -> int:
    items = get_all(type)
    count = len(items)

    current_time = datetime.now(timezone.utc)
    for item in items:
        item.meta.is_active = False
        item.meta.last_modified_at = current_time

    db.session.flush()
    return count


def get_inactive(type: str, id: str) -> Optional[ModelType]:
    model = MODEL_MAP[type]

    item = (
        db.session.query(model)
        .options(joinedload(model.meta))
        .filter(model.id == id)
        .filter(model.meta.has(is_active=False))
        .first()
    )

    return item

def get_inactive_all(type: str, page: Optional[int] = None, limit: Optional[int] = None, sort: str = 'id', reverse: bool = False) -> List[ModelType]:
    model = MODEL_MAP[type]

    query = (
        db.session.query(model)
        .join(model.meta)
        .options(contains_eager(model.meta))
        .filter(model.meta.has(is_active=False))
    )

    order_func = desc if reverse else asc
    query = query.order_by(order_func(getattr(model, sort)))

    if page and limit:
        page = max(1, page)
        limit = min(max(1, limit), 100)
        query = query.offset((page - 1) * limit).limit(limit)

    return query.all()

def recover(type: str, id: str) -> Optional[ModelType]:
    item = get_inactive(type, id)
    if not item:
        return None

    item.meta.is_active = True
    item.meta.last_modified_at = datetime.now(timezone.utc)

    db.session.flush()
    return item

def recover_all(type: str) -> int:
    items = get_inactive_all(type)
    count = len(items)
    
    current_time = datetime.now(timezone.utc)
    for item in items:
        item.meta.is_active = True
        item.meta.last_modified_at = current_time
    
    db.session.flush()
    return count

def cleanup(type: str, id: str) -> Optional[ModelType]:
    item = get_inactive(type, id)
    if not item:
        return None
    
    db.session.delete(item)
    db.session.flush()
    
    return item

def cleanup_all(type: str) -> int:
    items = get_inactive_all(type)
    count = len(items)
    
    for item in items:
        db.session.delete(item)
    
    db.session.flush()
    return count


@db_transaction
def get_save(*args, **kwargs) -> Optional[ModelType]: return get(*args, **kwargs)

@db_transaction
def get_all_save(*args, **kwargs) -> List[ModelType]: return get_all(*args, **kwargs)

@db_transaction
def create_save(*args, **kwargs) -> Optional[ModelType]: return create(*args, **kwargs)

@db_transaction
def update_save(*args, **kwargs) -> Optional[ModelType]: return update(*args, **kwargs)

@db_transaction
def delete_save(*args, **kwargs) -> Optional[ModelType]: return delete(*args, **kwargs)

@db_transaction
def delete_all_save(*args, **kwargs) -> int: return delete_all(*args, **kwargs)


@db_transaction
def get_inactive_save(*args, **kwargs) -> Optional[ModelType]: return get_inactive(*args, **kwargs)

@db_transaction
def get_inactive_all_save(*args, **kwargs) -> List[ModelType]: return get_inactive_all(*args, **kwargs)

@db_transaction
def recover_save(*args, **kwargs) -> Optional[ModelType]: return recover(*args, **kwargs)

@db_transaction
def recover_all_save(*args, **kwargs) -> int: return recover_all(*args, **kwargs)

@db_transaction
def cleanup_save(*args, **kwargs) -> int: return cleanup(*args, **kwargs)

@db_transaction
def cleanup_all_save(*args, **kwargs) -> Dict[str, int]: return cleanup_all(*args, **kwargs)