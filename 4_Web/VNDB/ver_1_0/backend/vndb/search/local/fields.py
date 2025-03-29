from typing import List

from vndb.database.models import VN, Tag, Producer, Staff, Character, Trait, Release

class LocalFields:
    VN = [column.key for column in VN.__table__.columns]
    RELEASE = [column.key for column in Release.__table__.columns]
    CHARACTER = [column.key for column in Character.__table__.columns]
    PRODUCER = [column.key for column in Producer.__table__.columns]
    STAFF = [column.key for column in Staff.__table__.columns]
    TAG = [column.key for column in Tag.__table__.columns]
    TRAIT = [column.key for column in Trait.__table__.columns]

    SMALL_VN = ['id', 'title', 'titles', 'released', 'image']
    SMALL_RELEASE = ['id', 'title', 'released', 'vns', 'producers']
    SMALL_CHARACTER = ['id', 'name', 'sex', 'original', 'vns', 'image']
    SMALL_PRODUCER = ['id', 'name', 'original']
    SMALL_STAFF = ['id', 'name', 'original']
    SMALL_TAG = ['id', 'name', 'category']
    SMALL_TRAIT = ['id', 'name', 'group_id', 'group_name']

    @staticmethod
    def get_fields(model_name: str) -> list:
        return getattr(LocalFields, model_name.upper(), [])

SORTABLE_FIELDS = {
    'vn': [
        'id', 'title', 'released', 'length_minutes', 
        'length_votes', 'average', 'rating', 'votecount', 
    ],
    'release': [
        'id', 'title', 'released', 'minage',
    ],
    'character': [
        'id', 'name', 'original', 'height', 
        'weight', 'bust', 'waist', 'hips', 
        'age', 'birthday',
    ],
    'producer': [
        'id', 'name', 'original',
    ],
    'staff': [
        'id', 'name', 'original',
    ],
    'tag': [
        'id', 'name', 'vn_count',
    ],
    'trait': [
        'id', 'name', 'group_id', 'group_name',
        'char_count',
    ]
}

def validate_sort(search_type: str, sort: str) -> str:
    if search_type not in SORTABLE_FIELDS:
        raise ValueError(f"Invalid search_type: {search_type}")
    if sort not in SORTABLE_FIELDS[search_type]:
        raise ValueError(f"Invalid sort: {sort} for search_type: {search_type}")
    return sort

def get_local_fields(search_type: str, response_size: str = 'small') -> List[str]:
    """
    Get the appropriate fields for a local database search based on the search type and response size.

    Args:
        search_type (str): The type of entity to search for ('vn', 'character', 'tag', 'producer', 'staff', 'trait' or 'release').
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