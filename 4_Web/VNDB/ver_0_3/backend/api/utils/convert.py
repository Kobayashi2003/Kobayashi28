def convert_model_to_dict(model):
    from sqlalchemy.inspection import inspect
    from datetime import datetime, date
    from ..database import models

    if model is None:
        return None
    if isinstance(model, list):
        return [convert_model_to_dict(item) for item in model]
    
    result = {}
    for column in inspect(model).mapper.column_attrs:
        value = getattr(model, column.key)
        if isinstance(value, (datetime, date)):
            value = value.isoformat()
        result[column.key] = value
    
    # Handle relationships
    if isinstance(model, models.VN):
        result['local_vn'] = convert_model_to_dict(model.local_vn)
    elif isinstance(model, models.Tag):
        result['local_tag'] = convert_model_to_dict(model.local_tag)
    elif isinstance(model, models.Producer):
        result['local_producer'] = convert_model_to_dict(model.local_producer)
    elif isinstance(model, models.Staff):
        result['local_staff'] = convert_model_to_dict(model.local_staff)
    elif isinstance(model, models.Character):
        result['local_character'] = convert_model_to_dict(model.local_character)
    elif isinstance(model, models.Trait):
        result['local_trait'] = convert_model_to_dict(model.local_trait)
    
    return result

def convert_remote_to_local(entity_type, remote_data):
    """
    Convert remote data to local database format.
    
    :param entity_type: String representing the type of entity (e.g., 'vn', 'character', etc.)
    :param remote_data: Dictionary containing the remote data
    :return: Dictionary with converted data ready for local database insertion
    """
    converters = {
        'vn': convert_vn,
        'character': convert_character,
        'producer': convert_producer,
        'staff': convert_staff,
        'tag': convert_tag,
        'trait': convert_trait
    }

    converter = converters.get(entity_type.lower())
    if not converter:
        raise ValueError(f"Unknown entity type: {entity_type}")

    remote_data.pop('id')
    
    return converter(remote_data)

def convert_vn(remote_data):
    local_data = remote_data.copy()
    
    # Convert devstatus
    devstatus_map = {0: 'Finished', 1: 'In development', 2: 'Cancelled'}
    local_data['devstatus'] = devstatus_map.get(remote_data.get('devstatus'), 'Finished')
    
    return local_data

def convert_character(remote_data): return remote_data

def convert_producer(remote_data): return remote_data

def convert_staff(remote_data): return remote_data

def convert_tag(remote_data): return remote_data

def convert_trait(remote_data): return remote_data