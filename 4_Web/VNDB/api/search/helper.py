from api.search.filter import *

import re

def __generate_filters(query: str | None = None, filters: list | None = None) -> list:
    if not filters:
        filters = []
    if query:
        return ["search", "=", query] + filters
    return filters

def generate_filters(
    query:      str | None = None,
    id:         str | None = None,
    developers: list | None = None,
    characters: list | None = None,
    staffs:     list | None = None,
    released_date_expressions: list | None = None,
    length:     int | None = None,
    dev_status: int | None = None, 
    has_anime:  bool | None = None,
    has_review: bool | None = None,
    has_screenshot: bool | None = None,
    has_description: bool | None = None,
) -> list:

    and_container = VN_Operactor_And()

    if id:
        and_container += VN_Filter_ID(id)
    if developers:
        or_container = VN_Operactor_Or()
        for developer in developers:
            or_container += VN_Filter_Developer(developer)
        and_container += or_container
    if characters:
        or_container = VN_Operactor_Or()
        for character in characters:
            or_container += VN_Filter_Character(character)
        and_container += or_container
    if staffs:
        or_container = VN_Operactor_Or()
        for staff in staffs:
            or_container += VN_Filter_Staff(staff)
        and_container += or_container
    if released_date_expressions:
        expression_match = re.compile(r'(\<|\<=|\>|\>=|=|\!=)\s*(\d{4}-\d{2}-\d{2}|\d{4}-\d{2}|\d{4})')
        for expression in released_date_expressions:
            match = expression_match.match(expression)
            if not match:
                raise ValueError("Invalid released date expression")
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

    return __generate_filters(query, filters)

def generate_fields(
    fields:             str = "",
    vn_info:            bool=False,
    tags_info:          bool=False,
    developers_info:    bool=False,
    extlinks_info:      bool=False,
    staff_info:         bool=False,
    character_info:     bool=False,
    character_va_info:  bool=False,
    character_vns_info: bool=False,
    character_traits_info: bool=False,
    relations_info:     bool=False,
    relations_vn_info:  bool=False,
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

    if fields == "":
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

def filters_params() -> dict:
    return {
        "query": None, # str = "",
        "id": None, # str | None = None,
        "developers": None, # list | None = None,
        "characters": None, # list | None = None,
        "staffs": None, # list | None = None,
        "released_date_expressions": None, # list | None = None,
        "length": None, # int | None = None,
        "dev_status": None, # int | None = None,
        "has_anime": None, # bool | None = None,
        "has_screenshot": None, # bool | None = None,
        "has_review": None, # bool | None = None,
        "has_description": None, # bool | None = None,
    }

def fields_params() -> dict:
    return {
        "vn_info": True, # bool=False,
        "tags_info": True, # bool=False,
        "developers_info": True, # bool=False,
        "extlinks_info": True, # bool=False,
        "staff_info": True, # bool=False,
        "character_info": True, # bool=False,
        "character_va_info": True, # bool=False,
        "character_vns_info": True, # bool=False,
        "character_traits_info": True, # bool=False,
        "relations_info": True, # bool=False,
        "relations_vn_info": True, # bool=False,
    }
