from vndb.utils import check_date

import requests
import json
import re

class VN_Filter:
    def __init__(self, query: list) -> None:
        self.query = query

class VN_Operactor:
    def __init__(self, operator: str, filters: list | None) -> None:
        self.operator = operator
        self.filters = filters if filters else []
    def __add__(self, other):
        if isinstance(other, VN_Operactor):
            self.filters.append(other.filters)
            return self
        if isinstance(other, VN_Filter):
            self.filters.append(other.query)
            return self
        raise TypeError("unsupported operand type(s) for +: 'VN_Operactor' and '{}'".format(type(other)))
    def get_filters(self):
        return [self.operator] + self.filters

class VN_Operactor_And(VN_Operactor):
    def __init__(self, filters: list | None = None) -> None:
        super().__init__("and", filters)

class VN_Operactor_Or(VN_Operactor):
    def __init__(self, filters: list | None = None) -> None:
        super().__init__("or", filters)

class VN_Filter_Staff(VN_Filter):
    def __init__(self, query: str = "") -> None:
        query = [] if not query else ["staff", "=", ["search", "=", query]]
        super().__init__(query)

class VN_Filter_Character(VN_Filter):
    def __init__(self, query: str = "") -> None:
        query = [] if not query else ["character", "=", ["search", "=", query]]
        super().__init__(query)

class VN_Filter_Developer(VN_Filter):
    def __init__(self, query: str = "") -> None:
        query = [] if not query else ["developer", "=", ["search", "=", query]]
        super().__init__(query)

class VN_Filter_Language(VN_Filter):
    def __init__(self, query: str = "") -> None:
        query = [] if not query else ["lang", "=", query]
        super().__init__(query)

class VN_Filter_OriginalLanguage(VN_Filter):
    def __init__(self, query: str = "") -> None:
        query = [] if not query else ["olang", "=", query]
        super().__init__(query)

class VN_Filter_Platform(VN_Filter):
    def __init__(self, query: str = "") -> None:
        query = [] if not query else ["platforms", "=", query]
        super().__init__(query)

class Vn_Filter_Tags(VN_Filter):
    def __init__(self, query: str = "") -> None:
        query = [] if not query else ["tags", "=", ["search", "=", query]]
        super().__init__(query)

class VN_Filter_ReleasedDate(VN_Filter):
    def __init__(self, operator: str, date: str) -> None:
        if operator not in ["<", ">", "=", ">=", "<=", "!="]:
            raise ValueError("Invalid operator")
        if not check_date(date):
            raise ValueError("Invalid date format")
        super().__init__(["released", operator, date])

class VN_Filter_Seiyuu(VN_Filter):
    def __init__(self, query: str = "") -> None:
        query = [] if not query else ["character", "=", ["seiyuu", "=", ["search", "=", query]]]
        super().__init__(query)


def generate_filters(query: str | None = None, filters: list | None = None) -> list:
    if not filters:
        filters = []
    if query:
        return ["search", "=", query] + filters
    return filters


def generate_fields(vn_info:            bool=False,
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
    fields = ""

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
    if fields[-1] == ",":
        fields = fields[:-1]
    return fields


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


def search_local(title: str = "", developers: str = "", character: str = "") -> list:
    pass


def test1():
    filters = generate_filters(filters=(
        VN_Operactor_And() + VN_Filter_Developer('HOOKSOFT') + VN_Filter_ReleasedDate('>', '2021-01-01')).get_filters())
    result = search_vndb(filters=filters, fields=generate_fields())
    if result:
        with open("result.json", "w") as f:
            json.dump(result, f, indent=4)
        print("Result saved to result.json")
    print("No result found")


def test2():
    filters = generate_filters(query='セレクトオブリージュ')
    result = search_vndb(filters=filters, fields=generate_fields())
    if result:
        with open("result.json", "w") as f:
            json.dump(result, f, indent=4)
        print("Result saved to result.json")
    print("No result found")
