def process_released_date(released_value):
    if not released_value or released_value == "TBA":
        return [-1]  # Use [-1] to represent TBA or unknown dates

    parts = released_value.split('-')
    processed_parts = []
    
    for part in parts:
        try:
            processed_parts.append(int(part))
        except Exception:
            # If we can't convert a part to integer, we'll stop processing
            break
    
    return processed_parts if processed_parts else [-1]

def process_resolution(resolution_value):
    if not resolution_value or resolution_value == 'non-standard':
        return [-1]
    
    try:
        width, height = map(int, resolution_value.lower().split('x'))
        return [width, height]
    except Exception:
        return [-1] 

def convert_remote_to_local(entity_type, remote_data):
    entity_type = entity_type.lower()
    local_data = remote_data.copy()
    
    local_data.pop('id', None)
    
    if entity_type == 'vn':
        for field in ['relation', 'relation_official', 'role', 'spoiler', 'release', 'rtype']:
            local_data.pop(field, None)
        local_data['released'] = process_released_date(local_data.pop('released', None))
    
    elif entity_type == 'character':
        for field in ['role', 'spoiler']:
            local_data.pop(field, None)
    
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
        local_data['released'] = process_released_date(local_data.pop('released', None))
        local_data['resolution'] = process_resolution(local_data.pop('resolution', None))
    
    else:
        raise ValueError(f"Unknown entity type: {entity_type}")
    
    return local_data