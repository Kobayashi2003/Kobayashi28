from typing import List, Dict, Any, Optional
from datetime import datetime, timezone 

from sqlalchemy import asc, desc
from sqlalchemy.orm import joinedload 

from api import db
from .common import db_transaction
from ..models import MODEL_MAP, META_MODEL_MAP, ModelType, MetaModelType

def exists(type: str, id: str) -> bool:
    model = MODEL_MAP.get(type)
    meta_model = META_MODEL_MAP.get(type)
    if not model or not meta_model:
        raise ValueError(f"Invalid model type: {type}")
    metadata = meta_model.query.filter_by(id=id).first()
    return metadata is not None and metadata.is_active

def count(type: str) -> bool:
    meta_model = META_MODEL_MAP.get(type)
    if not meta_model:
        raise ValueError(f"Invalid model type: {type}")
    return meta_model.query.filter_by(is_active=True).count()

def create(type: str, id: str, data: Dict[str, Any]) -> Optional[ModelType]:
    model = MODEL_MAP.get(type)
    meta_model = META_MODEL_MAP.get(type)
    if not model or not meta_model: 
        raise ValueError(f"Invalid model type: {type}")
    data.pop('id', None)

    if exists(type, id):
        return None

    model.query.filter_by(id=id).delete()
    meta_model.query.filter_by(id=id).delete()

    item = model(id=id, **data)
    db.session.add(item)

    metadata_item = meta_model(id=id)
    setattr(item, f"{type}_metadata", metadata_item)

    return item

def update(type: str, id: str, data: Dict[str, Any]) -> Optional[ModelType]:
    model = MODEL_MAP.get(type)
    meta_model = META_MODEL_MAP.get(type)
    if not model or not meta_model:
        raise ValueError(f"Invalid model type: {type}")

    item = model.query.get(id)
    if not item:
        return None

    for key, value in data.items():
        setattr(item, key, value)
            
    metadata_attr = f"{type}_metadata"
    metadata_item = getattr(item, metadata_attr, None)
    if metadata_item is None:
        metadata_item = meta_model(id=id)
        setattr(item, metadata_attr, metadata_item)
    metadata_item.last_modified_at = datetime.now(timezone.utc)
    metadata_item.is_active = True
    
    return item

def delete(type: str, id: str) -> Optional[ModelType]:
    model = MODEL_MAP.get(type)
    meta_model = META_MODEL_MAP.get(type)
    if not model or not meta_model:
        raise ValueError(f"Invalid model type: {type}")

    item = model.query.get(id)
    if not item:
        return None 

    metadata_attr = f"{type}_metadata"
    metadata_item = getattr(item, metadata_attr, None)

    if metadata_item and metadata_item.is_active:
        metadata_item.is_active = False
    else:
        db.session.delete(item)

    return item

def delete_all(type: str) -> int:
    model = MODEL_MAP.get(type)
    meta_model = META_MODEL_MAP.get(type)
    if not model or not meta_model:
        raise ValueError(f"Invalid model type: {type}")

    count = meta_model.query.filter_by(is_active=True).count()

    meta_model.query.update({meta_model.is_active: False}, synchronize_session=False)
    model.query.filter(~model.id.in_(db.session.query(meta_model.id).filter_by(is_active=True))).delete(synchronize_session=False)

    return count

def get(type: str, id: str) -> Optional[ModelType]:
    model = MODEL_MAP.get(type)
    meta_model = META_MODEL_MAP.get(type)
    if not model or not meta_model:
        raise ValueError(f"Invalid model type: {type}")

    metadata_attr = f"{type}_metadata"

    item = (
        db.session.query(model)
        .options(joinedload(getattr(model, metadata_attr)))
        .filter(model.id == id)
        .filter(getattr(meta_model, 'is_active') == True)
        .first()
    )

    return item if item else None

def get_all(type: str, page: Optional[int] = None, limit: Optional[int] = None, sort: str = 'id', reverse: bool = False) -> List[ModelType]:
    model = MODEL_MAP.get(type)
    meta_model = META_MODEL_MAP.get(type)
    if not model or not meta_model:
        raise ValueError(f"Invalid model type: {type}")

    metadata_attr = f"{type}_metadata"

    query = (
        db.session.query(model)
        .join(getattr(model, metadata_attr))
        .filter(getattr(meta_model, 'is_active') == True)
    )

    order_func = desc if reverse else asc
    query = query.order_by(order_func(getattr(model, sort)))

    if page and limit:
        page = max(1, page) 
        limit = min(max(1, limit), 100)
        query = query.offset((page - 1) * limit).limit(limit)

    query = query.options(joinedload(getattr(model, metadata_attr)))

    return query.all()

def cleanup(type: str, id: str) -> Optional[ModelType]:
    item = get_inactive(type, id)
    if not item:
        return None
    return delete(type, id)

def cleanup_type(type: str) -> int:
    model = MODEL_MAP.get(type)
    meta_model = META_MODEL_MAP.get(type)
    if not model or not meta_model:
        raise ValueError(f"Invalid model type: {type}")

    metadata_attr = f"{type}_metadata"

    active_ids = db.session.query(model.id).join(
        getattr(model, metadata_attr)
    ).filter(
        getattr(meta_model, 'is_active') == True
    ).subquery()

    deleted = db.session.query(model).filter(
        ~model.id.in_(active_ids)
    ).delete(synchronize_session=False)

    return deleted

def cleanup_all() -> Dict[str, int]:
    return { type: cleanup_type(type) for type in MODEL_MAP.keys() }

def recover(type: str, id: str) -> Optional[ModelType]:
    item = get_inactive(type, id)
    if not item:
        return None

    metadata_attr = f"{type}_metadata"
    metadata_model = getattr(item, metadata_attr)
    metadata_model.is_active = True
    metadata_model.last_modified_at = datetime.now(timezone.utc)

    return item

def recover_type(type: str) -> int:
    model = MODEL_MAP.get(type)
    meta_model = META_MODEL_MAP.get(type)
    if not model or not meta_model:
        raise ValueError("Invalid model type")

    count = meta_model.query.filter_by(is_active=False).count()
    meta_model.query.filter_by(is_active=False).update({
        meta_model.is_active: True,
        meta_model.last_modified_at: datetime.now(timezone.utc)
    }, synchronize_session=False)

    return count

def recover_all() -> Dict[str, int]:
    return { type: recover_type(type) for type in MODEL_MAP.keys() }

def get_inactive(type: str, id: str) -> Optional[ModelType]:
    model = MODEL_MAP.get(type)
    meta_model = META_MODEL_MAP.get(type)
    if not model or not meta_model:
        raise ValueError(f"Invalid model type: {type}")

    metadata_attr = f"{type}_metadata"

    item = (
        db.session.query(model)
        .options(joinedload(getattr(model, metadata_attr)))
        .filter(model.id == id)
        .filter(getattr(meta_model, 'is_active') == False)
        .first()
    )

    return item

def get_inactive_type(type: str, page: Optional[int] = None, limit: Optional[int] = None, sort: str = 'id', reverse: bool = False) -> List[ModelType]:
    model = MODEL_MAP.get(type)
    meta_model = META_MODEL_MAP.get(type)
    if not model or not meta_model:
        raise ValueError(f"Invalid model type: {type}")

    metadata_attr = f"{type}_metadata"

    query = (
        db.session.query(model)
        .join(getattr(model, metadata_attr))
        .filter(getattr(meta_model, 'is_active') == False)
    )

    order_func = desc if reverse else asc
    query = query.order_by(order_func(getattr(model, sort)))

    if page and limit:
        page = max(1, page)
        limit = min(max(1, limit), 100)
        query = query.offset((page - 1) * limit).limit(limit)

    query = query.options(joinedload(getattr(model, metadata_attr)))

    return query.all()

def get_inactive_all() -> Dict[str, List[ModelType]]:
    return { type: get_inactive_type(type) for type in MODEL_MAP.keys() }

@db_transaction
def create_save(*args, **kwargs) -> Optional[ModelType]: return create(*args, **kwargs)

@db_transaction
def update_save(*args, **kwargs) -> Optional[ModelType]: return update(*args, **kwargs)

@db_transaction
def delete_save(*args, **kwargs) -> Optional[ModelType]: return delete(*args, **kwargs)

@db_transaction
def delete_all_save(*args, **kwargs) -> int: return delete_all(*args, **kwargs)

@db_transaction
def get_save(*args, **kwargs) -> Optional[ModelType]: return get(*args, **kwargs)

@db_transaction
def get_all_save(*args, **kwargs) -> List[ModelType]: return get_all(*args, **kwargs)

@db_transaction
def cleanup_save(*args, **kwargs) -> int: return cleanup(*args, **kwargs)

@db_transaction
def cleanup_type_save(*args, **kwargs) -> int: return cleanup_type(*args, **kwargs)

@db_transaction
def cleanup_all_save(*args, **kwargs) -> Dict[str, int]: return cleanup_all(*args, **kwargs)

@db_transaction
def recover_save(*args, **kwargs) -> Optional[ModelType]: return recover(*args, **kwargs)

@db_transaction
def recover_type_save(*args, **kwargs) -> int: return recover_type(*args, **kwargs)

@db_transaction
def recover_all_save(*args, **kwargs) -> int: return recover_all(*args, **kwargs)

@db_transaction
def get_inactive_save(*args, **kwargs) -> Optional[ModelType]: return get_inactive(*args, **kwargs)

@db_transaction
def get_inactive_type_save(*args, **kwargs) -> List[ModelType]: return get_inactive_type(*args, **kwargs)

@db_transaction
def get_inactive_all_save(*args, **kwargs) -> List[ModelType]: return get_inactive_all(*args, **kwargs)

