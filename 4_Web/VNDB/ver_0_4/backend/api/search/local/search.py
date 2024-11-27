from typing import Dict, Any, Optional

from sqlalchemy import asc, desc

from api import db
from api.database.models import META_MODEL_MAP, MODEL_MAP

from .fields import get_local_fields
from .filters import get_local_filters

def search(resource_type: str, params: Dict[str, Any], response_size: str = 'small', 
           page: int = 1, limit: int = 100,
           sort: str = 'id', order: str = 'asc') -> Dict[str, Any]:

    model = MODEL_MAP.get(resource_type)
    meta_model = META_MODEL_MAP.get(resource_type)
    if not model or not meta_model:
        raise ValueError(f"Invalid model type: {resource_type}")

    active_metadata_query = db.session.query(meta_model.id).filter(meta_model.is_active == True)
    active_metadata_subquery = active_metadata_query.subquery()

    fields = get_local_fields(resource_type, response_size)
    filters = get_local_filters(resource_type, params)

    query = model.query.with_entities(*[getattr(model, field) for field in fields])
    query = query.filter(model.id.in_(active_metadata_subquery))

    for filter_condition in filters:
        query = query.filter(filter_condition)

    order_func = asc if order.lower() == 'asc' else desc
    query = query.order_by(order_func(getattr(model, sort)))

    page = max(1, page or 1)
    limit = min(max(1, limit or 20), 100)
    query = query.offset((page - 1) * limit).limit(limit)

    results = [dict(zip(fields, result)) for result in query.all()]

    total = active_metadata_query.count()
    more = (page * limit) < total

    return {
        "count": len(results),
        "total": total,
        "more": more,
        "result": results
    }