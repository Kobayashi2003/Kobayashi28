import re
from api.search.filter import *
from api.utils.logger import search_logger
from typing import Dict, Set, List, Any, Optional, Tuple 


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

    if not fields: fields = ""

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
            OR EXISTS (
                SELECT 1
                FROM jsonb_array_elements(vn.data->'titles') AS t
                WHERE t->>'title' ILIKE %s
            )
            OR EXISTS (
                SELECT 1
                FROM jsonb_array_elements_text(vn.data->'aliases') AS alias
                WHERE alias ILIKE %s
            ))
            """,
            [title_param, title_param, title_param]
        ))

    if length:
        filters.append(("vn.data->>'length' = %s", [str(length)]))

    if tags:
        tag_conditions = []
        tag_params = []
        for tag in tags:
            tag_param = f"%{tag}%"
            tag_conditions.append("EXISTS (SELECT 1 FROM jsonb_array_elements(vn.data->'tags') AS t WHERE t->>'name' ILIKE %s)")
            tag_params.append(tag_param)
        filters.append((
            f"({' AND '.join(tag_conditions)})",
            tag_params
        ))

    if developers:
        dev_conditions = []
        dev_params = []
        for dev in developers:
            dev_param = f"%{dev}%"
            dev_conditions.append("EXISTS (SELECT 1 FROM jsonb_array_elements(vn.data->'developers') AS d WHERE d->>'name' ILIKE %s)")
            dev_params.append(dev_param)
        filters.append((
            f"({' OR '.join(dev_conditions)})",
            dev_params
        ))

    if characters:
        char_conditions = []
        char_params = []
        for char in characters:
            char_param = f"%{char}%"
            char_conditions.append("EXISTS (SELECT 1 FROM jsonb_array_elements(vn.data->'va') AS va WHERE va->'character'->>'name' ILIKE %s)")
            char_params.append(char_param)
        filters.append((
            f"({' OR '.join(char_conditions)})",
            char_params
        ))

    return filters

def generate_local_fields(fields: str = "", **kwargs) -> str:
    DEFAULT_FIELDS: str = (
        # vn.{field} -> str 
        "id,date,downloaded,"
        # vn.data.{field} -> str
        "title,olang,released,description,length,length_minutes,"
        # vn.data.{field} -> list[str]
        "languages,platforms,"
        # vn.data.{field} -> dict[str, str]
        "image,"
        # vn.data.{field} -> list[dict[str, str]]
        "titles,aliases,screenshots,tags,developers,relations,va,extlinks"
    )

    VN_FIELDS: Set[str] = {
        "id", "date", "downloaded", "data"
    }
    STRING_FIELDS: Set[str] = {
        "title", "olang", "released", 
        "description", "length", "length_minutes"
    }
    JSON_FIELDS: Set[str] = {
        "languages", "platforms", "image", "titles", 
        "aliases",  "screenshots", "va", "tags", 
        "developers", "relations", "extlinks"
    }

    FIELD_MAPPING: Dict[str, str] = {
        "vn": "vn.{} AS {}",
        "string": "vn.data->>'{}' AS {}",
        "json": "COALESCE(vn.data->'{}', '[]')::jsonb AS {}"
    }

    fields: List[str] = (fields or DEFAULT_FIELDS).replace(" ", "").split(",")
    output_fields: List[str] = []

    for field in fields:
        if field in VN_FIELDS:
            output_fields.append(FIELD_MAPPING["vn"].format(field, field))
        elif field in STRING_FIELDS:
            output_fields.append(FIELD_MAPPING["string"].format(field, field))
        elif field in JSON_FIELDS:
            output_fields.append(FIELD_MAPPING["json"].format(field, field))
        else:
            search_logger.warning(f"Unrecognized field: {field}")

    if "id" not in fields:
        output_fields.insert(0, "DISTINCT " + FIELD_MAPPING["string"].format("id", "id"))

    return ", ".join(output_fields)


VNDB_FIELDS_SIMPLE = "title, released, image.thumbnail, image.sexual, image.violence"
LOCAL_FIELDS_SIMPLE = "date, downloaded, title, released, image"