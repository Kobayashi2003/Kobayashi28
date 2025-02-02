import httpx
from typing import Optional, Dict, List, Any, Optional, Callable
from enum import Enum, auto


class FilterOperator(Enum):
    EQUAL = "="
    NOT_EQUAL = "!="
    GREATER_THAN = ">"
    GREATER_THAN_EQUAL = ">="
    LESS_THAN = "<"
    LESS_THAN_EQUAL = "<="

class FilterType(Enum):
    STRING = auto()
    INTEGER = auto()
    FLOAT = auto()
    BOOLEAN = auto()
    DATE = auto()
    VNDBID = auto()
    ARRAY = auto()
    NESTED = auto()

class VNDBFilter:
    def __init__(self, name: str, filter_type: FilterType, flags: str = "", associated_domain: Optional[str] = None):
        self.name = name
        self.filter_type = filter_type
        self.flags = flags
        self.associated_domain = associated_domain

class VNDBFilters:
    VN = {
        "id": VNDBFilter("id", FilterType.VNDBID, "o"),
        "search": VNDBFilter("search", FilterType.STRING, "m"),
        "lang": VNDBFilter("lang", FilterType.STRING, "m"),
        "olang": VNDBFilter("olang", FilterType.STRING),
        "platform": VNDBFilter("platform", FilterType.STRING, "m"),
        "length": VNDBFilter("length", FilterType.INTEGER, "o"),
        "released": VNDBFilter("released", FilterType.DATE, "o,n"),
        "rating": VNDBFilter("rating", FilterType.FLOAT, "o,i"),
        "votecount": VNDBFilter("votecount", FilterType.INTEGER, "o"),
        "has_description": VNDBFilter("has_description", FilterType.BOOLEAN),
        "has_anime": VNDBFilter("has_anime", FilterType.BOOLEAN),
        "has_screenshot": VNDBFilter("has_screenshot", FilterType.BOOLEAN),
        "has_review": VNDBFilter("has_review", FilterType.BOOLEAN),
        "devstatus": VNDBFilter("devstatus", FilterType.INTEGER),
        "tag": VNDBFilter("tag", FilterType.ARRAY, "m"),
        "dtag": VNDBFilter("dtag", FilterType.ARRAY, "m"),
        "anime_id": VNDBFilter("anime_id", FilterType.INTEGER),
        "label": VNDBFilter("label", FilterType.ARRAY, "m"),
        "release": VNDBFilter("release", FilterType.NESTED, "m"),
        "character": VNDBFilter("character", FilterType.NESTED, "m", associated_domain="CHARACTER"),
        "staff": VNDBFilter("staff", FilterType.NESTED, "m", associated_domain="STAFF"),
        "developer": VNDBFilter("developer", FilterType.NESTED, "m", associated_domain="PRODUCER"),
    }

    CHARACTER = {
        "id": VNDBFilter("id", FilterType.VNDBID, "o"),
        "search": VNDBFilter("search", FilterType.STRING, "m"),
        "role": VNDBFilter("role", FilterType.STRING, "m"),
        "blood_type": VNDBFilter("blood_type", FilterType.STRING),
        "sex": VNDBFilter("sex", FilterType.STRING),
        "height": VNDBFilter("height", FilterType.INTEGER, "o,n,i"),
        "weight": VNDBFilter("weight", FilterType.INTEGER, "o,n,i"),
        "bust": VNDBFilter("bust", FilterType.INTEGER, "o,n,i"),
        "waist": VNDBFilter("waist", FilterType.INTEGER, "o,n,i"),
        "hips": VNDBFilter("hips", FilterType.INTEGER, "o,n,i"),
        "cup": VNDBFilter("cup", FilterType.STRING, "o,n,i"),
        "age": VNDBFilter("age", FilterType.INTEGER, "o,n,i"),
        "trait": VNDBFilter("trait", FilterType.ARRAY, "m"),
        "dtrait": VNDBFilter("dtrait", FilterType.ARRAY, "m"),
        "birthday": VNDBFilter("birthday", FilterType.ARRAY, "n"),
        "seiyuu": VNDBFilter("seiyuu", FilterType.NESTED, "m", associated_domain="STAFF"),
        "vn": VNDBFilter("vn", FilterType.NESTED, "m", associated_domain="VN"),
    }

    PRODUCER = {
        "id": VNDBFilter("id", FilterType.VNDBID, "o"),
        "search": VNDBFilter("search", FilterType.STRING, "m"),
        "lang": VNDBFilter("lang", FilterType.STRING),
        "type": VNDBFilter("type", FilterType.STRING),
    }

    STAFF = {
        "id": VNDBFilter("id", FilterType.VNDBID, "o"),
        "aid": VNDBFilter("aid", FilterType.INTEGER),
        "search": VNDBFilter("search", FilterType.STRING, "m"),
        "lang": VNDBFilter("lang", FilterType.STRING),
        "gender": VNDBFilter("gender", FilterType.STRING),
        "role": VNDBFilter("role", FilterType.STRING, "m"),
        "extlink": VNDBFilter("extlink", FilterType.STRING, "m"),
        "ismain": VNDBFilter("ismain", FilterType.BOOLEAN),
    }

    TAG = {
        "id": VNDBFilter("id", FilterType.VNDBID, "o"),
        "search": VNDBFilter("search", FilterType.STRING, "m"),
        "category": VNDBFilter("category", FilterType.STRING),
    }

    TRAIT = {
        "id": VNDBFilter("id", FilterType.VNDBID, "o"),
        "search": VNDBFilter("search", FilterType.STRING, "m"),
    }

    RELEASE = {
        "id": VNDBFilter("id", FilterType.VNDBID, "o"),
        "search": VNDBFilter("search", FilterType.STRING, "m"),
        "lang": VNDBFilter("lang", FilterType.STRING, "m"),
        "platform": VNDBFilter("platform", FilterType.STRING, "m"),
        "released": VNDBFilter("released", FilterType.DATE, "o"),
        "resolution": VNDBFilter("resolution", FilterType.ARRAY, "o,i"),
        "resolution_aspect": VNDBFilter("resolution_aspect", FilterType.ARRAY, "o,i"),
        "minage": VNDBFilter("minage", FilterType.INTEGER, "o,n,i"),
        "medium": VNDBFilter("medium", FilterType.STRING, "m,n"),
        "voiced": VNDBFilter("voiced", FilterType.INTEGER, "n"),
        "engine": VNDBFilter("engine", FilterType.STRING, "n"),
        "rtype": VNDBFilter("rtype", FilterType.STRING, "m"),
        "extlink": VNDBFilter("extlink", FilterType.STRING, "m"),
        "patch": VNDBFilter("patch", FilterType.BOOLEAN),
        "freeware": VNDBFilter("freeware", FilterType.BOOLEAN),
        "uncensored": VNDBFilter("uncensored", FilterType.BOOLEAN, "i"),
        "official": VNDBFilter("official", FilterType.BOOLEAN),
        "has_ero": VNDBFilter("has_ero", FilterType.BOOLEAN),
        "vn": VNDBFilter("vn", FilterType.NESTED, "m", associated_domain="VN"),
        "producer": VNDBFilter("producer", FilterType.NESTED, "m", associated_domain="PRODUCER"),
    }

def parse_logical_expression(expression: str, field: str) -> Dict[str, Any]:
    """
    Parse a logical expression and return a nested dictionary structure.
    
    Args:
        expression (str): The logical expression to parse.
        field (str): The field name to use in the resulting structure.
    
    Returns:
        Dict[str, Any]: A nested dictionary representing the parsed logical expression.
    """
    def parse_subexpression(subexpr: str) -> Dict[str, Any]:
        if ',' in subexpr:
            return {"or": [{field: term.strip()} for term in subexpr.split(',')]}
        elif '+' in subexpr:
            return {"and": [{field: term.strip()} for term in subexpr.split('+')]}
        else:
            return {field: subexpr.strip()}

    expression = expression.strip()
    if not expression:
        return {}

    if '(' not in expression:
        return parse_subexpression(expression)

    result = {}
    current_op = None
    stack = []
    current_expr = ""

    for char in expression:
        if char == '(':
            stack.append((current_op, result))
            current_op = None
            result = {}
            current_expr = ""
        elif char == ')':
            if current_expr:
                sub_result = parse_subexpression(current_expr)
                result = sub_result if not result else {current_op or "and": [result, sub_result]}
            prev_op, prev_result = stack.pop()
            if not prev_result:
                prev_result = result
            else:
                prev_result = {prev_op or "and": [prev_result, result]}
            result = prev_result
            current_expr = ""
        elif char in ('+', ','):
            if current_expr:
                sub_result = parse_subexpression(current_expr)
                result = sub_result if not result else {current_op or "and": [result, sub_result]}
                current_expr = ""
            current_op = "and" if char == '+' else "or"
        else:
            current_expr += char

    if current_expr:
        sub_result = parse_subexpression(current_expr)
        result = sub_result if not result else {current_op or "and": [result, sub_result]}

    return result

def parse_int(value: Optional[str]) -> Optional[int]:
    """
    Parse a string value to an integer, returning None if parsing fails.
    
    Args:
        value (Optional[str]): The string value to parse.
    
    Returns:
        Optional[int]: The parsed integer value, or None if parsing fails.
    """
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None

def get_vn_filters(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate filters for visual novel searches based on the provided parameters.
    
    Args:
        params (Dict[str, Any]): The search parameters.
    
    Returns:
        Dict[str, Any]: A dictionary of filters for visual novel searches.
    """
    filters = []
    
    # Handle simple search parameter
    if search := params.get('search'):
        filters.append({"search": search})
    
    # Handle fields that may contain multiple values
    multi_value_fields = ['lang', 'platform', 'released', 'tag', 'dtag', 'olang']
    for field in multi_value_fields:
        if value := params.get(field):
            parsed = parse_logical_expression(value, field)
            if parsed:
                filters.append(parsed)
    
    # Handle nested fields
    nested_fields = ['character', 'staff', 'developer', 'release']
    for field in nested_fields:
        if value := params.get(field):
            parsed = parse_logical_expression(value, 'search')
            if parsed:
                filters.append({field: parsed})
    
    # Handle numeric fields
    numeric_fields = ['length', 'devstatus']
    for field in numeric_fields:
        if value := parse_int(params.get(field)):
            filters.append({field: value})
    
    # Handle boolean fields
    boolean_fields = ['has_description', 'has_anime', 'has_screenshot', 'has_review']
    for field in boolean_fields:
        if value := params.get(field):
            filters.append({field: value.lower() == 'true'})
    
    # Wrap in 'and' if there are multiple filters
    return {"and": filters} if len(filters) > 1 else filters[0] if filters else {}

def get_character_filters(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate filters for character searches based on the provided parameters.
    
    Args:
        params (Dict[str, Any]): The search parameters.
    
    Returns:
        Dict[str, Any]: A dictionary of filters for character searches.
    """
    filters = []
    
    if search := params.get('search'):
        filters.append({"search": search})
    
    multi_value_fields = ['role', 'trait', 'dtrait', 'birthday']
    for field in multi_value_fields:
        if value := params.get(field):
            parsed = parse_logical_expression(value, field)
            if parsed:
                filters.append(parsed)
    
    # Handle nested fields
    nested_fields = ['seiyuu', 'vn']
    for field in nested_fields:
        if value := params.get(field):
            parsed = parse_logical_expression(value, 'search')
            if parsed:
                filters.append({field: parsed})
    
    single_value_fields = ['blood_type', 'sex', 'cup']
    for field in single_value_fields:
        if value := params.get(field):
            filters.append({field: value})
    
    numeric_fields = ['height', 'weight', 'bust', 'waist', 'hips', 'age']
    for field in numeric_fields:
        if value := parse_int(params.get(field)):
            filters.append({field: value})
    
    return {"and": filters} if len(filters) > 1 else filters[0] if filters else {}

def get_producer_filters(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate filters for producer searches based on the provided parameters.
    
    Args:
        params (Dict[str, Any]): The search parameters.
    
    Returns:
        Dict[str, Any]: A dictionary of filters for producer searches.
    """
    filters = []
    
    if search := params.get('search'):
        filters.append({"search": search})
    
    multi_value_fields = ['lang', 'type']
    for field in multi_value_fields:
        if value := params.get(field):
            parsed = parse_logical_expression(value, field)
            if parsed:
                filters.append(parsed)
    
    return {"and": filters} if len(filters) > 1 else filters[0] if filters else {}

def get_staff_filters(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate filters for staff searches based on the provided parameters.
    
    Args:
        params (Dict[str, Any]): The search parameters.
    
    Returns:
        Dict[str, Any]: A dictionary of filters for staff searches.
    """
    filters = []
    
    if search := params.get('search'):
        filters.append({"search": search})
    
    multi_value_fields = ['lang', 'role']
    for field in multi_value_fields:
        if value := params.get(field):
            parsed = parse_logical_expression(value, field)
            if parsed:
                filters.append(parsed)
    
    if gender := params.get('gender'):
        filters.append({"gender": gender})
    
    if ismain := params.get('ismain'):
        filters.append({"ismain": ismain.lower() == 'true'})

    if extlink := params.get('extlink'):
        filters.append({"extlink": extlink})

    return {"and": filters} if len(filters) > 1 else filters[0] if filters else {}

def get_tag_filters(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate filters for tag searches based on the provided parameters.
    
    Args:
        params (Dict[str, Any]): The search parameters.
    
    Returns:
        Dict[str, Any]: A dictionary of filters for tag searches.
    """
    filters = []
    
    if search := params.get('search'):
        filters.append({"search": search})
    
    if category := params.get('category'):
        parsed = parse_logical_expression(category, 'category')
        if parsed:
            filters.append(parsed)
    
    return {"and": filters} if len(filters) > 1 else filters[0] if filters else {}

def get_trait_filters(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate filters for trait searches based on the provided parameters.
    
    Args:
        params (Dict[str, Any]): The search parameters.
    
    Returns:
        Dict[str, Any]: A dictionary of filters for trait searches.
    """
    filters = []
    
    if search := params.get('search'):
        filters.append({"search": search})
    
    return {"and": filters} if len(filters) > 1 else filters[0] if filters else {}

def get_release_filters(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate filters for release searches based on the provided parameters.
    
    Args:
        params (Dict[str, Any]): The search parameters.
    
    Returns:
        Dict[str, Any]: A dictionary of filters for release searches.
    """
    filters = []

    if search := params.get('search'):
        filters.append({"search": search})

    if search := params.get('search'):
        filters.append({"search": search})

    # Handle fields that may contain multiple values
    multi_value_fields = ['lang', 'platform', 'medium']
    for field in multi_value_fields:
        if value := params.get(field):
            parsed = parse_logical_expression(value, field)
            if parsed:
                filters.append(parsed)

    # Handle date field
    if released := params.get('released'):
        filters.append({"released": released})

    # Handle resolution and resolution_aspect
    for field in ['resolution', 'resolution_aspect']:
        if value := params.get(field):
            try:
                width, height = map(int, value.strip('[]').split(','))
                filters.append({field: [width, height]})
            except ValueError:
                pass  # Invalid format, skip this filter

    # Handle numeric fields
    numeric_fields = ['minage', 'voiced']
    for field in numeric_fields:
        if value := parse_int(params.get(field)):
            filters.append({field: value})

    # Handle string fields
    string_fields = ['engine', 'rtype']
    for field in string_fields:
        if value := params.get(field):
            filters.append({field: value})

    # Handle boolean fields
    boolean_fields = ['patch', 'freeware', 'uncensored', 'official', 'has_ero']
    for field in boolean_fields:
        if value := params.get(field):
            filters.append({field: value.lower() == 'true'})

    # Handle nested fields
    nested_fields = ['vn', 'producer']
    for field in nested_fields:
        if value := params.get(field):
            parsed = parse_logical_expression(value, 'search')
            if parsed:
                filters.append({field: parsed}) 

    # Handle extlink field
    if extlink := params.get('extlink'):
        filters.append({"extlink": extlink})

    return {"and": filters} if len(filters) > 1 else filters[0] if filters else {}

def get_remote_filters(search_type: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate filters for remote searches based on the search type and provided parameters.
    
    Args:
        search_type (str): The type of search (e.g., 'vn', 'character', 'producer', etc.).
        params (Dict[str, Any]): The search parameters.
    
    Returns:
        Dict[str, Any]: A dictionary of filters for the specified search type.
    
    Raises:
        ValueError: If an invalid search_type is provided.
    """

    if id := params.get('id'): return {"id": id}

    if search_type == 'vn':
        return get_vn_filters(params)
    elif search_type == 'character':
        return get_character_filters(params)
    elif search_type == 'producer':
        return get_producer_filters(params)
    elif search_type == 'staff':
        return get_staff_filters(params)
    elif search_type == 'tag':
        return get_tag_filters(params)
    elif search_type == 'trait':
        return get_trait_filters(params)
    else:
        raise ValueError(f"Invalid search_type: {search_type}")


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
                _fields = ['ID', 'TITLE']

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
    VNDBFields.Release.RELEASED
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


VNDB_API_URL = "https://api.vndb.org/kana"

class VNDBEndpoint(Enum):
    VN = "vn"
    CHARACTER = "character"
    PRODUCER = "producer"
    STAFF = "staff"
    TAG = "tag"
    TRAIT = "trait"
    RELEASE = "release"

class VNDBAPIWrapper:
    def __init__(self, api_token: Optional[str] = None):
        self.client = httpx.Client()
        self.client.headers.update({"Content-Type": "application/json"})
        if api_token:
            self.client.headers.update({"Authorization": f"Token {api_token}"})

    def _build_filters(self, filters: Dict[str, Any], filter_set: Dict[str, Any]) -> List[Any]:
        """
        Recursively build VNDB filters from a dictionary of filter conditions.

        Args:
            filters (Dict[str, Any]): The filter conditions to process.
            filter_set (Dict[str, Any]): The set of valid filters for the current domain.

        Returns:
            List[Any]: A list representing the VNDB filter structure.
        """
        result = []
        for key, value in filters.items():
            if key in ["and", "or"]:
                # Handle logical operators by recursively processing their contents
                result.append([key] + [self._build_filters(item, filter_set) for item in value])
            else:
                # Process individual filter conditions
                result.append(self._build_filter(key, value, filter_set))
        
        # If there's only one filter, return it directly; otherwise, wrap in an "and" operation
        return result[0] if len(result) == 1 else ["and"] + result

    def _build_filter(self, key: str, value: Any, filter_set: Dict[str, Any]) -> List[Any]:
        """
        Build a single VNDB filter condition.

        Args:
            key (str): The filter key.
            value (Any): The filter value or nested filter structure.
            filter_set (Dict[str, Any]): The set of valid filters for the current domain.

        Returns:
            List[Any]: A list representing a single VNDB filter condition.

        Raises:
            ValueError: If the filter key is unknown.
        """
        if key not in filter_set:
            raise ValueError(f"Unknown filter: {key}")

        filter_def = filter_set[key]
        
        # Handle nested filters with associated domains
        if isinstance(value, dict) and filter_def.filter_type == FilterType.NESTED:
            if filter_def.associated_domain:
                # Use the associated domain's filter set for nested filters
                associated_filter_set = getattr(VNDBFilters, filter_def.associated_domain)
                nested_filters = self._build_filters(value, associated_filter_set)
            else:
                # Use the current filter set if no associated domain is specified
                nested_filters = self._build_filters(value, filter_set)
            return [key, "=", nested_filters]
        
        # Extract operator and value from tuple, or use default equality operator
        if isinstance(value, tuple):
            operator, filter_value = value
        else:
            operator, filter_value = FilterOperator.EQUAL, value

        # Special handling for array type filters
        if filter_def.filter_type == FilterType.ARRAY and not isinstance(filter_value, list):
            filter_value = [filter_value, 0, 0]

        return [key, operator.value, filter_value]

    def query(self, endpoint: VNDBEndpoint, filters: Dict[str, Any], fields: List[str], 
              sort: str = "id", reverse: bool = False, results: int = 10, page: int = 1, count: bool = True) -> Dict[str, Any]:
        url = f"{VNDB_API_URL}/{endpoint.value}"
        
        filter_set = getattr(VNDBFilters, endpoint.name)
        
        payload = {
            "filters": self._build_filters(filters, filter_set),
            "fields": ",".join(fields),
            "sort": sort,
            "reverse": reverse,
            "results": results,
            "page": page,
            "count": count
        }
        
        response = self.client.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def get_vn(self, filters: Dict[str, Any], fields: List[str], **kwargs) -> Dict[str, Any]:
        return self.query(VNDBEndpoint.VN, filters, fields, **kwargs)

    def get_character(self, filters: Dict[str, Any], fields: List[str], **kwargs) ->   Dict[str, Any]:
        return self.query(VNDBEndpoint.CHARACTER, filters, fields, **kwargs)

    def get_producer(self, filters: Dict[str, Any], fields: List[str], **kwargs) -> Dict[str, Any]:
        return self.query(VNDBEndpoint.PRODUCER, filters, fields, **kwargs)

    def get_staff(self, filters: Dict[str, Any], fields: List[str], **kwargs) -> Dict[str, Any]:
        return self.query(VNDBEndpoint.STAFF, filters, fields, **kwargs)

    def get_tag(self, filters: Dict[str, Any], fields: List[str], **kwargs) -> Dict[str, Any]:
        return self.query(VNDBEndpoint.TAG, filters, fields, **kwargs)

    def get_trait(self, filters: Dict[str, Any], fields: List[str], **kwargs) -> Dict[str, Any]:
        return self.query(VNDBEndpoint.TRAIT, filters, fields, **kwargs)

    def get_release(self, filters: Dict[str, Any], fields: List[str], **kwargs) -> Dict[str, Any]:
        return self.query(VNDBEndpoint.RELEASE, filters, fields, **kwargs)

    def update_user_list(self, vn_id: str, data: Dict[str, Any]) -> None:
        url = f"{VNDB_API_URL}/ulist/{vn_id}"
        response = self.client.patch(url, json=data)
        response.raise_for_status()

    def update_release_list(self, release_id: str, status: int) -> None:
        url = f"{VNDB_API_URL}/rlist/{release_id}"
        response = self.client.patch(url, json={"status": status})
        response.raise_for_status()

    def remove_from_user_list(self, vn_id: str) -> None:
        url = f"{VNDB_API_URL}/ulist/{vn_id}"
        response = self.client.delete(url)
        response.raise_for_status()

    def remove_from_release_list(self, release_id: str) -> None:
        url = f"{VNDB_API_URL}/rlist/{release_id}"
        response = self.client.delete(url)
        response.raise_for_status()

    def get_auth_info(self) -> Dict[str, Any]:
        url = f"{VNDB_API_URL}/authinfo"
        response = self.client.get(url)
        response.raise_for_status()
        return response.json()

api = VNDBAPIWrapper()

def unpaginated_search(search_function: Callable, **kwargs) -> Dict[str, Any]:
    results = []
    page = 1
    more = True
    while more:
        response = search_function(**kwargs, page=page)
        results.extend(response.get('results', []))
        more = response.get('more', False)
        page += 1
    
    return {'results': results, 'total': len(results), 'count': len(results)}

def paginated_results(results: Dict[str, Any], sort: str = 'id', reverse: bool = False, limit: int = 10, page: int = 1, count: bool = True) -> Dict[str, Any]:
    if not results or 'results' not in results:
        return {'results': [], 'count': 0} if count else {'results': []}
    
    results = results['results']
    count = len(results)
    start_index = (page - 1) * limit
    end_index = start_index + limit

    results.sort(key=lambda x: x.get(sort, 0), reverse=reverse)
    results = results[start_index:end_index]

    results = {'results': results, 'more': end_index < count}
    if count:
        results['count'] = count
    
    return results

def search_vn(filters: Dict[str, Any], fields: List[str], page: int = 1, **kwargs) -> Dict[str, Any]:
    return api.get_vn(filters, fields, page=page, **kwargs)

def search_character(filters: Dict[str, Any], fields: List[str], page: int = 1, **kwargs) -> Dict[str, Any]:
    return api.get_character(filters, fields, page=page, **kwargs)

def search_tag(filters: Dict[str, Any], fields: List[str], page: int = 1, **kwargs) -> Dict[str, Any]:
    return api.get_tag(filters, fields, page=page, **kwargs)

def search_producer(filters: Dict[str, Any], fields: List[str], page: int = 1, **kwargs) -> Dict[str, Any]:
    return api.get_producer(filters, fields, page=page, **kwargs)

def search_staff(filters: Dict[str, Any], fields: List[str], page: int = 1, **kwargs) -> Dict[str, Any]:
    return api.get_staff(filters, fields, page=page, **kwargs)

def search_trait(filters: Dict[str, Any], fields: List[str], page: int = 1, **kwargs) -> Dict[str, Any]:
    return api.get_trait(filters, fields, page=page, **kwargs)

def search_release(filters: Dict[str, Any], fields: List[str], page: int = 1, **kwargs) -> Dict[str, Any]:
    return api.get_release(filters, fields, page=page, **kwargs)

def search(resource_type: str, params: Dict[str, Any], response_size: str = 'small',
           page: int = 1, limit: int = 100, 
           sort: str = 'id', reverse: bool = False, count: bool = True) -> Dict[str, Any]:

    search_functions = {
        'vn': search_vn,
        'character': search_character,
        'tag': search_tag,
        'producer': search_producer,
        'staff': search_staff,
        'trait': search_trait,
        'release': search_release
    }

    if resource_type not in search_functions:
        raise ValueError(f"Invalid search type: {resource_type}")

    filters = get_remote_filters(resource_type, params)
    fields = get_remote_fields(resource_type, response_size)

    if page and limit: 
        results = search_functions[resource_type](filters, fields, page=page, results=limit, sort=sort, reverse=reverse, count=count)
    else:
        results = unpaginated_search(
            search_function=search_functions[resource_type], 
            filters=filters, fields=fields, sort=sort, reverse=reverse, count=count
        )
    
    if not (resource_type == 'vn' and response_size == 'large'):
        return results

    for vn in results['results']:
        vnid = vn['id']

        characters = unpaginated_search(
            search_function=search_characters_by_resource_id,
            resource_type='vn', resource_id=vnid, response_size='small', limit=100
        )
        vn['characters'] = characters['results'] 

        releases = unpaginated_search(
            search_function=search_releases_by_resource_id,
            resource_type='vn', resource_id=vnid, response_size='small', limit=100
        )
        vn['releases'] = releases['results']

    return results

def search_resources_by_release_id(release_id: str, related_resource_type: str, response_size: str = "small") -> Dict[str, Any]:
    url = "https://api.vndb.org/kana/release"

    related_resource_fields = get_remote_fields(related_resource_type, response_size)
    fields = {
        'vn': [f'vns.{field}' for field in related_resource_fields] + ['vns.rtype'],
        'producer': [f'producers.{field}' for field in related_resource_fields] + ['producers.developer', 'producers.publisher']
    }.get(related_resource_type)

    payload = {
        "filters": ["id", "=", release_id],
        "fields": ",".join(fields),
        "results": 100
    }

    with httpx.Client() as client:
        response = client.post(url, json=payload)
        response.raise_for_status()
        results = response.json()['results'][0]
        results = results.get(
            {
                'vn': 'vns',
                'producer': 'producers'
            }.get(related_resource_type)
        )

    return {'results': results}

def search_resources_by_charid(charid: str, related_resource_type: str, response_size: str = "small") -> Dict[str, Any]:
    url = "https://api.vndb.org/kana/character"

    related_resource_fields = get_remote_fields(related_resource_type, response_size)
    fields = {
        'trait': [f'traits.{field}' for field in related_resource_fields].extend['traits.spoiler', 'traits.lie'],
        'vns': [f'vns.{field}' for field in related_resource_fields].extend['vns.spoiler', 'vns.role', 'vns.release.id']
    }

    payload = {
        "filters": ["id", "=", charid],
        "fields": ",".join(fields),
        "results": 100
    }

    with httpx.Client() as client: 
        response = client.post(url, json=payload)
        response.raise_for_status()
        results = response.json()['results'][0]
        results = results.get(
            {
                'trait': 'traits',
            }.get(related_resource_type)
        )

    return {'results': results}

def search_resources_by_vnid(vnid: str, related_resource_type: str, response_size: str = "small") -> Dict[str, Any]:
    url = "https://api.vndb.org/kana/vn"

    related_resource_fields = get_remote_fields(related_resource_type, response_size)
    fields = {
        'vn': [f'relations.{field}' for field in related_resource_fields] + ['relations.relation', 'relations.relation_official'],
        'tag': [f'tags.{field}' for field in related_resource_fields] + ['tags.rating', 'tags.spoiler', 'tags.lie'],
        'producer': [f'developers.{field}' for field in related_resource_fields],
        'staff': [f'staff.{field}' for field in related_resource_fields] + ['staff.eid', 'staff.role'],
    }.get(related_resource_type)

    payload = {
        "filters": ["id", "=", vnid],
        "fields": ",".join(fields),
        "results": 100
    }

    with httpx.Client() as client:
        response = client.post(url, json=payload)
        response.raise_for_status()
        results = response.json()['results'][0]
        results = results.get(
            {
                'vn': 'relations',
                'tag': 'tags',
                'producer': 'developers',
                'staff': 'staff'
            }.get(related_resource_type)
        )

    return {'results': results}

def search_releases_by_resource_id(resource_type: str, resource_id: str, response_size: str = 'small',
                                   sort: str = 'id', reverse: bool = False, limit: int = 10, page: int = 1, count: bool = True) -> Dict[str, Any]:
    url = "https://api.vndb.org/kana/release"

    filters = {
        'vn': ['vn', '=', ['id', '=', resource_id]],
        'producer': ['producer', '=', ['id', '=', resource_id]]
    }.get(resource_type)

    release_fields = get_remote_fields("release", response_size)

    payload = {
        "filters": filters,
        "fields": ",".join(release_fields),
        "sort": sort,
        "reverse": reverse,
        "results": limit,
        "page": page,
        "count": count 
    }

    with httpx.Client() as client:
        response = client.post(url, json=payload)
        response.raise_for_status()
        results = response.json()

    return results

def search_characters_by_resource_id(resource_type: str, resource_id: str, response_size: str = 'small', 
                                      sort: str = 'id', reverse: bool = False, limit: int = 10, page: int = 1, count: bool = True) -> Dict[str, Any]:
    url = "https://api.vndb.org/kana/character"

    filters = {
        'trait': ['trait', '=', [resource_id, 0, 0]], 
        'dtrait': ['dtrait', '=', [resource_id, 0, 0]],
        'vn': ['vn', '=', ['id', '=', resource_id]]
    }.get(resource_type)

    character_fields = get_remote_fields("character", response_size)

    payload = {
        "filters": filters,
        "fields": ",".join(character_fields),
        "sort": sort,
        "reverse": reverse,
        "results": limit,
        "page": page,
        "count": count 
    }

    with httpx.Client() as client:
        response = client.post(url, json=payload)
        response.raise_for_status()
        results = response.json()

    return results

def search_vns_by_resource_id(resource_type: str, resource_id: str, response_size: str = 'small',
                              sort: str = 'id', reverse: bool = False, limit: int = 10, page: int = 1, count: bool = True) -> Dict[str, Any]:
    url = "https://api.vndb.org/kana/vn"

    filters = {
        'tag': ['tag', '=', [resource_id, 0, 0]],
        'dtag': ['dtag', '=', [resource_id, 0, 0]],
        'staff': ['staff', '=', ['id', '=', resource_id]],
        'producer': ['developer', '=', ['id', '=', resource_id]],
        'character': ['character', '=', ['id', '=', resource_id]],
        'release': ['release', '=', ['id', '=', resource_id]]
    }.get(resource_type)

    vn_fields = get_remote_fields("vn", response_size)

    payload = {
        "filters": filters,
        "fields": ",".join(vn_fields),
        "sort": sort,
        "reverse": reverse,
        "results": limit,
        "page": page,
        "count": count 
    }

    with httpx.Client() as client:
        response = client.post(url, json=payload)
        response.raise_for_status()
        results = response.json()

    if response_size == 'small':
        return results

    for vn in results['results']:
        vnid = vn['id']
        characters = unpaginated_search(
            search_function=search_characters_by_resource_id,
            resource_type='vn', resource_id=vnid, response_size='small'
        )
        vn['characters'] = characters['results'] 
    return results

def memoize(timeout=3600):
    try:
        from app import cache
        return cache.memoize(timeout=timeout)
    except ImportError:
        return lambda f: f

@memoize(timeout=3600)
def search_cache(*args, **kwargs): return search(*args, **kwargs)

@memoize(timeout=3600)
def search_resources_by_vnid_cache(*args, **kwargs): return search_resources_by_vnid(*args, **kwargs)

@memoize(timeout=3600)
def search_resources_by_charid_cache(*args, **kwargs): return search_resources_by_charid(*args, **kwargs)

@memoize(timeout=3600)
def search_resources_by_release_id_cache(*args, **kwargs): return search_resources_by_release_id(*args, **kwargs)

def search_resources_by_vnid_paginated(vnid: str, related_resource_type: str, response_size: str = "small", 
                                       sort: str = 'id', reverse: bool = False, limit: int = 10, page: int = 1, count: bool = True) -> Dict[str, Any]:
    return paginated_results(search_resources_by_vnid_cache(vnid, related_resource_type, response_size),
                             sort, reverse, limit, page, count)

def search_resources_by_charid_paginated(charid: str, related_resource_type: str, response_size: str = "small", 
                                         sort: str = 'id', reverse: bool = False, limit: int = 10, page: int = 1, count: bool = True) -> Dict[str, Any]:
    return paginated_results(search_resources_by_charid_cache(charid, related_resource_type, response_size), 
                             sort, reverse, limit, page, count)

def search_resources_by_release_id_paginated(release_id: str, related_resource_type: str, response_size: str = "small",
                                             sort: str = 'id', reverse: bool = False, limit: int = 10, page: int = 1, count: bool = True) -> Dict[str, Any]:
    return paginated_results(search_resources_by_release_id_cache(release_id, related_resource_type, response_size),
                             sort, reverse, limit, page, count)

@memoize(timeout=3600)
def search_vns_by_resource_id_cache(*args, **kwargs): return search_vns_by_resource_id(*args, **kwargs)

@memoize(timeout=3600)
def search_characters_by_resource_id_cache(*args, **kwargs): return search_characters_by_resource_id(*args, **kwargs)

@memoize(timeout=3600)
def search_releases_by_resource_id_cache(*args, **kwargs): return search_releases_by_resource_id(*args, **kwargs)