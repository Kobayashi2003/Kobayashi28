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

def _create(type: str, id: str, data: Dict[str, Any]) -> Optional[ModelType]:
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

def _update(type: str, id: str, data: Dict[str, Any]) -> Optional[ModelType]:
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

def _delete(type: str, id: str) -> Optional[ModelType]:
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

def _delete_all(type: str) -> int:
    model = MODEL_MAP.get(type)
    meta_model = META_MODEL_MAP.get(type)
    if not model or not meta_model:
        raise ValueError(f"Invalid model type: {type}")

    # Count the number of active items
    count = meta_model.query.filter_by(is_active=True).count()

    # Bulk update to set is_active to False for all metadata items
    meta_model.query.update({meta_model.is_active: False}, synchronize_session=False)
    # Delete all items that are not in the active metadata items
    model.query.filter(~model.id.in_(db.session.query(meta_model.id).filter_by(is_active=True))).delete(synchronize_session=False)

    return count

def _get(type: str, id: str) -> Optional[ModelType]:
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

def _get_all(type: str, page: Optional[int] = None, limit: Optional[int] = None, sort: str = 'id', reverse: bool = False) -> List[ModelType]:
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

def _cleanup(type: str, id: str) -> Optional[ModelType]:
    item = _get_inactive(type, id)
    if not item:
        return None
    return _delete(type, id)

def _cleanup_type(type: str) -> int:
    model = MODEL_MAP.get(type)
    meta_model = META_MODEL_MAP.get(type)
    if not model or not meta_model:
        raise ValueError(f"Invalid model type: {type}")

    metadata_attr = f"{type}_metadata"

    # Subquery to get IDs of items with active metadata
    active_ids = db.session.query(model.id).join(
        getattr(model, metadata_attr)
    ).filter(
        getattr(meta_model, 'is_active') == True
    ).subquery()

    # Delete items that are not in the active_ids subquery
    deleted = db.session.query(model).filter(
        ~model.id.in_(active_ids)
    ).delete(synchronize_session=False)

    return deleted

def _cleanup_all() -> Dict[str, int]:
    return { type: cleanup(type) for type in MODEL_MAP.keys() }

def _recover(type: str, id: str) -> Optional[ModelType]:
    item = _get_inactive(type, id)
    if not item:
        return None

    metadata_attr = f"{type}_metadata"
    metadata_model = getattr(item, metadata_attr)
    metadata_model.is_active = True
    metadata_model.last_modified_at = datetime.now(timezone.utc)

    return item

def _recover_type(type: str) -> int:
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

def _recover_all() -> Dict[str, int]:
    return { type: _recover_type(type) for type in MODEL_MAP.keys() }

def _get_inactive(type: str, id: str) -> Optional[ModelType]:
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

def _get_inactive_type(type: str, page: Optional[int] = None, limit: Optional[int] = None, sort: str = 'id', reverse: bool = False) -> List[ModelType]:
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

def _get_inactive_all() -> Dict[str, List[ModelType]]:
    return { type: get_inactive_type(type) for type in MODEL_MAP.keys() }

@db_transaction
def create(*args, **kwargs) -> Optional[ModelType]: return _create(*args, **kwargs)

@db_transaction
def update(*args, **kwargs) -> Optional[ModelType]: return _update(*args, **kwargs)

@db_transaction
def delete(*args, **kwargs) -> Optional[ModelType]: return _delete(*args, **kwargs)

@db_transaction
def delete_all(*args, **kwargs) -> int: return _delete_all(*args, **kwargs)

@db_transaction
def get(*args, **kwargs) -> Optional[ModelType]: return _get(*args, **kwargs)

@db_transaction
def get_all(*args, **kwargs) -> List[ModelType]: return _get_all(*args, **kwargs)

@db_transaction
def cleanup(*args, **kwargs) -> int: return _cleanup(*args, **kwargs)

@db_transaction
def cleanup_type(*args, **kwargs) -> int: return _cleanup_type(*args, **kwargs)

@db_transaction
def cleanup_all(*args, **kwargs) -> Dict[str, int]: return _cleanup_all(*args, **kwargs)

@db_transaction
def recover(*args, **kwargs) -> Optional[ModelType]: return _recover(*args, **kwargs)

@db_transaction
def recover_type(*args, **kwargs) -> int: return _recover_type(*args, **kwargs)

@db_transaction
def recover_all(*args, **kwargs) -> int: return _recover_all(*args, **kwargs)

@db_transaction
def get_inactive(*args, **kwargs) -> Optional[ModelType]: return _get_inactive(*args, **kwargs)

@db_transaction
def get_inactive_type(*args, **kwargs) -> List[ModelType]: return _get_inactive_type(*args, **kwargs)

@db_transaction
def get_inactive_all(*args, **kwargs) -> List[ModelType]: return _get_inactive_all(*args, **kwargs)
