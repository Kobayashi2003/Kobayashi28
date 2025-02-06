from typing import Dict, Any
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
    def __init__(self, name: str, filter_type: FilterType, flags: str = "", associated_domain: str | None = None):
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
        "rating": VNDBFilter("rating", FilterType.INTEGER, "o,i"),
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

def parse_int(value: str | None) -> int | None:
    """
    Parse a string value to an integer, returning None if parsing fails.
    
    Args:
        value (str | None): The string value to parse.
    
    Returns:
        int | None: The parsed integer value, or None if parsing fails.
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