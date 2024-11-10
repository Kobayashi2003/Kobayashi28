from typing import Dict, Any, List
from api.db.models import VN, Tag, Producer, Staff, Character, Trait
from api.search.local.fields import get_local_fields
from api.search.local.filters import get_local_filters

def search_vn(params: Dict[str, Any], response_size: str = 'small') -> List[Dict[str, Any]]:
    fields = get_local_fields('vn', response_size)
    filters = get_local_filters('vn', params)
    query = VN.query.with_entities(*[getattr(VN, field) for field in fields])
    for filter_condition in filters:
        query = query.filter(filter_condition)
    return [dict(zip(fields, result)) for result in query.all()]

def search_character(params: Dict[str, Any], response_size: str = 'small') -> List[Dict[str, Any]]:
    fields = get_local_fields('character', response_size)
    filters = get_local_filters('character', params)
    query = Character.query.with_entities(*[getattr(Character, field) for field in fields])
    for filter_condition in filters:
        query = query.filter(filter_condition)
    return [dict(zip(fields, result)) for result in query.all()]

def search_tag(params: Dict[str, Any], response_size: str = 'small') -> List[Dict[str, Any]]:
    fields = get_local_fields('tag', response_size)
    filters = get_local_filters('tag', params)
    query = Tag.query.with_entities(*[getattr(Tag, field) for field in fields])
    for filter_condition in filters:
        query = query.filter(filter_condition)
    return [dict(zip(fields, result)) for result in query.all()]

def search_producer(params: Dict[str, Any], response_size: str = 'small') -> List[Dict[str, Any]]:
    fields = get_local_fields('producer', response_size)
    filters = get_local_filters('producer', params)
    query = Producer.query.with_entities(*[getattr(Producer, field) for field in fields])
    for filter_condition in filters:
        query = query.filter(filter_condition)
    return [dict(zip(fields, result)) for result in query.all()]

def search_staff(params: Dict[str, Any], response_size: str = 'small') -> List[Dict[str, Any]]:
    fields = get_local_fields('staff', response_size)
    filters = get_local_filters('staff', params)
    query = Staff.query.with_entities(*[getattr(Staff, field) for field in fields])
    for filter_condition in filters:
        query = query.filter(filter_condition)
    return [dict(zip(fields, result)) for result in query.all()]

def search_trait(params: Dict[str, Any], response_size: str = 'small') -> List[Dict[str, Any]]:
    fields = get_local_fields('trait', response_size)
    filters = get_local_filters('trait', params)
    query = Trait.query.with_entities(*[getattr(Trait, field) for field in fields])
    for filter_condition in filters:
        query = query.filter(filter_condition)
    return [dict(zip(fields, result)) for result in query.all()]

def search(search_type: str, params: Dict[str, Any], response_size: str = 'small') -> List[Dict[str, Any]]:
    search_functions = {
        'vn': search_vn,
        'character': search_character,
        'tag': search_tag,
        'producer': search_producer,
        'staff': search_staff,
        'trait': search_trait
    }

    if search_type not in search_functions:
        raise ValueError(f"Invalid search type: {search_type}")
    
    return search_functions[search_type](params, response_size)