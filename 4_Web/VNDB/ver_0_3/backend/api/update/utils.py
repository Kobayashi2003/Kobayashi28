from datetime import datetime
from api.db.models import VN, Character, Producer, Staff, Tag, Trait

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

def convert_character(remote_data):
    local_data = remote_data.copy()
    
    return local_data

def convert_producer(remote_data):
    local_data = remote_data.copy()
    
    return local_data

def convert_staff(remote_data):
    local_data = remote_data.copy()
    
    return local_data

def convert_tag(remote_data):
    local_data = remote_data.copy()
    
    return local_data

def convert_trait(remote_data):

    return remote_data.copy()