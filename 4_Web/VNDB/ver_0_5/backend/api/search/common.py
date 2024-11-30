def convert_remote_to_local(entity_type, remote_data):
    entity_type = entity_type.lower()
    local_data = remote_data.copy()
    
    local_data.pop('id', None)
    
    if entity_type == 'vn':
        devstatus_map = {0: 'Finished', 1: 'In development', 2: 'Cancelled'}
        local_data['devstatus'] = devstatus_map.get(local_data.get('devstatus'), 'Finished')
        
        for field in ['relation', 'relation_official', 'role', 'spoiler']:
            local_data.pop(field, None)
    
    elif entity_type == 'character':
        for field in ['role', 'spoiler']:
            local_data.pop(field, None)
    
    elif entity_type == 'staff':
        for field in ['eid', 'role']:
            local_data.pop(field, None)
    
    elif entity_type == 'tag':
        for field in ['rating', 'spoiler', 'lie']:
            local_data.pop(field, None)
    
    elif entity_type == 'trait':
        ...
    
    elif entity_type == 'producer':
        ...
    
    else:
        raise ValueError(f"Unknown entity type: {entity_type}")
    
    return local_data