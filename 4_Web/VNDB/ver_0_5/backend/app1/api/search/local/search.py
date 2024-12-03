from typing import Dict, Any

from sqlalchemy import asc, desc 

from api import db 
from api.database.models import META_MODEL_MAP, MODEL_MAP

from .fields import get_local_fields
from .filters import get_local_filters

def search(resource_type: str, params: Dict[str, Any], response_size: str = 'small', 
           page: int = 1, limit: int = 100,
           sort: str = 'id', reverse: bool = False, count: bool = True) -> Dict[str, Any]:

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

    total = query.count()
    more = (page * limit) < total

    order_func = desc if reverse else asc
    query = query.order_by(order_func(getattr(model, sort)))

    page = max(1, page or 1)
    limit = min(max(1, limit or 20), 100)
    query = query.offset((page - 1) * limit).limit(limit)

    results = [dict(zip(fields, result)) for result in query.all()]

    return {'results': results, 'more': more, 'count': total} if count else {'results': results, 'more': more}

def search_resources_by_vnid(vnid: str, related_resource_type: str, response_size: str = 'small',
                             page: int = 1, limit: int = 100, sort: str = 'id', reverse: bool = False, count: bool = True) -> Dict[str, Any]:
    
    VN = MODEL_MAP['vn']
    VNMetadata = META_MODEL_MAP['vn']

    vn_meta = VNMetadata.query.filter(VNMetadata.id == vnid, VNMetadata.is_active == True).first()
    if not vn_meta:
        raise ValueError(f"Active VN with id {vnid} not found")

    vn = VN.query.get(vnid)
    if not vn:
        raise ValueError(f"VN with id {vnid} not found")

    related_resource_ids = []
    if related_resource_type == 'vn':
        related_resource_ids = [relation['id'] for relation in vn.relations]
    elif related_resource_type == 'tag':
        related_resource_ids = [tag['id'] for tag in vn.tags]
    elif related_resource_type == 'producer':
        related_resource_ids = [dev['id'] for dev in vn.developers]
    elif related_resource_type == 'staff':
        related_resource_ids = [staff['id'] for staff in vn.staff]
    elif related_resource_type == 'character':
        related_resource_ids = [char['id'] for char in vn.characters]
    elif related_resource_type == 'release':
        related_resource_ids = [release['id'] for release in vn.releases]
    else:
        raise ValueError(f"Invalid related_resource_type: {related_resource_type}")
    
    if not related_resource_ids:
        return {'results': [], 'more': False, 'count': 0} if count else {'results': [], 'more': False}

    model = MODEL_MAP.get(related_resource_type)
    meta_model = META_MODEL_MAP.get(related_resource_type)
    if not model or not meta_model:
        raise ValueError(f"Invalid model type: {related_resource_type}")

    fields = get_local_fields(related_resource_type, response_size)
    query = model.query.with_entities(*[getattr(model, field) for field in fields])

    active_metadata_query = db.session.query(meta_model.id).filter(meta_model.is_active == True)
    active_metadata_subquery = active_metadata_query.subquery()
    query = query.filter(model.id.in_(active_metadata_subquery))
    query = query.filter(model.id.in_(related_resource_ids))

    order_func = desc if reverse else asc
    query = query.order_by(order_func(getattr(model, sort)))

    page = max(1, page)
    limit = min(max(1, limit), 100)
    query = query.offset((page - 1) * limit).limit(limit)

    results = [dict(zip(fields, result)) for result in query.all()]

    total = query.count()
    more = (page * limit) < total

    return {'results': results, 'more': more, 'count': total} if count else {'results': results, 'more': more}

def search_resources_by_charid(charid: str, related_resource_type: str, response_size: str = 'small',
                               page: int = 1, limit: int = 100, sort: str = 'id', reverse: bool = False, count: bool = True) -> Dict[str, Any]:
    Character = MODEL_MAP['character']
    CharacterMetadata = META_MODEL_MAP['character']

    character_meta = CharacterMetadata.query.filter(CharacterMetadata.id == charid, CharacterMetadata.is_active == True).first()
    if not character_meta:
        raise ValueError(f"Active Character with id {charid} not found")

    character = Character.query.get(charid)
    if not character:
        raise ValueError(f"Character with id {charid} not found")

    related_resource_ids = []
    if related_resource_type == 'vn':
        related_resource_ids = [vn['id'] for vn in character.vns]
    elif related_resource_type == 'trait':
        related_resource_ids = [trait['id'] for trait in character.traits]
    else:
        raise ValueError(f"Invalid related_resource_type: {related_resource_type}")
    
    if not related_resource_ids:
        return {'results': [], 'more': False, 'count': 0} if count else {'results': [], 'more': False}

    model = MODEL_MAP.get(related_resource_type)
    meta_model = META_MODEL_MAP.get(related_resource_type)
    if not model or not meta_model:
        raise ValueError(f"Invalid model type: {related_resource_type}")

    fields = get_local_fields(related_resource_type, response_size)
    query = model.query.with_entities(*[getattr(model, field) for field in fields])

    active_metadata_query = db.session.query(meta_model.id).filter(meta_model.is_active == True)
    active_metadata_subquery = active_metadata_query.subquery()
    query = query.filter(model.id.in_(active_metadata_subquery))
    query = query.filter(model.id.in_(related_resource_ids))

    order_func = desc if reverse else asc
    query = query.order_by(order_func(getattr(model, sort)))

    page = max(1, page)
    limit = min(max(1, limit), 100)
    query = query.offset((page - 1) * limit).limit(limit)

    results = [dict(zip(fields, result)) for result in query.all()]

    total = query.count()
    more = (page * limit) < total

    return {'results': results, 'more': more, 'count': total} if count else {'results': results, 'more': more}

def search_resources_by_release_id(release_id: str, related_resource_type: str, response_size: str = 'small',
                                   page: int = 1, limit: int = 100, sort: str = 'id', reverse: bool = False, count: bool = True) -> Dict[str, Any]:
    Release = MODEL_MAP['release']
    ReleaseMetadata = META_MODEL_MAP['release']

    release_meta = ReleaseMetadata.query.filter(ReleaseMetadata.id == release_id, ReleaseMetadata.is_active == True).first()
    if not release_meta:
        raise ValueError(f"Active Release with id {release_id} not found")

    release = Release.query.get(release_id)
    if not release:
        raise ValueError(f"Release with id {release_id} not found")

    related_resource_ids = []
    if related_resource_type == 'vn':
        related_resource_ids = [vn['id'] for vn in release.vns]
    elif related_resource_type == 'producer':
        related_resource_ids = [producer['id'] for producer in release.producers]
    else:
        raise ValueError(f"Invalid related_resource_type: {related_resource_type}")
    
    if not related_resource_ids:
        return {'results': [], 'more': False, 'count': 0} if count else {'results': [], 'more': False}

    model = MODEL_MAP.get(related_resource_type)
    meta_model = META_MODEL_MAP.get(related_resource_type)
    if not model or not meta_model:
        raise ValueError(f"Invalid model type: {related_resource_type}")

    fields = get_local_fields(related_resource_type, response_size)
    query = model.query.with_entities(*[getattr(model, field) for field in fields])

    active_metadata_query = db.session.query(meta_model.id).filter(meta_model.is_active == True)
    active_metadata_subquery = active_metadata_query.subquery()
    query = query.filter(model.id.in_(active_metadata_subquery))
    query = query.filter(model.id.in_(related_resource_ids))

    order_func = desc if reverse else asc
    query = query.order_by(order_func(getattr(model, sort)))

    page = max(1, page)
    limit = min(max(1, limit), 100)
    query = query.offset((page - 1) * limit).limit(limit)

    results = [dict(zip(fields, result)) for result in query.all()]

    total = query.count()
    more = (page * limit) < total

    return {'results': results, 'more': more, 'count': total} if count else {'results': results, 'more': more}

def search_vns_by_resource_id(resource_type: str, resource_id: str, response_size: str = 'small',
                              page: int = 1, limit: int = 100, sort: str = 'id', reverse: bool = False, count: bool = True) -> Dict[str, Any]:
    params = {{
        'tag': 'tag',
        'character': 'character',
        'staff': 'staff',
        'producer': 'developer',
        'release': 'release'
    }.get(resource_type) : resource_id}

    results = search(resource_type='vn', params=params, response_size=response_size, 
                     page=page, limit=limit, sort=sort, reverse=reverse, count=count)

    return results

def search_characters_by_resource_id(resource_type: str, resource_id: str, response_size: str = 'small',
                                     page: int = 1, limit: int = 100, sort: str = 'id', reverse: bool = False, count: bool = True) -> Dict[str, Any]:
    params = {{
        'vn': 'vn',
        'trait': 'trait'
    }.get(resource_type) : resource_id}

    results = search(resource_type='character', params=params, response_size=response_size, 
                     page=page, limit=limit, sort=sort, reverse=reverse, count=count)

    return results

def search_releases_by_resource_id(resource_type: str, resource_id: str, response_size: str = 'small',
                                   page: int = 1, limit: int = 100, sort: str = 'id', reverse: bool = False, count: bool = True) -> Dict[str, Any]:
    params = {
        'vn': 'vn',
        'producer': 'producer'
    }.get(resource_type)

    if params is None:
        raise ValueError(f"Invalid resource_type: {resource_type}")

    results = search(resource_type='release', params={params: resource_id}, response_size=response_size, 
                     page=page, limit=limit, sort=sort, reverse=reverse, count=count)

    return results