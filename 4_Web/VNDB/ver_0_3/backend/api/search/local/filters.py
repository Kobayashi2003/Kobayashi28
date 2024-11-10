import re
from datetime import date
from typing import Dict, Any, List, Tuple, Callable

from sqlalchemy import or_, and_, text, cast, Integer, String

from api.db.models import VN, Tag, Producer, Staff, Character, Trait

def parse_comparison(value: str, field: Any, value_parser: Callable[[str], Any]):
    operators = {
        '>=': lambda f, v: f >= v,
        '<=': lambda f, v: f <= v,
        '>': lambda f, v: f > v,
        '<': lambda f, v: f < v,
        '=': lambda f, v: f == v
    }
    for op, func in operators.items():
        if value.startswith(op):
            parsed_value = value[len(op):].strip()
            return func(field, value_parser(parsed_value))
    return field == value_parser(value)  # Default to equality if no operator is specified

def parse_numeric_comparison(value: str, field):
    return parse_comparison(value, cast(field, Integer), int)

def parse_date_comparison(value: str, field):
    return parse_comparison(value, field, parse_date)

def parse_date(value: str) -> date:
    """
    Parse a date string and return a date object.
    Accepts YYYY, YYYY-MM, and YYYY-MM-DD formats.
    """
    patterns = [
        (r'^(\d{4})$', lambda m: date(int(m.group(1)), 1, 1)),
        (r'^(\d{4})-(\d{2})$', lambda m: date(int(m.group(1)), int(m.group(2)), 1)),
        (r'^(\d{4})-(\d{2})-(\d{2})$', lambda m: date(int(m.group(1)), int(m.group(2)), int(m.group(3))))
    ]
    
    for pattern, date_func in patterns:
        match = re.match(pattern, value)
        if match:
            return date_func(match)
    
    raise ValueError(f"Invalid date format: {value}. Use YYYY, YYYY-MM, or YYYY-MM-DD.")

def parse_cup_size(value: str):
    cup_sizes = ['AAA', 'AA', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
    if value.upper() in cup_sizes:
        return value.upper()
    raise ValueError(f"Invalid cup size: {value}")

def jsonb_array_match(array_field: str, match_conditions: List[Dict[str, str]]) -> str:
    """
    Generate SQL for matching conditions in a JSONB array field.
    
    :param array_field: Name of the JSONB array field
    :param match_conditions: List of dictionaries with 'field', 'value', and 'operator' keys
    :return: SQL string for the EXISTS clause
    """
    conditions = []
    for condition in match_conditions:
        field = condition['field']
        value = condition['value']
        operator = condition.get('operator', '=')
        
        if operator.upper() == 'ILIKE':
            conditions.append(f"(t->>'{field}')::text ILIKE :{value}")
        else:
            conditions.append(f"(t->>'{field}')::text {operator} :{value}")
    
    return f"""
        EXISTS (
            SELECT 1
            FROM unnest({array_field}) AS t
            WHERE {' OR '.join(conditions)}
        )
    """

def process_multi_value_expression(expression: str, field_name: str, value_processor: callable) -> Tuple[str, Dict[str, Any]]:
    """
    Process a multi-value expression with AND/OR logic.
    
    :param expression: The input expression (e.g., "tag1,tag2+tag3")
    :param field_name: The name of the field being processed (e.g., "tag" or "trait")
    :param value_processor: A function to process individual values
    :return: A tuple of (SQL condition string, bind parameters dictionary)
    """
    groups = re.split(r'\s*,\s*', expression.strip())
    conditions = []
    bind_params = {}
    
    for i, group in enumerate(groups):
        if '+' in group:
            and_conditions = []
            for j, value in enumerate(re.split(r'\s*\+\s*', group)):
                condition, params = value_processor(f"{field_name}_{i}_{j}", value)
                and_conditions.append(condition)
                bind_params.update(params)
            conditions.append('(' + ' AND '.join(and_conditions) + ')')
        else:
            condition, params = value_processor(f"{field_name}_{i}", group)
            conditions.append(condition)
            bind_params.update(params)
    
    return ' OR '.join(conditions), bind_params

def get_vn_filters(params: Dict[str, Any]) -> List:
    filters = []
    
    if search := params.get('search'):
        filters.append(or_(
            VN.title.ilike(f"%{search}%"),
            VN.aliases.any(search)
        ))
    
    if olang := params.get('olang'):
        filters.append(VN.olang == olang)
    
    if devstatus := params.get('devstatus'):
        filters.append(VN.devstatus == devstatus)
    
    if released := params.get('released'):
        filters.append(parse_date_comparison(released, VN.released))
    
    if language := params.get('language'):
        filters.append(VN.languages.contains([language]))
    
    if platform := params.get('platform'):
        filters.append(VN.platforms.contains([platform]))
    
    if length := params.get('length'):
        filters.append(parse_numeric_comparison(length, VN.length))
    
    if length_minutes := params.get('length_minutes'):
        filters.append(parse_numeric_comparison(length_minutes, VN.length_minutes))
    
    if tags := params.get('tag'):
        def process_tag(param_name, tag_value):
            match_conditions = [
                {'field': 'id', 'value': param_name},
                {'field': 'name', 'value': f"{param_name}_like", 'operator': 'ILIKE'}
            ]
            return jsonb_array_match('tags', match_conditions), {
                param_name: tag_value.strip(),
                f"{param_name}_like": f"%{tag_value.strip()}%"
            }
        
        tag_condition, tag_params = process_multi_value_expression(tags, 'tag', process_tag)
        filters.append(text(tag_condition).bindparams(**tag_params))
    
    if developer := params.get('developer'):
        match_conditions = [
            {'field': 'id', 'value': 'developer'},
            {'field': 'name', 'value': 'developer_like', 'operator': 'ILIKE'},
            {'field': 'original', 'value': 'developer_like', 'operator': 'ILIKE'}
        ]
        developer_filter = text(jsonb_array_match('developers', match_conditions)).bindparams(
            developer=developer,
            developer_like=f"%{developer}%"
        )
        filters.append(developer_filter)
    
    if staff := params.get('staff'):
        match_conditions = [
            {'field': 'id', 'value': 'staff'},
            {'field': 'name', 'value': 'staff_like', 'operator': 'ILIKE'},
            {'field': 'original', 'value': 'staff_like', 'operator': 'ILIKE'}
        ]
        staff_filter = text(jsonb_array_match('staff', match_conditions)).bindparams(
            staff=staff,
            staff_like=f"%{staff}%"
        )
        filters.append(staff_filter)

    return filters

def get_character_filters(params: Dict[str, Any]) -> List:
    filters = []
    
    if search := params.get('search'):
        filters.append(or_(
            Character.name.ilike(f"%{search}%"),
            Character.original.ilike(f"%{search}%"),
            Character.aliases.any(search)
        ))
    
    if blood_type := params.get('blood_type'):
        filters.append(Character.blood_type == blood_type)
    
    if sex := params.get('sex'):
        filters.append(Character.sex.contains([sex]))
    
    # Numeric fields with comparison
    numeric_fields = ['height', 'weight', 'bust', 'waist', 'hips', 'age']
    for field in numeric_fields:
        if value := params.get(field):
            filters.append(parse_numeric_comparison(value, getattr(Character, field)))
    
    if cup := params.get('cup'):
        # Convert the cup size to its string representation before comparison
        filters.append(Character.cup == cup.upper())
    
    if birthday := params.get('birthday'):
        month, day = map(int, birthday.split('-'))
        filters.append(and_(
            parse_numeric_comparison(str(month), Character.birthday[0]),
            parse_numeric_comparison(str(day), Character.birthday[1])
        ))

    if traits := params.get('trait'):
        def process_trait(param_name, trait_value):
            trait_group, trait_name = trait_value.split(':')
            match_conditions = [
                {'field': 'group_id', 'value': f"{param_name}_group"},
                {'field': 'group_name', 'value': f"{param_name}_group_like", 'operator': 'ILIKE'},
                {'field': 'id', 'value': f"{param_name}_name"},
                {'field': 'name', 'value': f"{param_name}_name_like", 'operator': 'ILIKE'}
            ]
            return jsonb_array_match('traits', match_conditions), {
                f"{param_name}_group": trait_group.strip(),
                f"{param_name}_group_like": f"%{trait_group.strip()}%",
                f"{param_name}_name": trait_name.strip(),
                f"{param_name}_name_like": f"%{trait_name.strip()}%"
            }
        
        trait_condition, trait_params = process_multi_value_expression(traits, 'trait', process_trait)
        filters.append(text(trait_condition).bindparams(**trait_params))
    
    if vns := params.get('vns'):
        match_conditions = [
            {'field': 'id', 'value': 'vn'},
            {'field': 'title', 'value': 'vn_like', 'operator': 'ILIKE'}
        ]
        vn_filter = text(jsonb_array_match('vns', match_conditions)).bindparams(
            vn=vns,
            vn_like=f"%{vns}%"
        )
        filters.append(vn_filter)

    return filters

def get_producer_filters(params: Dict[str, Any]) -> List:
    filters = []
    
    if search := params.get('search'):
        filters.append(or_(
            Producer.name.ilike(f"%{search}%"),
            Producer.original.ilike(f"%{search}%"),
            Producer.aliases.any(search)
        ))
    
    if lang := params.get('lang'):
        filters.append(Producer.lang == lang)
    
    if type_ := params.get('type'):
        filters.append(Producer.type == type_)
    
    return filters

def get_staff_filters(params: Dict[str, Any]) -> List:
    filters = []
    

    if search := params.get('search'):
        name_original_filter = or_(
            Staff.name.ilike(f"%{search}%"),
            Staff.original.ilike(f"%{search}%")
        )
        
        match_conditions = [
            {'field': 'name', 'value': 'search_like', 'operator': 'ILIKE'},
            {'field': 'original', 'value': 'search_like', 'operator': 'ILIKE'}
        ]
        alias_filter = text(jsonb_array_match('aliases', match_conditions)).bindparams(
            search_like=f"%{search}%"
        )
        
        filters.append(or_(name_original_filter, alias_filter))
    
    if lang := params.get('lang'):
        filters.append(Staff.lang == lang)
    
    if gender := params.get('gender'):
        filters.append(Staff.gender == gender)
    
    if ismain := params.get('ismain'):
        filters.append(Staff.ismain == (ismain.lower() == 'true'))
    
    return filters

def get_tag_filters(params: Dict[str, Any]) -> List:
    filters = []
    
    if search := params.get('search'):
        filters.append(or_(
            Tag.name.ilike(f"%{search}%"),
            Tag.aliases.any(search)
        ))
    
    if category := params.get('category'):
        filters.append(Tag.category == category)
    
    if vn_count := params.get('vn_count'):
        filters.append(parse_numeric_comparison(vn_count, Tag.vn_count))

    # Boolean fields
    boolean_fields = ['searchable', 'applicable']
    for field in boolean_fields:
        if value := params.get(field):
            filters.append(getattr(Tag, field) == (value.lower() == 'true'))
    
    return filters

def get_trait_filters(params: Dict[str, Any]) -> List:
    filters = []
    
    if search := params.get('search'):
        filters.append(or_(
            Trait.name.ilike(f"%{search}%"),
            Trait.aliases.any(search)
        ))
    
    # Boolean fields
    boolean_fields = ['searchable', 'applicable']
    for field in boolean_fields:
        if value := params.get(field):
            filters.append(getattr(Trait, field) == (value.lower() == 'true'))
    
    if group_id := params.get('group_id'):
        filters.append(Trait.group_id == group_id)
    
    if group_name := params.get('group_name'):
        filters.append(Trait.group_name.ilike(f"%{group_name}%"))
    
    if char_count := params.get('char_count'):
        filters.append(parse_numeric_comparison(char_count, Trait.char_count))
    
    return filters

def get_local_filters(search_type: str, params: Dict[str, Any]) -> List:
    """
    Generate filters for local database searches based on the search type and provided parameters.
    
    Args:
        search_type (str): The type of search (e.g., 'vn', 'character', 'producer', etc.).
        params (Dict[str, Any]): The search parameters.
    
    Returns:
        List: A list of SQLAlchemy filter conditions for the specified search type.
    
    Raises:
        ValueError: If an invalid search_type is provided.
    """
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