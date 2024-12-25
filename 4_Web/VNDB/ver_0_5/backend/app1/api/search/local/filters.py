from typing import Dict, Any, List, Callable

import re
import uuid
from datetime import date

from sqlalchemy import or_, and_, text, exists, select, func
from sqlalchemy.sql.expression import BinaryExpression

from api.database.models import VN, Tag, Producer, Staff, Character, Trait, Release

def generate_unique_param_name(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def array_jsonb_exact_match(column: Any, key: str, value: Any) -> BinaryExpression:
    param_key = generate_unique_param_name("key")
    param_value = generate_unique_param_name("value")
    return exists(
        select(1)
        .select_from(func.unnest(column).alias('jsonb_item'))
        .where(text(f"jsonb_item->>:{param_key} = :{param_value}"))
    ).params({param_key: key, param_value: value})

def array_jsonb_match(column: Any, key: str, value: Any) -> BinaryExpression:
    param_key = generate_unique_param_name("key")
    param_value = generate_unique_param_name("value")
    return exists(
        select(1)
        .select_from(func.unnest(column).alias('jsonb_item'))
        .where(text(f"jsonb_item->>:{param_key} ILIKE :{param_value}"))
    ).params({param_key: key, param_value: f"%{value}%"})

def array_string_match(column: Any, value: str) -> BinaryExpression:
    """
    Create a filter for matching a value in an ARRAY(String) column.
    
    :param column: The SQLAlchemy column object (ARRAY(String) type)
    :param value: The value to match against
    :return: An SQLAlchemy exists clause for filtering
    """
    param_value = generate_unique_param_name("value")
    return exists(
        select(1)
        .select_from(func.unnest(column).alias('array_item'))
        .where(text(f"array_item ILIKE :{param_value}"))
    ).params({param_value: f"%{value}%"})


def process_multi_value_expression(expression: str, value_processor: Callable[[str], BinaryExpression]) -> BinaryExpression:
    """
    Process a multi-value expression with OR/AND logic.
    
    :param expression: The input expression (e.g., "value1,value2+value3")
    :param value_processor: A function that takes a string value and returns a SQLAlchemy filter condition
    :return: A single SQLAlchemy filter condition (OR of all processed conditions)
    """
    or_expressions = re.split(r'\s*,\s*', expression.strip())
    or_conditions = []
    
    for or_expr in or_expressions:
        if '+' in or_expr:
            and_values = re.split(r'\s*\+\s*', or_expr)
            and_conditions = [value_processor(value.strip()) for value in and_values]
            or_conditions.append(and_(*and_conditions))
        else:
            or_conditions.append(value_processor(or_expr.strip()))
    
    return or_(*or_conditions)

def create_comparison_filter(field: Any, value: str, value_parser: Callable[[str], Any]) -> BinaryExpression:
    pattern = r'^(>=|<=|>|<|=)?(.+)$'
    match = re.match(pattern, value.strip())
    if not match:
        raise ValueError(f"Invalid comparison format: {value}")
    
    operator, actual_value = match.groups()
    operator = operator or '='
    
    operators = {
        '>=': lambda f, v: f >= v,
        '<=': lambda f, v: f <= v,
        '>': lambda f, v: f > v,
        '<': lambda f, v: f < v,
        '=': lambda f, v: f == v
    }
    
    parsed_value = value_parser(actual_value)
    return operators[operator](field, parsed_value)

def parse_date(value: str) -> List[int]:
    patterns = [
        (r'^(\d{4})$', lambda m: [int(m.group(1))]),
        (r'^(\d{4})-(\d{2})$', lambda m: [int(m.group(1)), int(m.group(2))]),
        (r'^(\d{4})-(\d{2})-(\d{2})$', lambda m: [int(m.group(1)), int(m.group(2)), int(m.group(3))])
    ]
    
    for pattern, date_func in patterns:
        match = re.match(pattern, value)
        if match:
            return date_func(match)
    
    if value.lower() == 'tba':
        return [-1]
    
    raise ValueError(f"Invalid date format: {value}. Use YYYY, YYYY-MM, YYYY-MM-DD, or TBA.")

def parse_resolution(value: str) -> List[int]:
    pattern = r'^(\d+)x(\d+)$'
    match = re.match(pattern, value)
    if match:
        return [int(match.group(1)), int(match.group(2))]

    if value.lower() == 'non-standard':
        return [-1]
    
    raise ValueError(f"Invalid resolution format: {value}. Use WIDTHxHEIGHT (e.g., 1920x1080).")

def parse_birthday(value: str) -> List[int]:
    pattern = r'^(\d{1,2})-(\d{1,2})$'
    match = re.match(pattern, value)
    if match:
        month, day = map(int, match.groups())
        if 1 <= month <= 12 and 1 <= day <= 31:
            return [month, day]
    raise ValueError(f"Invalid birthday format: {value}. Use MM-DD (e.g., 12-25).")

def parse_cup_size(value: str) -> str:
    cup_sizes = ['AAA', 'AA', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
    if value.upper() in cup_sizes:
        return value.upper()
    raise ValueError(f"Invalid cup size: {value}")


def get_vn_filters(params: Dict[str, Any]) -> List[BinaryExpression]:
    filters = []

    if olang := params.get('olang'):
        filters.append(VN.olang == olang)
    
    if devstatus := params.get('devstatus'):
        filters.append(VN.devstatus == devstatus)

    if released := params.get('released'):
        filters.append(create_comparison_filter(VN.released, released, parse_date))
    
    if language := params.get('language'):
        filters.append(array_string_match(VN.languages, language))
    
    if platform := params.get('platform'):
        filters.append(array_string_match(VN.platforms, platform))
    
    if length := params.get('length'):
        filters.append(create_comparison_filter(VN.length, length, int))
    
    if length_minutes := params.get('length_minutes'):
        filters.append(create_comparison_filter(VN.length_minutes, length_minutes, int))

    if vns := params.get('search'):
        def process_vn(vn_value):
            return or_(
                VN.id == vn_value,
                VN.title.ilike(f"%{vn_value}%"),
                VN.alttitle.ilike(f"%{vn_value}%"),
                array_string_match(VN.aliases, vn_value),
                array_jsonb_match(VN.titles, 'title', vn_value)
            )
        filters.append(process_multi_value_expression(vns, process_vn))

    if tags := params.get('tag'):
        def process_tag(tag_value):
            return or_(
                array_jsonb_exact_match(VN.tags, 'id', tag_value),
                array_jsonb_match(VN.tags, 'name', tag_value)
            )
        filters.append(process_multi_value_expression(tags, process_tag))

    if developers := params.get('developer'):
        def process_developer(dev_value):
            return or_(
                array_jsonb_exact_match(VN.developers, 'id', dev_value),
                array_jsonb_match(VN.developers, 'name', dev_value),
                array_jsonb_match(VN.developers, 'original', dev_value)
            )
        filters.append(process_multi_value_expression(developers, process_developer))

    if staff := params.get('staff'):
        def process_staff(staff_value):
            return or_(
                array_jsonb_exact_match(VN.staff, 'id', staff_value),
                array_jsonb_match(VN.staff, 'name', staff_value),
                array_jsonb_match(VN.staff, 'original', staff_value)
            )
        filters.append(process_multi_value_expression(staff, process_staff))

    if characters := params.get('character'):
        def process_character(char_value):
            return or_(
                array_jsonb_exact_match(VN.characters, 'id', char_value),
                array_jsonb_match(VN.characters, 'name', char_value),
                array_jsonb_match(VN.characters, 'original', char_value)
            )
        filters.append(process_multi_value_expression(characters, process_character))

    return filters

def get_release_filters(params: Dict[str, Any]) -> List[BinaryExpression]:
    filters = []

    if lang := params.get('lang'):
        filters.append(array_jsonb_match(Release.languages, 'lang', lang))

    if platform := params.get('platform'):
        filters.append(array_string_match(Release.platforms, platform))

    if media := params.get('medium'):
        filters.append(array_jsonb_match(Release.media, 'medium', media))

    if released := params.get('released'):
        filters.append(create_comparison_filter(Release.released, released, parse_date))

    if minage := params.get('minage'):
        filters.append(create_comparison_filter(Release.minage, minage, int))

    if resolution := params.get('resolution'):
        filters.append(create_comparison_filter(Release.resolution, resolution, parse_resolution))

    if engine := params.get('engine'):
        filters.append(Release.engine == engine)

    if voiced := params.get('voiced'):
        filters.append(create_comparison_filter(Release.voiced, voiced, int))

    if gtin := params.get('gtin'):
        filters.append(Release.gtin == gtin)

    if catalog := params.get('catalog'):
        filters.append(Release.catalog.ilike(f"%{catalog}%"))

    boolean_fields = ['patch', 'freeware', 'uncensored', 'official', 'has_ero']
    for field in boolean_fields:
        if value := params.get(field):
            filters.append(getattr(Release, field) == (value.lower() == 'true'))

    if releases := params.get('search'):
        def process_release(release_value):
            return or_(
                Release.id == release_value,
                Release.title.ilike(f"%{release_value}%"),
                Release.alttitle.ilike(f"%{release_value}%")
            )
        filters.append(process_multi_value_expression(releases, process_release))

    if vns := params.get('vn'):
        def process_vn(vn_value):
            return or_(
                array_jsonb_exact_match(Release.vns, 'id', vn_value),
                array_jsonb_match(Release.vns, 'title', vn_value)
            )
        filters.append(process_multi_value_expression(vns, process_vn))

    if producers := params.get('producer'):
        def process_producer(producer_value):
            return or_(
                array_jsonb_exact_match(Release.producers, 'id', producer_value),
                array_jsonb_match(Release.producers, 'name', producer_value),
                array_jsonb_match(Release.producers, 'original', producer_value)
            )
        filters.append(process_multi_value_expression(producers, process_producer))

    return filters

def get_character_filters(params: Dict[str, Any]) -> List[BinaryExpression]:
    filters = []

    if blood_type := params.get('blood_type'):
        filters.append(Character.blood_type == blood_type)
    
    if sex := params.get('sex'):
        filters.append(array_string_match(Character.sex, sex))
    
    # Expanded numeric fields
    if height := params.get('height'):
        filters.append(create_comparison_filter(Character.height, height, int))
    
    if weight := params.get('weight'):
        filters.append(create_comparison_filter(Character.weight, weight, int))
    
    if bust := params.get('bust'):
        filters.append(create_comparison_filter(Character.bust, bust, int))
    
    if waist := params.get('waist'):
        filters.append(create_comparison_filter(Character.waist, waist, int))
    
    if hips := params.get('hips'):
        filters.append(create_comparison_filter(Character.hips, hips, int))
    
    if age := params.get('age'):
        filters.append(create_comparison_filter(Character.age, age, int))
    
    if cup := params.get('cup'):
        filters.append(Character.cup == parse_cup_size(cup))

    if birthday := params.get('birthday'):
        filters.append(create_comparison_filter(Character.birthday, birthday, parse_birthday))

    if characters := params.get('search'):
        def process_character(character_value):
            return or_(
                Character.id == character_value,
                Character.name.ilike(f"%{character_value}%"),
                Character.original.ilike(f"%{character_value}%"),
                array_string_match(Character.aliases, character_value)
            )
        filters.append(process_multi_value_expression(characters, process_character))

    if traits := params.get('trait'):
        def process_trait(trait_value):
            trait_group, trait_name = trait_value.split(':')
            return and_(
                or_(
                    array_jsonb_exact_match(Character.traits, 'group_id', trait_group),
                    array_jsonb_match(Character.traits, 'group_name', trait_group)
                ),
                or_(
                    array_jsonb_exact_match(Character.traits, 'id', trait_name),
                    array_jsonb_match(Character.traits, 'name', trait_name)
                )
            )
        filters.append(process_multi_value_expression(traits, process_trait))

    if vns := params.get('vn'):
        def process_vn(vn_value):
            return or_(
                array_jsonb_exact_match(Character.vns, 'id', vn_value),
                array_jsonb_match(Character.vns, 'title', vn_value)
            )
        filters.append(process_multi_value_expression(vns, process_vn))
    
    return filters
    
def get_producer_filters(params: Dict[str, Any]) -> List[BinaryExpression]:
    filters = []

    if producers := params.get('search'):
        def process_producer(producer_value):
            return or_(
                Producer.id == producer_value,
                Producer.name.ilike(f"%{producer_value}%"),
                Producer.original.ilike(f"%{producer_value}%"),
                array_string_match(Producer.aliases, producer_value)
            )
        filters.append(process_multi_value_expression(producers, process_producer))
    
    if lang := params.get('lang'):
        filters.append(Producer.lang == lang)
    
    if type := params.get('type'):
        filters.append(Producer.type == type)
    
    return filters

def get_staff_filters(params: Dict[str, Any]) -> List[BinaryExpression]:
    filters = []

    if staff := params.get('search'):
        def process_staff(staff_value):
            return or_(
                Staff.id == staff_value,
                Staff.name.ilike(f"%{staff_value}%"),
                Staff.original.ilike(f"%{staff_value}%"),
                array_jsonb_match(Staff.aliases, 'name', staff_value),
            )
        filters.append(process_multi_value_expression(staff, process_staff))

    if lang := params.get('lang'):
        filters.append(Staff.lang == lang)
    
    if gender := params.get('gender'):
        filters.append(Staff.gender == gender)
    
    if ismain := params.get('ismain'):
        filters.append(Staff.ismain == (ismain.lower() == 'true'))
    
    return filters

def get_tag_filters(params: Dict[str, Any]) -> List[BinaryExpression]:
    filters = []

    if tags := params.get('search'):
        def process_tag(tag_value):
            return or_(
                Tag.id == tag_value,
                Tag.name.ilike(f"%{tag_value}%"),
                array_string_match(Tag.aliases, tag_value)
            )
        filters.append(process_multi_value_expression(tags, process_tag))

    if category := params.get('category'):
        filters.append(Tag.category == category)
    
    if vn_count := params.get('vn_count'):
        filters.append(create_comparison_filter(Tag.vn_count, vn_count, int))

    if searchable := params.get('searchable'):
        filters.append(Tag.searchable == (searchable.lower() == 'true'))
    
    if applicable := params.get('applicable'):
        filters.append(Tag.applicable == (applicable.lower() == 'true'))

    return filters

def get_trait_filters(params: Dict[str, Any]) -> List[BinaryExpression]:
    filters = []
    
    if traits := params.get('search'):
        def process_trait(trait_value):
            return or_(
                Trait.id == trait_value,
                Trait.name.ilike(f"%{trait_value}%"),
                array_string_match(Trait.aliases, trait_value)
            )
        filters.append(process_multi_value_expression(traits, process_trait))
    
    if searchable := params.get('searchable'):
        filters.append(Trait.searchable == (searchable.lower() == 'true'))
    
    if applicable := params.get('applicable'):
        filters.append(Trait.applicable == (applicable.lower() == 'true'))
    
    if group_id := params.get('group_id'):
        filters.append(Trait.group_id == group_id)
    
    if group_name := params.get('group_name'):
        filters.append(Trait.group_name.ilike(f"%{group_name}%"))
    
    if char_count := params.get('char_count'):
        filters.append(create_comparison_filter(Trait.char_count, char_count, int))
    
    return filters

def get_local_filters(search_type: str, params: Dict[str, Any]) -> List[BinaryExpression]:
    if id := params.get('id'):
        model = {
            'vn': VN,
            'character': Character,
            'producer': Producer,
            'staff': Staff,
            'tag': Tag,
            'trait': Trait,
            'release': Release
        }.get(search_type)

        if model:
            return [model.id == id]
        else:
            raise ValueError(f"Invalid search_type: {search_type}")

    filter_functions = {
        'vn': get_vn_filters,
        'character': get_character_filters,
        'producer': get_producer_filters,
        'staff': get_staff_filters,
        'tag': get_tag_filters,
        'trait': get_trait_filters,
        'release': get_release_filters
    }

    if filter_function := filter_functions.get(search_type):
        return filter_function(params)
    else:
        raise ValueError(f"Invalid search_type: {search_type}")