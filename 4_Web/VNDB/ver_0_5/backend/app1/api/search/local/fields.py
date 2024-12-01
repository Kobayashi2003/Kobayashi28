from typing import List

from api.database.models import VN, Tag, Producer, Staff, Character, Trait, Release

class LocalFields:
    VN = [column.key for column in VN.__table__.columns]
    TAG = [column.key for column in Tag.__table__.columns]
    PRODUCER = [column.key for column in Producer.__table__.columns]
    STAFF = [column.key for column in Staff.__table__.columns]
    CHARACTER = [column.key for column in Character.__table__.columns]
    TRAIT = [column.key for column in Trait.__table__.columns]
    RELEASE = [column.key for column in Release.__table__.columns]

    SMALL_VN = ['id', 'title', 'released', 'image']
    SMALL_CHARACTER = ['id', 'name']
    SMALL_TAG = ['id', 'name']
    SMALL_PRODUCER = ['id', 'name']
    SMALL_STAFF = ['id', 'name']
    SMALL_TRAIT = ['id', 'name', 'group_id', 'group_name']
    SMALL_RELEASE = ['id', 'title', 'released']

    @staticmethod
    def get_fields(model_name: str) -> list:
        return getattr(LocalFields, model_name.upper(), [])

def get_local_fields(search_type: str, response_size: str = 'small') -> List[str]:
    """
    Get the appropriate fields for a local database search based on the search type and response size.

    Args:
        search_type (str): The type of entity to search for ('vn', 'character', 'tag', 'producer', 'staff', or 'trait').
        response_size (str): The desired size of the response ('small' or 'large'). Defaults to 'small'.

    Returns:
        List[str]: A list of field names to be used in the database query.

    Raises:
        ValueError: If an invalid search_type or response_size is provided.
    """
    if response_size not in ['small', 'large']:
        raise ValueError(f"Invalid response_size: {response_size}. Must be 'small' or 'large'.")

    field_mapping = {
        'vn': (LocalFields.SMALL_VN, LocalFields.VN),
        'character': (LocalFields.SMALL_CHARACTER, LocalFields.CHARACTER),
        'tag': (LocalFields.SMALL_TAG, LocalFields.TAG),
        'producer': (LocalFields.SMALL_PRODUCER, LocalFields.PRODUCER),
        'staff': (LocalFields.SMALL_STAFF, LocalFields.STAFF),
        'trait': (LocalFields.SMALL_TRAIT, LocalFields.TRAIT),
        'release': (LocalFields.SMALL_RELEASE, LocalFields.RELEASE)
    }

    if search_type not in field_mapping:
        raise ValueError(f"Invalid search_type: {search_type}")

    return field_mapping[search_type][0] if response_size == 'small' else field_mapping[search_type][1]