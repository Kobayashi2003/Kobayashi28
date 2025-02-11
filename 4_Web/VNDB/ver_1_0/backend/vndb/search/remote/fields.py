from typing import List


class FieldMeta(type):

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        for attr_name, attr_value in cls.__dict__.items():
            if isinstance(attr_value, type):
                setattr(attr_value, '_outer', cls)
        return cls

    def __getattr__(cls, name):
        if name == 'ALL':
            return cls._get_all_fields()
        return cls._get_field(name)

class FieldGroup(metaclass=FieldMeta):

    _outer = None
    _prefix = ""
    _fields = []

    @classmethod
    def _get_outer_prefix(cls):
        if cls._outer is None:
            return ""
        return f"{cls._outer._get_outer_prefix()}{cls._outer._prefix}"

    @classmethod
    def _handle_field(cls, value):
        if isinstance(value, str):
            return f"{cls._get_outer_prefix()}{cls._prefix}{value}"
        raise TypeError(f"Expected string, got {type(value).__name__}")

    @classmethod
    def _get_field(cls, name):
        if name in cls._fields:
            return cls._handle_field(name.lower())
        raise AttributeError(f"'{cls.__name__}' object has no attribute '{name}'")

    @classmethod
    def _get_all_fields(cls):
        all_fields = []
        for field in cls._fields:
            all_fields.append(cls._handle_field(field.lower()))
        for attr, value in cls.__dict__.items():
            if isinstance(value, type) and attr != '_outer':
                all_fields.extend(value._get_all_fields())
        return all_fields

class VNDBFields:
    class VN(FieldGroup):
        _prefix = ""
        _fields = ['ID', 'TITLE', 'ALTTITLE', 'ALIASES', 'OLANG', 'DEVSTATUS', 'RELEASED', 
                   'LANGUAGES', 'PLATFORMS', 'LENGTH', 'LENGTH_MINUTES', 'LENGTH_VOTES', 
                   'DESCRIPTION', 'AVERAGE', 'RATING', 'VOTECOUNT']

        class TITLES(FieldGroup):
            _prefix = "titles."
            _fields = ['LANG', 'TITLE', 'LATIN', 'OFFICIAL', 'MAIN']

        class IMAGE(FieldGroup):
            _prefix = "image."
            _fields = ['ID', 'URL', 'DIMS', 'SEXUAL', 'VIOLENCE', 'THUMBNAIL', 'THUMBNAIL_DIMS']

        class SCREENSHOTS(FieldGroup):
            _prefix = "screenshots."
            _fields = ['URL', 'DIMS', 'SEXUAL', 'VIOLENCE', 'THUMBNAIL', 'THUMBNAIL_DIMS']
            
            class RELEASE(FieldGroup):
                _prefix = "release."
                _fields = ['ID']

        class RELATIONS(FieldGroup):
            _prefix = "relations."
            _fields = ['ID', 'RELATION', 'RELATION_OFFICIAL', 'TITLE']

        class TAGS(FieldGroup):
            _prefix = "tags."
            _fields = ['ID', 'RATING', 'SPOILER', 'LIE', 'NAME', 'CATEGORY']

        class DEVELOPERS(FieldGroup):
            _prefix = "developers."
            _fields = ['ID', 'NAME', 'ORIGINAL']

        class STAFF(FieldGroup):
            _prefix = "staff."
            _fields = ['ID', 'EID', 'ROLE', 'NOTE', 'NAME', 'ORIGINAL']

        class EDITIONS(FieldGroup):
            _prefix = "editions."
            _fields = ['EID', 'LANG', 'NAME', 'OFFICIAL']

        class VA(FieldGroup):
            _prefix = "va."
            _fields = ['NOTE']

            class STAFF(FieldGroup):
                _prefix = "staff."
                _fields = ['ID', 'NAME', 'ORIGINAL']

            class CHARACTER(FieldGroup):
                _prefix = "character."
                _fields = ['ID', 'NAME', 'ORIGINAL']

        class EXTLINKS(FieldGroup):
            _prefix = "extlinks."
            _fields = ['URL', 'LABEL', 'NAME', 'ID']

    class Character(FieldGroup):
        _prefix = ""
        _fields = ['ID', 'NAME', 'ORIGINAL', 'ALIASES', 'DESCRIPTION', 'BLOOD_TYPE', 'HEIGHT', 
                   'WEIGHT', 'BUST', 'WAIST', 'HIPS', 'CUP', 'AGE', 'BIRTHDAY', 'SEX']

        class IMAGE(FieldGroup):
            _prefix = "image."
            _fields = ['ID', 'URL', 'DIMS', 'SEXUAL', 'VIOLENCE']

        class VNS(FieldGroup):
            _prefix = "vns."
            _fields = ['ID', 'SPOILER', 'ROLE', 'TITLE']

            class RELEASE(FieldGroup):
                _prefix = "release."
                _fields = ['ID']

        class TRAITS(FieldGroup):
            _prefix = "traits."
            _fields = ['ID', 'SPOILER', 'LIE', 'GROUP_ID', 'NAME', 'GROUP_NAME']

    class Tag(FieldGroup):
        _prefix = ""
        _fields = ['ID', 'NAME', 'ALIASES', 'DESCRIPTION', 'CATEGORY', 'SEARCHABLE', 'APPLICABLE', 'VN_COUNT']

    class Producer(FieldGroup):
        _prefix = ""
        _fields = ['ID', 'NAME', 'ORIGINAL', 'ALIASES', 'LANG', 'TYPE', 'DESCRIPTION']

    class Staff(FieldGroup):
        _prefix = ""
        _fields = ['ID', 'AID', 'ISMAIN', 'NAME', 'ORIGINAL', 'LANG', 'GENDER', 'DESCRIPTION']

        class ALIASES(FieldGroup):
            _prefix = "aliases."
            _fields = ['AID', 'NAME', 'LATIN', 'ISMAIN']

        class EXTLINKS(FieldGroup):
            _prefix = "extlinks."
            _fields = ['URL', 'LABEL', 'NAME', 'ID']

    class Trait(FieldGroup):
        _prefix = ""
        _fields = ['ID', 'NAME', 'ALIASES', 'DESCRIPTION', 'SEARCHABLE', 'APPLICABLE', 
                   'GROUP_ID', 'GROUP_NAME', 'CHAR_COUNT']

    class Release(FieldGroup):
        _prefix = ""
        _fields = ['ID', 'TITLE', 'ALTTITLE', 'PLATFORMS', 'RELEASED', 'MINAGE', 'PATCH', 'FREEWARE', 
                   'UNCENSORED', 'OFFICIAL', 'HAS_ERO', 'RESOLUTION', 'ENGINE', 'VOICED', 'NOTES', 'GTIN', 'CATALOG']

        class LANGUAGES(FieldGroup):
            _prefix = "languages."
            _fields = ['LANG', 'TITLE', 'LATIN', 'MTL', 'MAIN']

        class MEDIA(FieldGroup):
            _prefix = "media."
            _fields = ['MEDIUM', 'QTY']
        
        class VNS(FieldGroup):
            _prefix = "vns."
            _fields = ['ID', 'RTYPE', 'TITLE']
        
        class PRODUCERS(FieldGroup):
            _prefix = "producers."
            _fields = ['ID', 'DEVELOPER', 'PUBLISHER']

        class IMAGES(FieldGroup):
            _prefix = "images."
            _fields = ['ID', 'TYPE', 'VN', 'LANGUAGES', 'PHOTO', 'URL', 'DIMS', 'SEXUAL', 
                       'VIOLENCE', 'THUMBNAIL', 'THUMBNAIL_DIMS']

        class EXTLINKS(FieldGroup):
            _prefix = "extlinks."
            _fields = ['URL', 'LABEL', 'NAME', 'ID']


SMALL_FIELDS_VN: List[str] = [
    VNDBFields.VN.ID,
    VNDBFields.VN.TITLE,
    VNDBFields.VN.RELEASED,
    VNDBFields.VN.IMAGE.URL,
    VNDBFields.VN.IMAGE.THUMBNAIL,
    VNDBFields.VN.IMAGE.SEXUAL,
    VNDBFields.VN.IMAGE.VIOLENCE
]

SMALL_FIELDS_CHARACTER: List[str] = [
    VNDBFields.Character.ID,
    VNDBFields.Character.NAME,
    VNDBFields.Character.ORIGINAL,
    VNDBFields.Character.IMAGE.URL,
    VNDBFields.Character.IMAGE.SEXUAL,
    VNDBFields.Character.IMAGE.VIOLENCE
]

SMALL_FIELDS_TAG: List[str] = [
    VNDBFields.Tag.ID,
    VNDBFields.Tag.NAME
]

SMALL_FIELDS_PRODUCER: List[str] = [
    VNDBFields.Producer.ID,
    VNDBFields.Producer.NAME,
    VNDBFields.Producer.ORIGINAL
]

SMALL_FIELDS_STAFF: List[str] = [
    VNDBFields.Staff.ID,
    VNDBFields.Staff.NAME,
    VNDBFields.Staff.ORIGINAL
]

SMALL_FIELDS_TRAIT: List[str] = [
    VNDBFields.Trait.ID,
    VNDBFields.Trait.NAME,
    VNDBFields.Trait.GROUP_ID,
    VNDBFields.Trait.GROUP_NAME
]

SMALL_FIELDS_RELEASE: List[str] = [
    VNDBFields.Release.ID,
    VNDBFields.Release.TITLE, 
    VNDBFields.Release.RELEASED,
    VNDBFields.Release.IMAGES.VN,
    VNDBFields.Release.IMAGES.TYPE,
    VNDBFields.Release.IMAGES.URL,
    VNDBFields.Release.IMAGES.THUMBNAIL,
    VNDBFields.Release.IMAGES.SEXUAL,
    VNDBFields.Release.IMAGES.VIOLENCE
]


FIELDS_VN: List[str] = VNDBFields.VN.ALL
FIELDS_CHARACTER: List[str] = VNDBFields.Character.ALL
FIELDS_TAG: List[str] = VNDBFields.Tag.ALL
FIELDS_PRODUCER: List[str] = VNDBFields.Producer.ALL
FIELDS_STAFF: List[str] = VNDBFields.Staff.ALL
FIELDS_TRAIT: List[str] = VNDBFields.Trait.ALL
FIELDS_RELEASE: List[str] = VNDBFields.Release.ALL


def get_remote_fields(search_type: str, response_size: str = 'small') -> List[str]:

    """
    Get the appropriate fields for a remote VNDB API search based on the search type and response size.

    Args:
        search_type (str): The type of entity to search for ('vn', 'character', 'tag', 'producer', 'staff', 'trait', or 'release').
        response_size (str): The desired size of the response ('small' or 'large'). Defaults to 'small'.

    Returns:
        List[str]: A list of field names to be used in the API request.

    Raises:
        ValueError: If an invalid search_type is provided.
    """
    if response_size not in ['small', 'large']:
        raise ValueError(f"Invalid response_size: {response_size}. Must be 'small' or 'large'.")

    field_mapping = {
        'vn': (SMALL_FIELDS_VN, FIELDS_VN),
        'character': (SMALL_FIELDS_CHARACTER, FIELDS_CHARACTER),
        'tag': (SMALL_FIELDS_TAG, FIELDS_TAG),
        'producer': (SMALL_FIELDS_PRODUCER, FIELDS_PRODUCER),
        'staff': (SMALL_FIELDS_STAFF, FIELDS_STAFF),
        'trait': (SMALL_FIELDS_TRAIT, FIELDS_TRAIT),
        'release': (SMALL_FIELDS_RELEASE, FIELDS_RELEASE)
    }

    if search_type not in field_mapping:
        raise ValueError(f"Invalid search_type: {search_type}")

    return field_mapping[search_type][0] if response_size == 'small' else field_mapping[search_type][1]


if __name__ == '__main__':
    print("VN" + "="*50)
    print(get_remote_fields('vn', 'large'))
    print("Character" + "="*50)
    print(get_remote_fields('character', 'large'))
    print("TAG" + "="*50)
    print(get_remote_fields('tag', 'large'))
    print("Producer" + "="*50)
    print(get_remote_fields('producer', 'large'))
    print("staff" + "="*50)
    print(get_remote_fields('staff', 'large'))
    print("Trait" + "="*50)
    print(get_remote_fields('trait', 'large'))
    print("Release" + "="*50)
    print(get_remote_fields('release', 'large'))