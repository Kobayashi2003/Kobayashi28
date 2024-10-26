import re
import json
from api.search.filter import *
from typing import List, Dict, Any, Optional, Tuple


def generate_vndb_filters(
    query:      Optional[str] = None,
    id:         Optional[str] = None,
    developers: Optional[List[str]] = None,
    characters: Optional[List[str]] = None,
    staffs:     Optional[List[str]] = None,
    released_date_expressions: Optional[List[str]] = None,
    length:     Optional[int] = None,
    dev_status: Optional[int] = None, 
    has_anime:  Optional[bool] = None,
    has_review: Optional[bool] = None,
    has_screenshot: Optional[bool] = None,
    has_description: Optional[bool] = None,
    **kwargs
) -> List[Any]:

    and_container = VN_Operactor_And()

    if id: 
        and_container += VN_Filter_ID(id)

    if developers and any(developers):
        or_container = VN_Operactor_Or()
        for developer in developers:
            if not developer: continue
            or_container += VN_Filter_Developer(developer)
        and_container += or_container

    if characters and any(characters):
        or_container = VN_Operactor_Or()
        for character in characters:
            if not character: continue
            or_container += VN_Filter_Character(character)
        and_container += or_container

    if staffs and any(staffs):
        or_container = VN_Operactor_Or()
        for staff in staffs:
            if not staff: continue
            or_container += VN_Filter_Staff(staff)
        and_container += or_container

    if released_date_expressions:
        expression_match = re.compile(r'(\<|\<=|\>|\>=|=|\!=)\s*(\d{4}-\d{2}-\d{2}|\d{4}-\d{2}|\d{4})')
        for expression in released_date_expressions:
            match = expression_match.match(expression)
            if not match: continue
            operator, date = match.groups()
            and_container += VN_Filter_ReleasedDate(operator, date)

    if length:
        and_container += VN_Filter_Length(length)

    if dev_status:
        and_container += VN_Filter_DevStatus(dev_status)

    if has_anime:
        and_container += VN_Filter_HasAnime(has_anime)

    if has_screenshot:
        and_container += VN_Filter_HasScreenshot(has_screenshot)

    if has_review:
        and_container += VN_Filter_HasReview(has_review)

    if has_description:
        and_container += VN_Filter_HasDescription(has_description)
    
    filters = and_container.get_filters()
    filters = filters if len(filters) > 1 else []

    if query:
        return ["search", "=", query] + filters
    return filters

def generate_vndb_fields(
    fields:             str = "",
    vn_info:            bool = False,
    tags_info:          bool = False,
    developers_info:    bool = False,
    extlinks_info:      bool = False,
    staff_info:         bool = False,
    character_info:     bool = False,
    character_va_info:  bool = False,
    character_vns_info: bool = False,
    character_traits_info: bool = False,
    relations_info:     bool = False,
    relations_vn_info:  bool = False,
    **kwargs
) -> str:

    if vn_info:
        fields += """
        title, titles.title, titles.lang, titles.official, titles.main, aliases,
        image.url, image.dims, image.sexual, image.violence,
        image.thumbnail, image.thumbnail_dims,
        screenshots.url, screenshots.dims, screenshots.sexual, screenshots.violence,
        screenshots.thumbnail, screenshots.thumbnail_dims,
        olang, languages, platforms, released, description,
        length, length_minutes, devstatus,
"""

    if tags_info:
        fields += """
        tags.name, tags.aliases, tags.description,
        tags.category, tags.rating, tags.spoiler, tags.lie,
"""

    if developers_info:
        fields += """
        developers.name, developers.original, developers.aliases,
        developers.lang, developers.type, developers.description,
"""

    if relations_info:
        fields += """
        relations.relation, relations.relation_official, relations.title,
"""

    if relations_info and relations_vn_info:
        fields += "".join([f"relations.{field}," for field in re.findall(r"([\w\.]+)", """
        titles.title, titles.lang, titles.official, titles.main, aliases,
        image.url, image.dims, image.sexual, image.violence,
        image.thumbnail, image.thumbnail_dims,
        screenshots.url, screenshots.dims, screenshots.sexual, screenshots.violence,
        screenshots.thumbnail, screenshots.thumbnail_dims,
        olang, languages, platforms, released, length, length_minutes, description,
""")])

    if staff_info:
        fields += """
        staff.name, staff.original, staff.lang, staff.gender, staff.role, staff.description,
"""

    if character_info:
        fields += """
        va.character.name, va.character.original, va.character.aliases,
        va.character.description, va.character.blood_type, va.character.sex,
        va.character.height, va.character.weight, va.character.age, va.character.birthday,
        va.character.bust, va.character.waist, va.character.hips, va.character.cup,
        va.character.image.url, va.character.image.dims,
        va.character.image.sexual, va.character.image.violence,
        va.character.vns.role, va.character.vns.title,
"""

    if character_info and character_traits_info:
        fields += """
        va.character.traits.name, va.character.traits.aliases,
        va.character.traits.description, va.character.traits.spoiler,
        va.character.traits.lie, va.character.traits.group_id,
        va.character.traits.group_name,
"""

    if character_info and character_va_info:
        fields += "".join([f"va.{field}," for field in re.findall(r"([\w\.]+)", """
        staff.name, staff.original, staff.lang, staff.gender, staff.description,
""")])

    if character_info and character_vns_info:
        fields += "".join([f"va.character.vns.{field}," for field in re.findall(r"([\w\.]+)", """
        titles.title, titles.lang, titles.official, titles.main, aliases,
        image.url, image.dims, image.sexual, image.violence,
        image.thumbnail, image.thumbnail_dims,
        screenshots.url, screenshots.dims, screenshots.sexual, screenshots.violence,
        screenshots.thumbnail, screenshots.thumbnail_dims,
        olang, languages, platforms, released, length, length_minutes, description,
""")])

    if extlinks_info:
        fields += """
        extlinks.url, extlinks.label, extlinks.name
"""

    if not fields:
        fields += """
        title, titles.title, titles.lang, titles.official, titles.main, aliases,
        image.url, image.dims, image.sexual, image.violence,
        image.thumbnail, image.thumbnail_dims,
        screenshots.url, screenshots.dims, screenshots.sexual, screenshots.violence,
        screenshots.thumbnail, screenshots.thumbnail_dims,
        olang, languages, platforms, released, length, length_minutes, description,
        tags.name, tags.category, developers.name, developers.original,
        relations.relation, relations.relation_official, relations.title,
        va.character.name, va.character.original, va.character.aliases,
        va.character.description, va.character.blood_type, va.character.sex,
        va.character.height, va.character.weight, va.character.age, va.character.birthday,
        va.character.bust, va.character.waist, va.character.hips, va.character.cup,
        va.character.image.url, va.character.image.dims,
        va.character.image.sexual, va.character.image.violence,
        va.character.vns.role, va.character.vns.title,
        va.staff.name, va.staff.original, extlinks.url,
"""

    fields = fields.strip().replace("\n", "").replace(" ", "")
    fields = fields[:-1] if fields[-1] == "," else fields

    return fields

def generate_local_filters(
    id:         Optional[str] = None,
    title:      Optional[str] = None,
    length:     Optional[int] = None,
    tags:       Optional[List[str]] = None,
    developers: Optional[List[str]] = None,
    characters: Optional[List[str]] = None,
    **kwargs
) -> List[Tuple[str, List[Any]]]:
    filters = []

    if id:
        filters.append(("vn.data->>'id' = %s", [id]))

    if title:
        title_param = f"%{title}%"
        filters.append((
            """
            (vn.data->>'title' ILIKE %s
            OR vn.data->'titles' @> %s::jsonb
            OR vn.data->'aliases' @> %s::jsonb)
            """,
            [title_param, json.dumps([{"title": title_param}]), json.dumps([title_param])]
        ))

    if length:
        filters.append(("vn.data->>'length' = %s", [str(length)]))

    if tags:
        filters.append(("vn.data->'tags' @> %s::jsonb", [json.dumps([{"name": tag} for tag in tags])]))

    if developers:
        filters.append(("vn.data->'developers' @> %s::jsonb", [json.dumps([{"name": dev} for dev in developers])]))

    if characters:
        filters.append((
            """
            EXISTS (
                SELECT 1
                FROM jsonb_array_elements(vn.data->'va') AS va
                WHERE va->'character'->>'name' ILIKE ANY(%s)
            )
            """,
            [[f"%{char}%" for char in characters]]
        ))

    return filters

def generate_local_fields(
    fields: str = "", 
    **kwargs
) -> str:
    if not fields:
        return generate_local_fields("date, downloaded" + generate_vndb_fields())

    fields = fields.strip().replace("\n", "").replace(" ", "").split(",")
    output_fields = []

    for field in fields:
        if field in {"id", "date", "downloaded", "data"}:
            output_fields.append(f'vn.{field}')
        else:
            output_fields.append(f"vn.data->'{'->'.join(field.split('.'))}' AS {field.replace('.', '_')}")
        
    if "id" not in fields:
        output_fields.insert(0, "DISTINCT vn.data->>'id' AS id")

    return ", ".join(output_fields)

def generate_filters(search_type: str, **kwargs) -> Any:
    if search_type == "vndb":
        return generate_vndb_filters(**kwargs)
    elif search_type == "local":
        return generate_local_filters(**kwargs)

    return None

def generate_fields(search_type: str, **kwargs) -> str:
    if search_type == "vndb":
        return generate_vndb_fields(**kwargs)
    elif search_type == "local":
        return generate_local_fields(**kwargs)
    
    return None


VNDB_FIELDS_SIMPLE = generate_vndb_fields("title, released, image.thumbnail, image.sexual, image.violence")
LOCAL_FILELDS_SIMPLE = generate_local_fields("date, download, title, released, image.thumbnail, image.sexual, image.violence")