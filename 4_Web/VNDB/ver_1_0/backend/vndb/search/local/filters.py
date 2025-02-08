from typing import Dict, Tuple, List, Callable, Any

import re
import uuid
from datetime import datetime

from sqlalchemy import or_, and_, text, false, exists, select, func, Integer, Float
from sqlalchemy.sql.expression import BinaryExpression

from vndb.database.models import VN, Tag, Producer, Staff, Character, Trait, Release

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


def parse_released(value: str) -> str:
    """
    Parse the released date string.
    
    :param value: A string representing the release date in YYYY, YYYY-MM, or YYYY-MM-DD format
    :return: A normalized date string in YYYY-MM-DD format
    """
    patterns = [
        (r'^(\d{4})$', r'\1-01-01'),  # YYYY format
        (r'^(\d{4})-(\d{2})$', r'\1-\2-01'),  # YYYY-MM format
        (r'^(\d{4})-(\d{2})-(\d{2})$', r'\1-\2-\3')  # YYYY-MM-DD format
    ]

    for pattern, replacement in patterns:
        if re.match(pattern, value):
            normalized = re.sub(pattern, replacement, value)
            # Validate the date
            try:
                datetime.strptime(normalized, "%Y-%m-%d")
                return normalized
            except ValueError:
                pass

    raise ValueError(f"Invalid release date format: {value}. Use YYYY, YYYY-MM, or YYYY-MM-DD format.")

def parse_resolution(value: str) -> Tuple[int, int]:
    """
    Parse the resolution string.
    
    :param value: A string representing the resolution in the format "WIDTHxHEIGHT"
    :return: A tuple of (width, height)
    """
    pattern = r'^(\d+)x(\d+)$'
    match = re.match(pattern, value)
    if match:
        return tuple(map(int, match.groups()))
    
    raise ValueError(f"Invalid resolution format: {value}. Use 'WIDTHxHEIGHT' format (e.g., '640x480').")

def parse_birthday(value: str) -> Tuple[int, int]:
    """
    Parse the birthday string.
    
    :param value: A string representing the birthday in the format "MM-DD"
    :return: A tuple of (month, day)
    """
    pattern = r'^(\d{1,2})-(\d{1,2})$'
    match = re.match(pattern, value)
    if match:
        month, day = map(int, match.groups())
        if 1 <= month <= 12 and 1 <= day <= 31:
            return (month, day)
    
    raise ValueError(f"Invalid birthday format: {value}. Use 'MM-DD' format (e.g., '12-25').")

def parse_cup(value: str) -> str:
    cup_sizes = ['AAA', 'AA', 'A', 'B', 'C', 'D', 'E', 
                 'F', 'G', 'H', 'I', 'J', 'K', 'L', 
                 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 
                 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    if value.upper() in cup_sizes:
        return value.upper()
    raise ValueError(f"Invalid cup size: {value}")

def create_released_comparison_filter(value: str, model) -> BinaryExpression:
    """
    Create a filter for comparing released dates stored as strings.
    
    :param value: The release date value to compare against in the format "OPERATOR DATE"
    :param model: The SQLAlchemy model (VN or Release) to use for the filter
    :return: An SQLAlchemy filter expression
    """
    pattern = r'^(>=|<=|>|<|=)?(.+)$'
    match = re.match(pattern, value.strip())
    if not match:
        raise ValueError(f"Invalid release date comparison format: {value}. Use format like '>=2022-01-01'.")
    
    operator, date_value = match.groups()
    operator = operator or '='
    
    normalized_date = parse_released(date_value)
    
    operators = {
        '>=': lambda field, date: and_(field != 'TBA', field.isnot(None), field >= date),
        '<=': lambda field, date: and_(field != 'TBA', field.isnot(None), field <= date),
        '>': lambda field, date: and_(field != 'TBA', field.isnot(None), field > date),
        '<': lambda field, date: and_(field != 'TBA', field.isnot(None), field < date),
        '=': lambda field, date: and_(field != 'TBA', field.isnot(None), field == date)
    }
    
    return operators[operator](model.released, normalized_date)

def create_resolution_comparison_filter(value: str) -> BinaryExpression:
    """
    Create a filter for comparing resolutions stored as strings in the format "[WIDTH,HEIGHT]".
    
    :param value: The resolution value to compare against in the format "OPERATORWIDTHxHEIGHT"
    :return: An SQLAlchemy filter expression
    """
    pattern = r'^(>=|<=|>|<|=)?(.+)$'
    match = re.match(pattern, value.strip())
    if not match:
        raise ValueError(f"Invalid resolution comparison format: {value}. Use format like '>=640x480'.")

    operator, resolution_value = match.groups()
    operator = operator or '='

    width, height = parse_resolution(resolution_value)

    resolution_without_brackets = func.substring(Release.resolution, 2, func.length(Release.resolution) - 2)
    extracted_width = func.cast(func.split_part(resolution_without_brackets, ',', 1), Integer)
    extracted_height = func.cast(func.split_part(resolution_without_brackets, ',', 2), Integer)

    operators = {
        '>=': lambda w, h: or_(
            extracted_width > w,
            and_(extracted_width == w, extracted_height >= h)
        ),
        '<=': lambda w, h: or_(
            extracted_width < w,
            and_(extracted_width == w, extracted_height <= h)
        ),
        '>': lambda w, h: or_(
            extracted_width > w,
            and_(extracted_width == w, extracted_height > h)
        ),
        '<': lambda w, h: or_(
            extracted_width < w,
            and_(extracted_width == w, extracted_height < h)
        ),
        '=': lambda w, h: and_(extracted_width == w, extracted_height == h)
    }

    return and_(
        Release.resolution.isnot(None),
        Release.resolution != '"non-standard"',
        operators[operator](width, height)
    )

def create_resolution_aspect_comparison_filter(value: str) -> BinaryExpression:
    """
    Create a filter for comparing resolutions and aspect ratios stored as strings in the format "[WIDTH,HEIGHT]".
    
    :param value: The resolution value to compare against in the format "OPERATORWIDTHxHEIGHT"
    :return: An SQLAlchemy filter expression
    """
    pattern = r'^(>=|<=|>|<|=)?(.+)$'
    match = re.match(pattern, value.strip())
    if not match:
        raise ValueError(f"Invalid resolution comparison format: {value}. Use format like '>=640x480'.")
    
    operator, resolution_value = match.groups()
    operator = operator or '='
    
    width, height = parse_resolution(resolution_value)
    
    # Extract numbers from the stored string
    resolution_without_brackets = func.substring(Release.resolution, 2, func.length(Release.resolution) - 2)
    extracted_width = func.cast(func.split_part(resolution_without_brackets, ',', 1), Integer)
    extracted_height = func.cast(func.split_part(resolution_without_brackets, ',', 2), Integer)
    
    # Calculate aspect ratios
    given_aspect_ratio = width / height
    stored_aspect_ratio = func.cast(extracted_width, Float) / func.cast(extracted_height, Float)
    
    # Define a small tolerance for floating-point comparisons
    tolerance = 0.0001
    
    aspect_ratio_match = func.abs(stored_aspect_ratio - given_aspect_ratio) < tolerance
    
    operators = {
        '>=': lambda w, h: and_(
            or_(
                extracted_width > w,
                and_(extracted_width == w, extracted_height >= h)
            ),
            aspect_ratio_match
        ),
        '<=': lambda w, h: and_(
            or_(
                extracted_width < w,
                and_(extracted_width == w, extracted_height <= h)
            ),
            aspect_ratio_match
        ),
        '>': lambda w, h: and_(
            or_(
                extracted_width > w,
                and_(extracted_width == w, extracted_height > h)
            ),
            aspect_ratio_match
        ),
        '<': lambda w, h: and_(
            or_(
                extracted_width < w,
                and_(extracted_width == w, extracted_height < h)
            ),
            aspect_ratio_match
        ),
        '=': lambda w, h: and_(extracted_width == w, extracted_height == h, aspect_ratio_match)
    }
    
    return and_(
        Release.resolution.isnot(None),
        Release.resolution != '"non-standard"',
        operators[operator](width, height)
    )

def create_birthday_comparison_filter(value: str) -> BinaryExpression:
    """
    Create a filter for comparing birthdays stored as strings in the format "[MM,DD]".
    
    :param value: The birthday value to compare against in the format "OPERATOR MM-DD"
    :return: An SQLAlchemy filter expression
    """

    pattern = r'^(>=|<=|>|<|=)?(.+)$'
    match = re.match(pattern, value.strip())
    if not match:
        raise ValueError(f"Invalid birthday comparison format: {value}. Use format like '>=12-25'.")
    
    operator, birthday_value = match.groups()
    operator = operator or '='
    
    month, day = parse_birthday(birthday_value)
    
    birthday_without_brackets = func.substring(Character.birthday, 2, func.length(Character.birthday) - 2)
    extracted_month = func.cast(func.split_part(birthday_without_brackets, ',', 1), Integer)
    extracted_day = func.cast(func.split_part(birthday_without_brackets, ',', 2), Integer)
    
    operators = {
        '>=': lambda m, d: or_(
            extracted_month > m,
            and_(extracted_month == m, extracted_day >= d)
        ),
        '<=': lambda m, d: or_(
            extracted_month < m,
            and_(extracted_month == m, extracted_day <= d)
        ),
        '>': lambda m, d: or_(
            extracted_month > m,
            and_(extracted_month == m, extracted_day > d)
        ),
        '<': lambda m, d: or_(
            extracted_month < m,
            and_(extracted_month == m, extracted_day < d)
        ),
        '=': lambda m, d: and_(extracted_month == m, extracted_day == d)
    }
    
    return and_(
        Character.birthday.isnot(None),
        operators[operator](month, day)
    )

def create_cup_comparison_filter(value: str) -> BinaryExpression:
    """
    Create a filter for comparing cup sizes stored as strings.
    
    :param value: The cup size value to compare against in the format "OPERATOR SIZE"
    :param model: The SQLAlchemy model (Character) to use for the filter
    :return: An SQLAlchemy filter expression
    """
    pattern = r'^(>=|<=|>|<|=)?(.+)$'
    match = re.match(pattern, value.strip())
    if not match:
        raise ValueError(f"Invalid cup size comparison format: {value}. Use format like '>=B'.")
    
    operator, cup_value = match.groups()
    operator = operator or '='
    
    cup_size = parse_cup(cup_value)
    
    if cup_size == 'AAA':
        operators = {
            '>=': lambda field, size: field.isnot(None),
            '<=': lambda field, size: field == 'AAA',
            '>': lambda field, size: and_(field.isnot(None), field != 'AAA'),
            '<': lambda field, size: false(),  # No cup size smaller than AAA
            '=': lambda field, size: field == 'AAA'
        }
    elif cup_size == 'AA':
        operators = {
            '>=': lambda field, size: and_(field.isnot(None), field != 'AAA'),
            '<=': lambda field, size: or_(field == 'AAA', field == 'AA'),
            '>': lambda field, size: and_(field.isnot(None), field != 'AAA', field != 'AA'),
            '<': lambda field, size: field == 'AAA',
            '=': lambda field, size: field == 'AA'
        }
    elif cup_size == 'A':
        operators = {
            '>=': lambda field, size: and_(field.isnot(None), field != 'AAA', field != 'AA'),
            '<=': lambda field, size: or_(field == 'AAA', field == 'AA', field == 'A'),
            '>': lambda field, size: and_(field.isnot(None), field != 'AAA', field != 'AA', field != 'A'),
            '<': lambda field, size: or_(field == 'AAA', field == 'AA'),
            '=': lambda field, size: field == 'A'
        }
    else:
        operators = {
                '>=': lambda field, size: and_(field.isnot(None), field >= size),
                '<=': lambda field, size: and_(field.isnot(None), field <= size),
                '>': lambda field, size: and_(field.isnot(None), field > size),
                '<': lambda field, size: and_(field.isnot(None), field < size),
                '=': lambda field, size: field == size
            }
    
    return operators[operator](Character.cup, cup_size)


def get_vn_filters(params: Dict[str, Any]) -> List[BinaryExpression]:
    filters = []

    if id := params.get('id'):
        return [VN.id == id]

    if search := params.get('search'):
        def process_vn(vn_value):
            return or_(
                VN.id == vn_value,
                VN.title.ilike(f"%{vn_value}%"),
                VN.alttitle.ilike(f"%{vn_value}%"),
                array_string_match(VN.aliases, vn_value),
                array_jsonb_match(VN.titles, 'title', vn_value)
            )
        filters.append(process_multi_value_expression(search, process_vn))

    if lang := params.get('lang'):
        filters.append(array_string_match(VN.languages, lang))

    if olang := params.get('olang'):
        filters.append(VN.olang == olang)
    
    if platform := params.get('platform'):
        filters.append(array_string_match(VN.platforms, platform))

    if length := params.get('length'):
        filters.append(create_comparison_filter(VN.length, length, int))

    if released := params.get('released'):
        filters.append(create_released_comparison_filter(released, VN))

    if rating := params.get('rating'):
        filters.append(create_comparison_filter(VN.rating, rating, int))

    if votecount := params.get('votecount'):
        filters.append(create_comparison_filter(VN.votecount, votecount, int))

    if 'has_description' in params:
        has_description = params['has_description']
        if str(has_description).lower() == 'true':
            filters.append(VN.description.isnot(None))
        elif str(has_description).lower() == 'false':
            filters.append(VN.description.is_(None))
        else:
            raise ValueError(f"Invalid value for has_description: {has_description}. Use 'true' or 'false'.")

    if 'has_anime' in params: #TODO 
        raise ValueError("The 'has_anime' search field is not available for local searches.")

    if 'has_screenshot' in params:
        has_screenshot = params['has_screenshot']
        if str(has_screenshot).lower() == 'true':
            filters.append(and_(VN.screenshots.isnot(None), func.array_length(VN.screenshots, 1) > 0))
        elif str(has_screenshot).lower() == 'false':
            filters.append(or_(VN.screenshots.is_(None), func.array_length(VN.screenshots, 1) == 0))
        else:
            raise ValueError(f"Invalid value for has_screenshot: {has_screenshot}. Use 'true' or 'false'.")

    if 'has_review' in params: #TODO
        raise ValueError("The 'has_review' search field is not available for local searches.")
    
    if devstatus := params.get('devstatus'):
        filters.append(VN.devstatus == devstatus)

    if tags := params.get('tag'):
        def process_tag(tag_value):
            return or_(
                array_jsonb_exact_match(VN.tags, 'id', tag_value),
                array_jsonb_match(VN.tags, 'name', tag_value)
            )
        filters.append(process_multi_value_expression(tags, process_tag))

    if dtags := params.get('dtag'): #TODO
        raise ValueError("The 'dtags' search field is not available for local searches.")

    if anime_id := params.get('anime_id'): #TODO
        raise ValueError("The 'anime_id' search field is not available for local searches.")

    if label := params.get('label'): #TODO
        raise ValueError("The 'label' search field is not available for local searches.")

    if releases := params.get('release'):
        def process_release(release_value):
            return or_(
                array_jsonb_exact_match(VN.releases, 'id', release_value),
                array_jsonb_match(VN.releases, 'title', release_value)
            )
        filters.append(process_multi_value_expression(releases, process_release))

    if characters := params.get('character'):
        def process_character(char_value):
            return or_(
                array_jsonb_exact_match(VN.characters, 'id', char_value),
                array_jsonb_match(VN.characters, 'name', char_value),
                array_jsonb_match(VN.characters, 'original', char_value)
            )
        filters.append(process_multi_value_expression(characters, process_character))

    if staff := params.get('staff'):
        def process_staff(staff_value):
            return or_(
                array_jsonb_exact_match(VN.staff, 'id', staff_value),
                array_jsonb_match(VN.staff, 'name', staff_value),
                array_jsonb_match(VN.staff, 'original', staff_value)
            )
        filters.append(process_multi_value_expression(staff, process_staff))

    if developers := params.get('developer'):
        def process_developer(dev_value):
            return or_(
                array_jsonb_exact_match(VN.developers, 'id', dev_value),
                array_jsonb_match(VN.developers, 'name', dev_value),
                array_jsonb_match(VN.developers, 'original', dev_value)
            )
        filters.append(process_multi_value_expression(developers, process_developer))

    return filters

def get_release_filters(params: Dict[str, Any]) -> List[BinaryExpression]:
    filters = []

    if id := params.get('id'):
        return [Release.id == id]

    if search := params.get('search'):
        def process_release(release_value):
            return or_(
                Release.id == release_value,
                Release.title.ilike(f"%{release_value}%"),
                Release.alttitle.ilike(f"%{release_value}%")
            )
        filters.append(process_multi_value_expression(search, process_release))

    if lang := params.get('lang'):
        filters.append(array_jsonb_match(Release.languages, 'lang', lang))

    if platform := params.get('platform'):
        filters.append(array_string_match(Release.platforms, platform))
        
    if released := params.get('released'):
        filters.append(create_released_comparison_filter(released, Release))

    if resolution := params.get('resolution'):
        filters.append(create_resolution_comparison_filter(resolution))

    if resolution_aspect := params.get('resolution_aspect'):
        filters.append(create_resolution_aspect_comparison_filter(resolution_aspect))

    if minage := params.get('minage'):
        filters.append(create_comparison_filter(Release.minage, minage, int))

    if media := params.get('medium'):
        filters.append(array_jsonb_match(Release.media, 'medium', media))

    if voiced := params.get('voiced'):
        filters.append(create_comparison_filter(Release.voiced, voiced, int))

    if engine := params.get('engine'):
        filters.append(Release.engine == engine)

    if rtype := params.get('rtype'):
        filters.append(array_jsonb_exact_match(Release.vns, 'rtype', rtype))

    if extlink := params.get('extlink'):
        filters.append(or_(
            array_jsonb_exact_match(Release.extlinks, 'id', extlink),
            array_jsonb_match(Release.extlinks, 'url', extlink),
            array_jsonb_match(Release.extlinks, 'label', extlink),
            array_jsonb_match(Release.extlinks, 'name', extlink)
        ))

    if 'patch' in params:
        patch = params['patch']
        if str(patch).lower() == 'true':
            filters.append(Release.patch == True)
        elif str(patch).lower() == 'false':
            filters.append(Release.patch == False)
        else:
            raise ValueError(f"Invalid value for patch: {patch}. Use 'true' or 'false'.")

    if 'freeware' in params:
        freeware = params['freeware']
        if str(freeware).lower() == 'true':
            filters.append(Release.freeware == True)
        elif str(freeware).lower() == 'false':
            filters.append(Release.freeware == False)
        else:
            raise ValueError(f"Invalid value for freeware: {freeware}. Use 'true' or 'false'.")

    if 'uncensored' in params:
        uncensored = params['uncensored']
        if str(uncensored).lower() == 'true':
            filters.append(Release.uncensored == True)
        elif str(uncensored).lower() == 'false':
            filters.append(Release.uncensored == False)
        else:
            raise ValueError(f"Invalid value for uncensored: {uncensored}. Use 'true' or 'false'.")

    if 'official' in params:
        official = params['official']
        if str(official).lower() == 'true':
            filters.append(Release.official == True)
        elif str(official).lower() == 'false':
            filters.append(Release.official == False)
        else:
            raise ValueError(f"Invalid value for official: {official}. Use 'true' or 'false'.")

    if 'has_ero' in params:
        has_ero = params['has_ero']
        if str(has_ero).lower() == 'true':
            filters.append(Release.has_ero == True)
        elif str(has_ero).lower() == 'false':
            filters.append(Release.has_ero == False)
        else:
            raise ValueError(f"Invalid value for has_ero: {has_ero}. Use 'true' or 'false'.")

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

    if id := params.get('id'):
        return [Character.id == id]

    if search := params.get('search'):
        def process_character(character_value):
            return or_(
                Character.id == character_value,
                Character.name.ilike(f"%{character_value}%"),
                Character.original.ilike(f"%{character_value}%"),
                array_string_match(Character.aliases, character_value)
            )
        filters.append(process_multi_value_expression(search, process_character))

    if role := params.get('role'):
        filters.append(array_jsonb_exact_match(Character.vns, 'role', role))

    if blood_type := params.get('blood_type'):
        filters.append(Character.blood_type == blood_type)
    
    if sex := params.get('sex'):
        filters.append(array_string_match(Character.sex, sex))
    
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
    
    if cup := params.get('cup'):
        filters.append(create_cup_comparison_filter(cup))

    if age := params.get('age'):
        filters.append(create_comparison_filter(Character.age, age, int))

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

    if dtraits := params.get('dtrait'): #TODO
        raise ValueError("The 'dtraits' search field is not available for local searches.")

    if birthday := params.get('birthday'):
        filters.append(create_birthday_comparison_filter(birthday))

    if seiyuu := params.get('seiyuu'): #TODO
        ...

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

    if id := params.get('id'):
        return [Producer.id == id]

    if search := params.get('search'):
        def process_producer(producer_value):
            return or_(
                Producer.id == producer_value,
                Producer.name.ilike(f"%{producer_value}%"),
                Producer.original.ilike(f"%{producer_value}%"),
                array_string_match(Producer.aliases, producer_value)
            )
        filters.append(process_multi_value_expression(search, process_producer))
    
    if lang := params.get('lang'):
        filters.append(Producer.lang == lang)
    
    if type := params.get('type'):
        filters.append(Producer.type == type)
    
    return filters

def get_staff_filters(params: Dict[str, Any]) -> List[BinaryExpression]:
    filters = []

    if id := params.get('id'):
        return [Staff.id == id]

    if aid := params.get('aid'):
        return [Staff.aid == aid]

    if search := params.get('search'):
        def process_staff(staff_value):
            return or_(
                Staff.id == staff_value,
                Staff.name.ilike(f"%{staff_value}%"),
                Staff.original.ilike(f"%{staff_value}%"),
                array_jsonb_match(Staff.aliases, 'name', staff_value),
            )
        filters.append(process_multi_value_expression(search, process_staff))

    if lang := params.get('lang'):
        filters.append(Staff.lang == lang)
    
    if gender := params.get('gender'):
        filters.append(Staff.gender == gender)

    if role := params.get('role'):
        # TODO
        ...

    if extlink := params.get('extlink'):
        filters.append(or_(
            array_jsonb_exact_match(Staff.extlinks, 'id', extlink),
            array_jsonb_match(Staff.extlinks, 'url', extlink),
            array_jsonb_match(Staff.extlinks, 'label', extlink),
            array_jsonb_match(Staff.extlinks, 'name', extlink)
        ))
    
    if 'ismain' in params:
        ismain = params['ismain']
        if str(ismain).lower() == 'true':
            filters.append(Staff.ismain == True)
        elif str(ismain).lower() == 'false':
            filters.append(Staff.ismain == False)
        else:
            raise ValueError(f"Invalid value for ismain: {ismain}. Use 'true' or 'false'.")
    
    return filters

def get_tag_filters(params: Dict[str, Any]) -> List[BinaryExpression]:
    filters = []

    if id := params.get('id'):
        return [Tag.id == id]

    if search := params.get('search'):
        def process_tag(tag_value):
            return or_(
                Tag.id == tag_value,
                Tag.name.ilike(f"%{tag_value}%"),
                array_string_match(Tag.aliases, tag_value)
            )
        filters.append(process_multi_value_expression(search, process_tag))

    if category := params.get('category'):
        filters.append(Tag.category == category)
    
    return filters

def get_trait_filters(params: Dict[str, Any]) -> List[BinaryExpression]:
    filters = []
    
    if id := params.get('id'):
        return [Trait.id == id]

    if traits := params.get('search'):
        def process_trait(trait_value):
            return or_(
                Trait.id == trait_value,
                Trait.name.ilike(f"%{trait_value}%"),
                array_string_match(Trait.aliases, trait_value)
            )
        filters.append(process_multi_value_expression(traits, process_trait))
    
    return filters

def get_local_filters(search_type: str, params: Dict[str, Any]) -> List[BinaryExpression]:

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