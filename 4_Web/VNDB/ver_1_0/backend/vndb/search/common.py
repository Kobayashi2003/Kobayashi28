import re

def process_resolution(resolution_value):
    if not resolution_value:
        return None
    return re.sub(r'\s', '', str(resolution_value))

def process_released(released_value):
    if not released_value:
        return None
    return re.sub(r'\s', '', str(released_value))

def process_birthday(birthday_value):
    if not birthday_value:
        return None
    return re.sub(r'\s', '', str(birthday_value))

def convert_remote_to_local(entity_type, remote_data):
    entity_type = entity_type.lower()
    local_data = remote_data.copy()
    
    local_data.pop('id', None)
    
    if entity_type == 'vn':
        for field in ['relation', 'relation_official', 'role', 'spoiler', 'release', 'rtype']:
            local_data.pop(field, None)
        local_data['released'] = process_released(local_data.pop('released'))
    
    elif entity_type == 'character':
        for field in ['role', 'spoiler']:
            local_data.pop(field, None)
        local_data['birthday'] = process_birthday(local_data.pop('birthday'))
    
    elif entity_type == 'staff':
        for field in ['eid', 'role', 'note']:
            local_data.pop(field, None)
    
    elif entity_type == 'tag':
        for field in ['rating', 'spoiler', 'lie']:
            local_data.pop(field, None)
    
    elif entity_type == 'trait':
        for field in ['spoiler', 'lie']:
            local_data.pop(field, None)
    
    elif entity_type == 'producer':
        for field in ['developer', 'publisher']:
            local_data.pop(field, None)

    elif entity_type == 'release':
        local_data['resolution'] = process_resolution(local_data.pop('resolution', None))
        local_data['released'] = process_released(local_data.pop('released'))
    
    else:
        raise ValueError(f"Unknown entity type: {entity_type}")
    
    return local_data