import re
from typing import Any 
from datetime import datetime, timezone, timedelta
from functools import wraps

from sqlalchemy import asc, desc

from vndb import db
from .models import MODEL_MAP, ModelType 


def db_transaction(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            with db.session.begin_nested():
                result = func(*args, **kwargs)
            if result is None:
                return None
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            print(f"Error in {func.__name__}: {str(e)}")
            return None
    return wrapper


def formatId(type: str, id: str) -> str:
    type_prefix = {
        'vn': 'v',
        'release': 'r',
        'character': 'c',
        'producer': 'p',
        'staff': 's',
        'tag': 'g',
        'trait': 'i'
    }[type]
    id = str(id)
    if re.match(r'^\d+$', id):
        return f"{type_prefix}{id}"
    if re.match(r'^[a-zA-Z]\d+$', id):
        if id[:1] not in type_prefix:
            raise ValueError(f"Invalid ID: {id}")
        return id
    raise ValueError(f"Invalid ID: {id}")

def exists(type: str, id: str) -> bool:
    id = formatId(type, id)
    model = MODEL_MAP[type]
    item = db.session.query(model).get(id)
    return item is not None and item.deleted_at is None

def count_all(type: str) -> int:
    model = MODEL_MAP[type]
    return db.session.query(model).filter(model.deleted_at == None).count()

def updatable(type: str, id: str, update_interval: timedelta = timedelta(minutes=10)) -> bool:
    id = formatId(type, id)
    item = get(type, id)
    if not item:
        return True  # Allow update if item doesn't exist (it will be created)
    if item.deleted_at is not None:
        return True  # Allow update if item is deleted
    if item.updated_at is None:
        return True  # Allow update if item has never been updated
    return datetime.now(timezone.utc) - item.updated_at > update_interval


def get(type: str, id: str) -> ModelType | None:
    id = formatId(type, id)
    model = MODEL_MAP[type]
    item = (
        db.session.query(model)
        .filter(model.id == id)
        .filter(model.deleted_at == None)
        .first()
    )
    return item

def get_all(type: str, page: int | None = None, limit: int | None = None, sort: str = 'id', reverse: bool = False) -> list[ModelType]:
    model = MODEL_MAP[type]
    query = db.session.query(model).filter(model.deleted_at == None)
    order_func = desc if reverse else asc
    query = query.order_by(order_func(getattr(model, sort)))
    if page and limit:
        page = max(1, page) 
        limit = min(max(1, limit), 100)
        query = query.offset((page - 1) * limit).limit(limit)
    return query.all()

def create(type: str, id: str, data: dict[str, Any]) -> ModelType | None:
    id = formatId(type, id)
    model = MODEL_MAP[type]
    data.pop('id', None)
    if exists(type, id):
        return None
    # Use cleanup to ensure deletion of any existing inactive items
    cleanup(type, id)
    item = model(id=id, **data)
    db.session.add(item)
    db.session.flush()
    return item

def update(type: str, id: str, data: dict[str, Any]) -> ModelType | None:
    id = formatId(type, id)
    item = get(type, id)
    if not item:
        return None
    for key, value in data.items():
        setattr(item, key, value)
    item.updated_at = datetime.now(timezone.utc)
    db.session.flush()
    return item

def delete(type: str, id: str) -> ModelType | None:
    id = formatId(type, id)
    item = get(type, id)
    if not item:
        return None 
    item.deleted_at = datetime.now(timezone.utc)
    db.session.flush()
    return item

def delete_all(type: str) -> int:
    model = MODEL_MAP[type]
    current_time = datetime.now(timezone.utc)
    count = (
        db.session.query(model)
        .filter(model.deleted_at == None)
        .update({model.deleted_at: current_time})
    )
    db.session.flush()
    return count


def get_inactive(type: str, id: str) -> ModelType | None:
    id = formatId(type, id)
    model = MODEL_MAP[type]
    item = (
        db.session.query(model)
        .filter(model.id == id)
        .filter(model.deleted_at != None)
        .first()
    )
    return item

def get_inactive_all(type: str, page: int | None = None, limit: int | None = None, sort: str = 'id', reverse: bool = False) -> list[ModelType]:
    model = MODEL_MAP[type]
    query = db.session.query(model).filter(model.deleted_at != None)
    order_func = desc if reverse else asc
    query = query.order_by(order_func(getattr(model, sort)))
    if page and limit:
        page = max(1, page)
        limit = min(max(1, limit), 100)
        query = query.offset((page - 1) * limit).limit(limit)
    return query.all()

def recover(type: str, id: str) -> ModelType | None:
    id = formatId(type, id)
    item = get_inactive(type, id)
    if not item:
        return None
    item.deleted_at = None
    db.session.flush()
    return item

def recover_all(type: str) -> int:
    model = MODEL_MAP[type]
    count = (
        db.session.query(model)
        .filter(model.deleted_at != None)
        .update({model.deleted_at: None})
    )
    db.session.flush()
    return count

def cleanup(type: str, id: str) -> ModelType | None:
    id = formatId(type, id)
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
def get_save(*args, **kwargs) -> ModelType | None: return get(*args, **kwargs)

@db_transaction
def get_all_save(*args, **kwargs) -> list[ModelType]: return get_all(*args, **kwargs)

@db_transaction
def create_save(*args, **kwargs) -> ModelType | None: return create(*args, **kwargs)

@db_transaction
def update_save(*args, **kwargs) -> ModelType | None: return update(*args, **kwargs)

@db_transaction
def delete_save(*args, **kwargs) -> ModelType | None: return delete(*args, **kwargs)

@db_transaction
def delete_all_save(*args, **kwargs) -> int: return delete_all(*args, **kwargs)


@db_transaction
def get_inactive_save(*args, **kwargs) -> ModelType | None: return get_inactive(*args, **kwargs)

@db_transaction
def get_inactive_all_save(*args, **kwargs) -> list[ModelType]: return get_inactive_all(*args, **kwargs)

@db_transaction
def recover_save(*args, **kwargs) -> ModelType | None: return recover(*args, **kwargs)

@db_transaction
def recover_all_save(*args, **kwargs) -> int: return recover_all(*args, **kwargs)

@db_transaction
def cleanup_save(*args, **kwargs) -> int: return cleanup(*args, **kwargs)

@db_transaction
def cleanup_all_save(*args, **kwargs) -> dict[str, int]: return cleanup_all(*args, **kwargs)