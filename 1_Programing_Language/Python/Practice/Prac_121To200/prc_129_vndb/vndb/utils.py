import requests
import json

import re
from typing import List


def judge_sexual(sexual: float) -> bool:
    if (sexual > 1):
        return True
    return False

def judge_violence(violence: float) -> bool:
    if (violence > 1):
        return True
    return False

def check_date(date_str: str) -> bool:
    # date should match format YYYY-MM-DD or YYYY-MM or YYYY
    match = re.match(r"^(\d{4})(-\d{2})?(-\d{2})?$", date_str)
    if not match:
        return False
    year, month, day = match.groups()
    if year:
        year = int(year)
        if year < 1900 or year > 2100:
            return False
    if month:
        month = int(month[1:])
        if month < 1 or month > 12:
            return False
    if day:
        month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if year % 4 == 0 and (year % 100!= 0 or year % 400 == 0):
            month_days[1] = 29
        day = int(day[1:])
        if day < 1 or day > month_days[month - 1]:
            return False
    return True

def format_date(date_str: str) -> str:
    # YYYY => YYYY-01-01
    # YYYY-MM => YYYY-MM-01
    match = re.match(r"^(\d{4})(-\d{2})?(-\d{2})?$", date_str)
    year, month, day = match.groups()
    if month is None:
        month = "-01"
    if day is None:
        day = "-01"
    return f"{year}{month}{day}"

def format_description(description: str) -> str:
    if description is None:
        return ""
    description = re.sub(r"\[url=.*?\](.*?)\[/url\]", r"\1", description)
    description = re.sub(r"\[([bis])\](.*?)\[/\1\]", r"\2", description)
    description = re.sub(r"\[.*?\]", "", description)
    return description


def search_vndb(filters: list,
                fields: str,
                results: int=100,
                sort: str="",
                page: int=1
                ) -> dict|None:
    url = "https://api.vndb.org/kana/vn"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "filters": filters,
        "fields": fields,
        "results": results,
        "sort": sort,
        "page": page
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        print(f"Error: {response.status_code} {response.text}")
    return None


def generate_filters(query:     str|None=None,
                     developer: str|None=None,
                     character: str|None=None,
                     seiyuu:    str|None=None,
                     staff:     str|None=None,
                     olang:     str|None=None,
                     lang:      List[str]|None=None,
                     platforms: List[str]|None=None,
                     released_min: str|None=None,
                     released_max: str|None=None
              ) -> list:
    filters = ["and"]
    if query is not None:
        filters.append(["search", "=", query])
    if platforms is not None:
        filters.append(["or"].extend([["platforms", "=", platform] for platform in platforms]))
    if developer is not None:
        filters.append(["developer", "=", ["search", "=", developer]])
    if character is not None:
        filters.append(["character", "=", ["search", "=", character]])
    if seiyuu is not None:
        filters.append(["character", "=", ["seiyuu", "=", ["search", "=", seiyuu]]])
    if staff is not None:
        filters.append(["staff", "=", ["search", "=", staff]])
    if released_min is not None and check_date(released_min):
        filters.append(["released", ">=", format_date(released_min)])
    if released_max is not None and check_date(released_max):
        filters.append(["released", "<=", format_date(released_max)])
    if lang is not None:
        filters.append(["or"].extend([["lang", "=", lang] for lang in lang]))
    if olang is not None:
        filters.append(["olang", "=", olang])

    if filters == ["and"]:
        return []
    return filters


def generate_fields(vn_info:            bool=False,
                    tags_info:          bool=False,
                    developers_info:    bool=False,
                    staff_info:         bool=False,
                    character_info:     bool=False,
                    character_va_info:  bool=False,
                    character_vns_info: bool=False,
                    character_traits_info: bool=False,
                    relations_info:     bool=False,
                    relations_vn_info:  bool=False,
                    ) -> str:
    fields = ""

    if vn_info:
        fields += """
        title, titles.title, titles.lang, titles.official, titles.main, aliases,
        image.url, image.dims, image.sexual, image.violence,
        image.thumbnail, image.thumbnail_dims,
        screenshots.url, screenshots.dims, screenshots.sexual, screenshots.violence,
        screenshots.thumbnail, screenshots.thumbnail_dims,
        olang, languages, platforms, released, length, length_minutes, description,
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
        va.staff.name, va.staff.original
"""

    fields = fields.strip().replace("\n", "").replace(" ", "")
    if fields[-1] == ",":
        fields = fields[:-1]
    return fields


if __name__ == "__main__":
    query = 'セレクトオブリージュ'
    filters = generate_filters(query=query)
    fields = generate_fields()
    result = search_vndb(filters=filters, fields=fields)

    if result:
        with open("result.json", "w") as f:
            json.dump(result, f, indent=4)
        print("Result saved to result.json")
    else:
        print("No result found")
