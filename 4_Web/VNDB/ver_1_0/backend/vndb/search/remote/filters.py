import re
from typing import Dict, Any, List
from enum import Enum, auto


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
        "sex_spoil": VNDBFilter("sex_spoil", FilterType.STRING),
        "gender": VNDBFilter("gender", FilterType.STRING),
        "gender_spoil": VNDBFilter("gender_spoil", FilterType.STRING),
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
    def parse_sub_expression(subexpr: str) -> Dict[str, Any]:
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
        return parse_sub_expression(expression)

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
                sub_result = parse_sub_expression(current_expr)
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
                sub_result = parse_sub_expression(current_expr)
                result = sub_result if not result else {current_op or "and": [result, sub_result]}
                current_expr = ""
            current_op = "and" if char == '+' else "or"
        else:
            current_expr += char

    if current_expr:
        sub_result = parse_sub_expression(current_expr)
        result = sub_result if not result else {current_op or "and": [result, sub_result]}

    return result

def parse_int(value: str | None, comparable: bool = False) -> str | None:
    value = value.replace(" ", "")
    pattern = r'^(>=|<=|>|<|=|!=)?(\d+)$' if comparable else r'^(\d+)$'
    match = re.match(pattern, value)
    if match:
        return value
    return None 

def parse_birthday(value: str) -> List[int]:
    value = value.replace(" ", "")
    pattern = r'^(\d{1,2})-(\d{1,2})$'
    match = re.match(pattern, value)
    if match:
        month, day = map(int, match.groups())
        if 1 <= month <= 12 and 1 <= day <= 31:
            return [month, day]
    return None

def get_vn_additional_filters(params: Dict[str, Any]) -> Dict[str, Any]:
    filters = []

    if release_id := params.get('release_id'):
        filters.append({"release": ["id", "=", release_id]})

    if character_id := params.get('character_id'):
        filters.append({"character": ["id", "=", character_id]})

    if staff_id := params.get('staff_id'):
        filters.append({"staff": ["id", "=", staff_id]})

    if developer_id := params.get('developer_id'):
        filters.append({"developer": ["id", "=", developer_id]})

    return filters

def get_release_additional_filters(params: Dict[str, Any]) -> Dict[str, Any]:
    filters = []

    if vn_id := params.get('vn_id'):
        filters.append({"vn": ["id", "=", vn_id]})

    if producer_id := params.get('producer_id'):
        filters.append({"producer": ["id", "=", producer_id]})

    return filters

def get_character_additional_filters(params: Dict[str, Any]) -> Dict[str, Any]:
    filters = []

    if vn_id := params.get('vn_id'):
        filters.append({"vn": ["id", "=", vn_id]})

    return filters

def get_producer_additional_filters(params: Dict[str, Any]) -> Dict[str, Any]:
    filters = []

    return filters

def get_staff_additional_filters(params: Dict[str, Any]) -> Dict[str, Any]:
    filters = []

    return filters

def get_tag_additional_filters(params: Dict[str, Any]) -> Dict[str, Any]:
    filters = []

    return filters

def get_trait_additional_filters(params: Dict[str, Any]) -> Dict[str, Any]:
    filters = []

    return filters


def get_vn_filters(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate filters for visual novel searches based on the provided parameters.
    
    Args:
        params (Dict[str, Any]): The search parameters.
    
    Returns:
        Dict[str, Any]: A dictionary of filters for visual novel searches.
    """
    filters = []

    if id := params.get('id'):
        filters.append(parse_logical_expression(id, 'id'))

    # Handle simple search parameter
    if search := params.get('search'):
        filters.append({"search": search})
    
    # Handle fields that may contain multiple values
    multi_value_fields = ['lang', 'platform', 'released', 'tag', 'dtag', 'olang']
    for field in multi_value_fields:
        if value := params.get(field):
            if parsed := parse_logical_expression(value, field):
                filters.append(parsed)
    
    # Handle nested fields
    nested_fields = ['character', 'staff', 'developer', 'release']
    for field in nested_fields:
        if value := params.get(field):
            if parsed := parse_logical_expression(value, 'search'):
                filters.append({field: parsed})
    
    # Handle uncomparable numeric fields
    uncomparable_numeric_fields = ['devstatus']
    for field in uncomparable_numeric_fields:
        if value := params.get(field):
            if parsed := parse_int(value):
                filters.append({field: parsed})

    # Handle comparable numeric fields
    comparable_numeric_fields = ['length']
    for field in comparable_numeric_fields:
        if value := params.get(field):
            if parsed := parse_int(value, True):
                filters.append({field: parsed})
    
    # Handle boolean fields
    boolean_fields = ['has_description', 'has_anime', 'has_screenshot', 'has_review']
    for field in boolean_fields:
        if value := params.get(field):
            filters.append({field: str(value).lower() == 'true' or str(value) == '1'})
    
    filters.extend(get_vn_additional_filters(params))

    # Wrap in 'and' if there are multiple filters
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

    if id := params.get('id'):
        filters.append(parse_logical_expression(id, 'id'))

    if search := params.get('search'):
        filters.append({"search": search})

    if search := params.get('search'):
        filters.append({"search": search})

    # Handle fields that may contain multiple values
    multi_value_fields = ['lang', 'platform', 'medium']
    for field in multi_value_fields:
        if value := params.get(field):
            if parsed := parse_logical_expression(value, field):
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

    # Handle uncomparable numeric fields
    uncomparable_numeric_fields = ['voiced']
    for field in uncomparable_numeric_fields:
        if value := params.get(field):
            if parsed := parse_int(value):
                filters.append({field: parsed})

    # Handle comparable numeric fields
    comparable_numeric_fields = ['minage']
    for field in comparable_numeric_fields:
        if value := params.get(field):
            if parsed := parse_int(value, True):
                filters.append({field: parsed})

    # Handle string fields
    string_fields = ['engine', 'rtype']
    for field in string_fields:
        if value := params.get(field):
            filters.append({field: value})

    # Handle boolean fields
    boolean_fields = ['patch', 'freeware', 'uncensored', 'official', 'has_ero']
    for field in boolean_fields:
        if value := params.get(field):
            filters.append({field: str(value).lower() == 'true' or str(value) == '1'})

    # Handle nested fields
    nested_fields = ['vn', 'producer']
    for field in nested_fields:
        if value := params.get(field):
            if parsed := parse_logical_expression(value, 'search'):
                filters.append({field: parsed}) 

    # Handle extlink field
    if extlink := params.get('extlink'):
        filters.append({"extlink": extlink})

    filters.extend(get_release_additional_filters(params))

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

    if id := params.get('id'):
        filters.append(parse_logical_expression(id, 'id'))
    
    if search := params.get('search'):
        filters.append({"search": search})

    if birthday := params.get('birthday'):
        if parsed := parse_birthday(birthday):
            filters.append({"birthday": parsed})
    
    multi_value_fields = ['role', 'trait', 'dtrait']
    for field in multi_value_fields:
        if value := params.get(field):
            if parsed := parse_logical_expression(value, field):
                filters.append(parsed)
    
    # Handle nested fields
    nested_fields = ['seiyuu', 'vn']
    for field in nested_fields:
        if value := params.get(field):
            if parsed := parse_logical_expression(value, 'search'):
                filters.append({field: parsed})
    
    single_value_fields = ['blood_type', 'sex', 'sex_spoil', 'gender', 'gender_spoil', 'cup']
    for field in single_value_fields:
        if value := params.get(field):
            filters.append({field: value})
    
    comparable_numeric_fields = ['height', 'weight', 'bust', 'waist', 'hips', 'age']
    for field in comparable_numeric_fields:
        if value := params.get(field):
            if parsed := parse_int(value, True):
                filters.append({field: parsed})
    
    filters.extend(get_character_additional_filters(params))

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

    if id := params.get('id'):
        filters.append(parse_logical_expression(id, 'id'))
    
    if search := params.get('search'):
        filters.append({"search": search})
    
    multi_value_fields = ['lang', 'type']
    for field in multi_value_fields:
        if value := params.get(field):
            if parsed := parse_logical_expression(value, field):
                filters.append(parsed)
    
    filters.extend(get_producer_additional_filters(params))

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

    if id := params.get('id'):
        filters.append(parse_logical_expression(id, 'id'))
    
    if search := params.get('search'):
        filters.append({"search": search})
    
    multi_value_fields = ['lang', 'role']
    for field in multi_value_fields:
        if value := params.get(field):
            if parsed := parse_logical_expression(value, field):
                filters.append(parsed)
    
    if gender := params.get('gender'):
        filters.append({"gender": gender})
    
    if ismain := params.get('ismain'):
        filters.append({"ismain": str(ismain).lower() == 'true' or str(ismain) == '1'})

    if extlink := params.get('extlink'):
        filters.append({"extlink": extlink})

    filters.extend(get_staff_additional_filters(params))

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

    if id := params.get('id'):
        filters.append(parse_logical_expression(id, 'id'))
    
    if search := params.get('search'):
        filters.append({"search": search})
    
    if category := params.get('category'):
        if parsed := parse_logical_expression(category, 'category'):
            filters.append(parsed)
    
    filters.extend(get_tag_additional_filters(params))

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

    if id := params.get('id'):
        filters.append(parse_logical_expression(id, 'id'))
    
    if search := params.get('search'):
        filters.append({"search": search})
    
    filters.extend(get_trait_additional_filters(params))

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

    if search_type == 'vn':
        return get_vn_filters(params)
    elif search_type == 'release':
        return get_release_filters(params)
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


if __name__ == '__main__':
    print(get_remote_filters(
        search_type='vn',
        params={
            'search': 'ai kiss',
            'id': 'v1,v2',
            'tag': 't1+t2',
            'developer': 'p1,p2'
        }
    ))