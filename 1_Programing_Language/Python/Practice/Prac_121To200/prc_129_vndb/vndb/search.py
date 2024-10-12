try:
    from vndb.utils import check_date
    from vndb.db import connect_db
except ImportError:
    from utils import check_date
    from db import connect_db

import requests
import json
import re
import datetime
import logging

logger = logging.getLogger(__name__)

class VN_Filter:
    def __init__(self, query: list) -> None:
        self.query = query
    def get_filters(self):
        return self.query

class VN_Operactor:
    def __init__(self, operator: str, filters: list | None) -> None:
        self.operator = operator
        self.filters = filters if filters else []
    def __add__(self, other):
        if isinstance(other, VN_Operactor) or isinstance(other, VN_Filter):
            self.filters.append(other)
            return self
        raise TypeError("unsupported operand type(s) for +: 'VN_Operactor' and '{}'".format(type(other)))
    def get_filters(self):
        return [self.operator] + [sub_filters.get_filters() for sub_filters in self.filters]

class VN_Operactor_And(VN_Operactor):
    def __init__(self, filters: list | None = None) -> None:
        super().__init__("and", filters)

class VN_Operactor_Or(VN_Operactor):
    def __init__(self, filters: list | None = None) -> None:
        super().__init__("or", filters)

class VN_Filter_ID(VN_Filter):
    def __init__(self, query: str = "") -> None:
        query = [] if not query else ["id", "=", query]
        super().__init__(query)

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

class VN_Filter_Length(VN_Filter):
    def __init__(self, query: int = 1) -> None:
        if query < 1 or query > 5:
            raise ValueError("Invalid length")
        query = [] if not query else ["length", "=", query]
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
        query = [] if not query else ["platform", "=", query]
        super().__init__(query)

class VN_Filter_DevStatus(VN_Filter):
    def __init__(self, query: int = 0) -> None:
        if query < 0 or query > 2:
            raise ValueError("Invalid devstatus")
        query = [] if not query else ["devstatus", "=", query]
        super().__init__(query)

class VN_Filter_HasDescription(VN_Filter):
    def __init__(self, query: bool = False) -> None:
        query = [] if not query else ["has_description", "=", 1]
        super().__init__(query)

class VN_Filter_HasAnime(VN_Filter):
    def __init__(self, query: bool = False) -> None:
        query = [] if not query else ["has_anime", "=", 1]
        super().__init__(query)

class VN_Filter_HasScreenshot(VN_Filter):
    def __init__(self, query: bool = False) -> None:
        query = [] if not query else ["has_screenshot", "=", 1]
        super().__init__(query)

class VN_Filter_HasReview(VN_Filter):
    def __init__(self, query: bool = False) -> None:
        query = [] if not query else ["has_review", "=", 1]
        super().__init__(query)

class VN_Filter_ReleasedDate(VN_Filter):
    def __init__(self, operator: str, date: str) -> None:
        if operator not in ["<", ">", "=", ">=", "<=", "!="]:
            raise ValueError("Invalid operator")
        if not check_date(date):
            raise ValueError("Invalid date format")
        query = (
        ["release", "=",
          ["and",
            ["released", operator, date],
              ["platform", "=", "win"],
              ["or",
                ["lang", "=", "ja"],
                # ["lang", "=", "zh-Hans"]
              ]
          ]
        ])
        super().__init__(query)

def generate_filters(query: str | None = None, filters: list | None = None) -> list:
    if not filters:
        filters = []
    if query:
        return ["search", "=", query] + filters
    return filters

def generate_fields(fields:                 str = "",
                    vn_info:                bool=False,
                    tags_info:              bool=False,
                    developers_info:        bool=False,
                    extlinks_info:          bool=False,
                    staff_info:             bool=False,
                    character_info:         bool=False,
                    character_va_info:      bool=False,
                    character_vns_info:     bool=False,
                    character_traits_info:  bool=False,
                    relations_info:         bool=False,
                    relations_vn_info:      bool=False,
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

def search_vndb(filters:    list,
                fields:     str,
                results:    int=100,
                sort:       str="",
                reverse:    bool=False,
                ) -> dict | None:

    logging.basicConfig(filename="search.log", level=logging.INFO)
    logger.info(f"{datetime.datetime.now()}: Searching VNDB with filters {filters}, fields {fields}, results {results}, sort {sort}, reverse {reverse}")

    url = "https://api.vndb.org/kana/vn"

    headers = {
        "Content-Type": "application/json"
    }

    sort = sort if sort in ['id', 'title', 'released'] else 'title'

    data = {
        "filters":  filters,
        "fields":   fields,
        "results":  results,
        "sort":     sort,
        "reverse":  reverse,
        "page":     1
    }

    more = True
    responses = []

    while more:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            response_json = json.loads(response.text)
            more = response_json['more']
            responses.append(response_json)
            data['page'] += 1
            logger.info(f"{datetime.datetime.now()}: {response.status_code} page {data['page']}")
        else:
            logger.error(f"{datetime.datetime.now()}: {response.status_code} {response.text}")
            break

    if not responses:
        return None

    # Merge responses results
    merged_results = []
    for response in responses:
        merged_results += response['results']

    logger.info(f"{datetime.datetime.now()}: {len(merged_results)} results found")

    return {
        "results": merged_results,
        "count":   len(merged_results)
    }

def search_local(title:      str = "",
                 tags:       str = "",
                 developers: str = "",
                 characters: str = "",
                 length:     int | str = "",
                 sort_by:    str = "",
                 sort_order: bool = False
                 ) -> list | None:

    logging.basicConfig(filename="search.log", level=logging.INFO)
    logger.info(f"{datetime.datetime.now()}: Searching local database with title {title}, tags {tags}, developers {developers}, characters {characters}, length {length}, sort_by {sort_by}, sort_order {sort_order}")

    localTitle      = title
    localDevelopers = developers
    localCharacters = characters
    localTags       = tags
    localLength     = length

    conn = connect_db()
    with conn.cursor() as curs:
        select_sentence = ""

        if localTitle:
            localTitle = localTitle.replace("'",  "''")
            select_sentence += f"""(
            SELECT DISTINCT data->>'id' AS id
            FROM vn
            WHERE data ->> 'title' ILIKE '%{localTitle}%'
            UNION
            SELECT DISTINCT data->>'id' AS id
            FROM vn, jsonb_array_elements(data->'titles') AS data_title
            WHERE data_title->>'title' ILIKE '%{localTitle}%'
            UNION
            SELECT DISTINCT data->>'id' AS id
            FROM vn, jsonb_array_elements(data->'alias') AS data_alias
            WHERE data_alias->>'name' ILIKE '%{localTitle}%'
            )"""
        if localDevelopers:
            localDevelopers = localDevelopers.replace("'",  "''")
            select_sentence += " INTERSECT " if select_sentence else ""
            select_sentence += f"""(
            SELECT DISTINCT
                data ->> 'id' AS id
            FROM vn, jsonb_array_elements(data -> 'developers') AS data_developers
            WHERE
                data_developers ->> 'name' ILIKE '%{localDevelopers}%'
                OR data_developers ->> 'original' ILIKE '%{localDevelopers}%'
            )"""
        if localCharacters:
            localCharacters = localCharacters.replace("'",  "''")
            select_sentence += " INTERSECT " if select_sentence else ""
            select_sentence += f"""(
            SELECT DISTINCT data->>'id' AS id
            FROM vn, jsonb_array_elements(data->'va') AS data_va
            WHERE
                data_va->'character'->>'name' ILIKE '%{localCharacters}%'
                OR data_va->'character'->>'original' ILIKE '%{localCharacters}%'
            )"""
        if localTags:
            localTags = localTags.replace("'",  "''")
            select_sentence += " INTERSECT " if select_sentence else ""
            select_sentence += f"""(
            SELECT DISTINCT data->>'id' AS id
            FROM vn, jsonb_array_elements(data->'tags') AS data_tags
            WHERE data_tags->>'name' ILIKE '%{localTags}%'
            )"""
        if localLength:
            select_sentence += " INTERSECT " if select_sentence else ""
            if isinstance(localLength, str):
                localLength = {'very-short': 1,'short': 2, 'medium': 3, 'long': 4,'very-long': 5}[localLength]
            elif localLength < 1 or localLength > 5:
                raise ValueError("Invalid length")
            select_sentence += f"""(
            SELECT DISTINCT data->>'id' AS id
            FROM vn
            WHERE data->>'length' = '{localLength}'
            )"""
        curs.execute(f"""
        SELECT
            data ->> 'id' as id,
            data ->> 'title' as title,
            data -> 'image' ->> 'thumbnail' as thumbnail,
            data -> 'image' ->> 'sexual' as image__sexual,
            data -> 'image' ->> 'violence' as image__violence
        FROM vn
        WHERE data ->> 'id' IN (
            {select_sentence if select_sentence else "SELECT data->>'id' FROM vn"}
        ) ORDER BY {
            {
                "id":       "data ->> 'id'",
                "title":    "data ->> 'title'",
                "released": "data ->> 'released'",
            }.get(sort_by, "data ->> 'title'")
        } {
            "DESC" if sort_order else "ASC"
        }""")
        result = curs.fetchall()

        logger.info(f"{datetime.datetime.now()}: {len(result)} results found")

        return result


def test1():
    filters = generate_filters(filters=(
        VN_Operactor_And() + VN_Filter_Developer('HOOKSOFT') + VN_Filter_ReleasedDate('>', '2021-01-01')).get_filters())
    result = search_vndb(filters=filters, fields=generate_fields())
    if result:
        with open("result.json", "w") as f:
            json.dump(result, f, indent=4)
        print("Result saved to result.json")
    else:
        print("No result found")


def test2():
    filters = generate_filters(query='セレクトオブリージュ')
    result = search_vndb(filters=filters, fields=generate_fields())
    if result:
        with open("result.json", "w") as f:
            json.dump(result, f, indent=4)
        print("Result saved to result.json")
    else:
        print("No result found")


def test3():
    filters = generate_filters(query='セレクトオブリージュ')
    fields = generate_fields("""id, title, image.thumbnail, image.sexual, image.violence""")
    result = search_vndb(filters=filters, fields=fields)
    if result:
        with open("result.json", "w") as f:
            json.dump(result, f, indent=4)
        print("Result saved to result.json")
    else:
        print("No result found")
