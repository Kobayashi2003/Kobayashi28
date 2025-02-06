def convert_remote_to_local(entity_type, remote_data):
    entity_type = entity_type.lower()
    local_data = remote_data.copy()
    
    local_data.pop('id', None)
    
    if entity_type == 'vn':
        for field in ['relation', 'relation_official', 'role', 'spoiler', 'release', 'rtype']:
            local_data.pop(field, None)
    
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
        ...
    
    else:
        raise ValueError(f"Unknown entity type: {entity_type}")
    
    return local_data