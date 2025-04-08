import re
import httpx
from typing import Any 
from enum import Enum, auto
from ..parse import validate_logical_expression


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
        "release": VNDBFilter("release", FilterType.NESTED, "m", associated_domain="RELEASE"),
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


def build_filter(filter_set: dict[str, VNDBFilter], key: str, value: Any) -> list:
    if key not in filter_set:
        raise ValueError(f"Invalid key: {key}")

    filter_def = filter_set[key]
    
    operator, filter_value = '=', value

    if 'o' in filter_def.flags:
        pattern = r'^(>=|<=|>|<|=|!=)(.+)$'
        match = re.match(pattern, value.strip())
        if match:
            operator, filter_value = match.groups()
   
    if not filter_value:
        raise ValueError(f"Invalid value: {value}")

    if isinstance(filter_value, str):
        filter_value = filter_value.strip()

    if filter_def.filter_type == FilterType.NESTED:
        if not isinstance(filter_value, dict):
            raise ValueError(f"Invalid value: {value}")
        if filter_def.associated_domain:
            associated_filter_set = getattr(VNDBFilters, filter_def.associated_domain)
            nested_filters = build_filters(associated_filter_set, filter_value)
        else:
            nested_filters = build_filters(filter_set, filter_value)
        return [key, "=", nested_filters]
    
    if filter_def.filter_type == FilterType.ARRAY:
        if key == 'tag' or key == 'dtag':
            ...
        elif key == 'trait' or key == 'dtrait':
            ...
        elif not isinstance(filter_value, list):
            raise ValueError(f"Invalid value: {value}")

    if filter_def.filter_type == FilterType.BOOLEAN:
        if isinstance(filter_value, bool):
            operator = '=' if filter_value else '!='
        elif isinstance(filter_value, str):
            if filter_value.lower() == 'false' or filter_value.lower() == '0':
                operator = '!='
            elif filter_value.lower() == 'true' or filter_value.lower() == '1':
                operator = '='
            else:
                raise ValueError(f"Invalid value: {value}")
        elif isinstance(filter_value, int):
            if filter_value == 0:
                operator = '!='
            elif filter_value == 1:
                operator = '='
            else:
                raise ValueError(f"Invalid value: {value}")
        else:
            raise ValueError(f"Invalid value: {value}")
        filter_value = 1

    if filter_def.filter_type == FilterType.INTEGER:
        if isinstance(filter_value, str):
            int(filter_value)
        elif not isinstance(filter_value, int):
            raise ValueError(f"Invalid value: {value}")

    if filter_def.filter_type == FilterType.FLOAT:
        if isinstance(filter_value, str):
            float(filter_value)
        elif not isinstance(filter_value, float):
            raise ValueError(f"Invalid value: {value}")

    if filter_def.filter_type == FilterType.VNDBID:
        pattern = r'^([v|r|c|p|s|g|i]\d+|\d+)$'
        match = re.match(pattern, filter_value)
        if not match:
            raise ValueError(f"Invalid value: {value}")
        filter_value = match.group(1)

    filter_value = str(filter_value)

    return [key, operator, filter_value]

def build_filters(filter_set: dict[str, VNDBFilter], filters: dict[str, Any]) -> list:
    result = []
    for key, value in filters.items():
        if key in ['and', 'or']:
            result.append([key] + [build_filters(filter_set, item) for item in value])
        else:
            result.append(build_filter(filter_set, key, value))
    return [] if not result else result[0] if len(result) == 1 else ["and"] + result


def parse_logical_expression(expression: str, field: str) -> dict[str, Any]:
    """
    Parse logical expression using two stacks.
    Operators: OR (',', lower precedence) and AND ('+', higher precedence)
    """
    if not validate_logical_expression(expression):
        raise ValueError(f"Invalid expression: {expression}")

    def or_operation(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
        """Merge OR operations"""
        if isinstance(left, dict) and "or" in left:
            if isinstance(right, dict) and "or" in right:
                return {"or": left["or"] + right["or"]}
            left["or"].append(right)
            return left
        elif isinstance(right, dict) and "or" in right:
            right["or"].insert(0, left)
            return right
        return {"or": [left, right]}

    def and_operation(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
        """Merge AND operations"""
        if isinstance(left, dict) and "and" in left:
            if isinstance(right, dict) and "and" in right:
                return {"and": left["and"] + right["and"]}
            left["and"].append(right)
            return left
        elif isinstance(right, dict) and "and" in right:
            right["and"].insert(0, left)
            return right
        return {"and": [left, right]}

    def evaluate(ops: list, vals: list) -> None:
        if len(ops) > 0 and len(vals) >= 2:
            op = ops.pop()
            right = vals.pop()
            left = vals.pop()
            
            if op == "or":
                vals.append(or_operation(left, right))
            elif op == "and":
                vals.append(and_operation(left, right))

    ops = []
    vals = []
    current = ""
    
    for char in expression:
        if char == '(':
            ops.append(char)
        elif char == ')':
            if current:
                vals.append({field: current.strip()})
                current = ""
            while ops and ops[-1] != '(':
                evaluate(ops, vals)
            if ops and ops[-1] == '(':
                ops.pop()
        elif char in '+,':
            if current:
                vals.append({field: current.strip()})
                current = ""
            while ops and ops[-1] != '(' and char == ',' and ops[-1] == '+':
                evaluate(ops, vals)
            ops.append('and' if char == '+' else 'or')
        else:
            current += char
    
    if current:
        vals.append({field: current.strip()})
    
    while ops:
        evaluate(ops, vals)
    
    return vals[0] if vals else {}

def parse_tag_expression(expression: str, directly: bool = False) -> dict[str, Any]:
    url = "https://api.vndb.org/kana/tag"
    client = httpx.Client()

    def get_tag_ids(tag: str) -> list[str]:
        """Get tag IDs from tag name using unpaginated search"""
        results = []
        page =1 
        more = True
        while more:
            payload = {
                "filters": ["search", "=", tag],
                "fields": "id",
                "page": page,
                "results": 100
            }
            response = client.post(url, json=payload)
            results.extend(response.json().get('results', []))
            more = response.json().get('more', False)
            page += 1
        return [result['id'] for result in results]

    def process_tags(expr: str) -> str:
        """Extract and process tags from expression"""
        # Store positions of brackets for reconstruction
        brackets = []
        current_pos = 0
        while current_pos < len(expr):
            if expr[current_pos] in '()':
                brackets.append((current_pos, expr[current_pos]))
            current_pos += 1

        # Split by operators and process each tag
        tags = re.split(r'[+,()]', expr)
        tags = [tag.strip() for tag in tags if tag.strip()]
        
        # Create mapping of original tags to their IDs
        tag_map = {}
        for tag in tags:
            if tag not in tag_map:
                ids = get_tag_ids(tag)
                if ids:
                    # If multiple IDs found, combine them with OR
                    tag_map[tag] = f"({','.join(ids)})" if len(ids) > 1 else ids[0]
                else:
                    tag_map[tag] = "t0"  # Placeholder for non-existent tag

        # Reconstruct expression with IDs
        new_expr = expr
        for tag, tag_ids in tag_map.items():
            new_expr = re.sub(r'\b' + re.escape(tag) + r'\b', tag_ids, new_expr)

        return new_expr

    new_expression = process_tags(expression.strip())

    field = 'dtag' if directly else 'tag'
    return parse_logical_expression(new_expression, field)

def parse_trait_expression(expression: str, directly: bool = False) -> dict[str, Any]:
    url = "https://api.vndb.org/kana/trait"
    client = httpx.Client()

    # def get_trait_ids(trait: str) -> List[str]:
    #     """Get trait IDs from trait name using unpaginated search"""
    #     results = []
    #     page = 1
    #     more = True
    #     while more:
    #         payload = {
    #             "filters": ["search", "=", trait],
    #             "fields": "id",
    #             "page": page,
    #             "results": 100
    #         }
    #         response = client.post(url, json=payload)
    #         results.extend(response.json().get('results', []))
    #         more = response.json().get('more', False)
    #         page += 1
    #     return [result['id'] for result in results]

    def get_trait_ids(trait: str) -> list[str]:
        # Recently, there is no way to get trait ids from trait name and trait group name at the same time.
        # So, we don't process the trait here.
        return [trait]

    def process_traits(expr: str) -> str:
        # Split by operators and process each trait
        traits = re.split(r'[+,()]', expr)
        traits = [trait.strip() for trait in traits if trait.strip()]
        
        # Create mapping of original traits to their IDs
        trait_map = {}
        for trait in traits:
            if trait not in trait_map:
                ids = get_trait_ids(trait)
                trait_map[trait] = f"({','.join(ids)})" if len(ids) > 1 else ids[0] if ids else "i0"

        # Reconstruct expression with IDs
        new_expr = expr
        for trait, trait_ids in trait_map.items():
            new_expr = re.sub(r'\b' + re.escape(trait) + r'\b', trait_ids, new_expr)

        return new_expr

    new_expression = process_traits(expression.strip())

    field = 'dtrait' if directly else 'trait'
    return parse_logical_expression(new_expression, field)

def parse_int(value: str | None, comparable: bool = False) -> str | None:
    value = value.replace(" ", "")
    pattern = r'^(>=|<=|>|<|=|!=)?(\d+)$' if comparable else r'^(\d+)$'
    match = re.match(pattern, value)
    if match:
        return value
    return None 

def parse_birthday(value: str) -> list[int] | None:
    value = value.replace(" ", "")
    pattern = r'^(\d{1,2})-(\d{1,2})$'
    match = re.match(pattern, value)
    if match:
        month, day = map(int, match.groups())
        if 1 <= month <= 12 and 1 <= day <= 31:
            return [month, day]
    return None


def get_vn_additional_filters(params: dict[str, Any]) -> dict[str, Any]:
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

def get_release_additional_filters(params: dict[str, Any]) -> dict[str, Any]:
    filters = []

    if vn_id := params.get('vn_id'):
        filters.append({"vn": ["id", "=", vn_id]})

    if producer_id := params.get('producer_id'):
        filters.append({"producer": ["id", "=", producer_id]})

    return filters

def get_character_additional_filters(params: dict[str, Any]) -> dict[str, Any]:
    filters = []

    if vn_id := params.get('vn_id'):
        filters.append({"vn": ["id", "=", vn_id]})

    return filters

def get_producer_additional_filters(params: dict[str, Any]) -> dict[str, Any]:
    filters = []

    return filters

def get_staff_additional_filters(params: dict[str, Any]) -> dict[str, Any]:
    filters = []

    return filters

def get_tag_additional_filters(params: dict[str, Any]) -> dict[str, Any]:
    filters = []

    return filters

def get_trait_additional_filters(params: dict[str, Any]) -> dict[str, Any]:
    filters = []

    return filters


def get_vn_filters(params: dict[str, Any]) -> dict[str, Any]:
    """
    Generate filters for visual novel searches based on the provided parameters.
    
    Args:
        params (dict[str, Any]): The search parameters.
    
    Returns:
        dict[str, Any]: A dictionary of filters for visual novel searches.
    """
    filters = []

    if id := params.get('id'):
        filters.append(parse_logical_expression(id, 'id'))

    if search := params.get('search'):
        filters.append({"search": search})

    if tag := params.get('tag'):
        filters.append(parse_tag_expression(tag))

    if dtag := params.get('dtag'):
        filters.append(parse_tag_expression(dtag, directly=True))
    
    # Handle fields that may contain multiple values
    multi_value_fields = ['lang', 'platform', 'released', 'olang']
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

def get_release_filters(params: dict[str, Any]) -> dict[str, Any]:
    """
    Generate filters for release searches based on the provided parameters.
    
    Args:
        params (dict[str, Any]): The search parameters.
    
    Returns:
        dict[str, Any]: A dictionary of filters for release searches.
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

def get_character_filters(params: dict[str, Any]) -> dict[str, Any]:
    """
    Generate filters for character searches based on the provided parameters.
    
    Args:
        params (dict[str, Any]): The search parameters.
    
    Returns:
        dict[str, Any]: A dictionary of filters for character searches.
    """
    filters = []

    if id := params.get('id'):
        filters.append(parse_logical_expression(id, 'id'))
    
    if search := params.get('search'):
        filters.append({"search": search})

    if birthday := params.get('birthday'):
        if parsed := parse_birthday(birthday):
            filters.append({"birthday": parsed})
    
    if trait := params.get('trait'):
        filters.append(parse_trait_expression(trait))

    if dtrait := params.get('dtrait'):
        filters.append(parse_trait_expression(dtrait, directly=True))

    multi_value_fields = ['role']
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

def get_producer_filters(params: dict[str, Any]) -> dict[str, Any]:
    """
    Generate filters for producer searches based on the provided parameters.
    
    Args:
        params (dict[str, Any]): The search parameters.
    
    Returns:
        dict[str, Any]: A dictionary of filters for producer searches.
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

def get_staff_filters(params: dict[str, Any]) -> dict[str, Any]:
    """
    Generate filters for staff searches based on the provided parameters.
    
    Args:
        params (dict[str, Any]): The search parameters.
    
    Returns:
        dict[str, Any]: A dictionary of filters for staff searches.
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

def get_tag_filters(params: dict[str, Any]) -> dict[str, Any]:
    """
    Generate filters for tag searches based on the provided parameters.
    
    Args:
        params (dict[str, Any]): The search parameters.
    
    Returns:
        dict[str, Any]: A dictionary of filters for tag searches.
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

def get_trait_filters(params: dict[str, Any]) -> dict[str, Any]:
    """
    Generate filters for trait searches based on the provided parameters.
    
    Args:
        params (dict[str, Any]): The search parameters.
    
    Returns:
        dict[str, Any]: A dictionary of filters for trait searches.
    """
    filters = []

    if id := params.get('id'):
        filters.append(parse_logical_expression(id, 'id'))
    
    if search := params.get('search'):
        filters.append({"search": search})
    
    filters.extend(get_trait_additional_filters(params))

    return {"and": filters} if len(filters) > 1 else filters[0] if filters else {}


def get_remote_filters(search_type: str, params: dict[str, Any]) -> list:
    """
    Generate filters for remote searches based on the search type and provided parameters.
    
    Args:
        search_type (str): The type of search (e.g., 'vn', 'character', 'producer', etc.).
        params (dict[str, Any]): The search parameters.
    
    Returns:
        dict[str, Any]: A dictionary of filters for the specified search type.
    
    Raises:
        ValueError: If an invalid search_type is provided.
    """

    if search_type == 'vn':
        return build_filters(VNDBFilters.VN, get_vn_filters(params))
    elif search_type == 'release':
        return build_filters(VNDBFilters.RELEASE, get_release_filters(params))
    elif search_type == 'character':
        return build_filters(VNDBFilters.CHARACTER, get_character_filters(params))
    elif search_type == 'producer':
        return build_filters(VNDBFilters.PRODUCER, get_producer_filters(params))
    elif search_type == 'staff':
        return build_filters(VNDBFilters.STAFF, get_staff_filters(params))
    elif search_type == 'tag':
        return build_filters(VNDBFilters.TAG, get_tag_filters(params))
    elif search_type == 'trait':
        return build_filters(VNDBFilters.TRAIT, get_trait_filters(params))
    else:
        raise ValueError(f"Invalid search_type: {search_type}")


if __name__ == '__main__':
    print(get_remote_filters(
        search_type='vn',
        params={
            'id': '17',
            # 'search': 'ai kiss',
            # 'id': '((v1,v2)+(v6,v7,v8))',
            # 'tag': 'Gang Rape + Unavoidable Rape',
        }
    ))