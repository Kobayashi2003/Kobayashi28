from typing import List, Dict, Any, Optional, Callable

from .fields import VNDBFields

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
]

SMALL_FIELDS_TAG: List[str] = [
    VNDBFields.Tag.ID,
    VNDBFields.Tag.NAME
]

SMALL_FIELDS_PRODUCER: List[str] = [
    VNDBFields.Producer.ID,
    VNDBFields.Producer.NAME,
]

SMALL_FIELDS_STAFF: List[str] = [
    VNDBFields.Staff.ID,
    VNDBFields.Staff.NAME,
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

