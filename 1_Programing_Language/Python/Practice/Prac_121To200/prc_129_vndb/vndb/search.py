from flask import current_app, render_template, request, abort, redirect, url_for, Blueprint, jsonify

from vndb.db import connect_db
from vndb.utils import format_description, judge_violence, judge_sexual, check_date

import requests
import json
import re

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

def __generate_filters(query: str | None = None, filters: list | None = None) -> list:
    if not filters:
        filters = []
    if query:
        return ["search", "=", query] + filters
    return filters

def generate_filters(query:         str | None = None,
                     id:            str | None = None,
                     developers:    list | None = None,
                     characters:    list | None = None,
                     staffs:        list | None = None,
                     released_date_expressions: list | None = None,
                     length:        int | None = None,
                     dev_status:    int | None = None, 
                     has_anime:     bool | None = None,
                     has_screenshot:bool | None = None,
                     has_review:    bool | None = None,
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
        else:
            break

    if not responses:
        return None

    # Merge responses results
    merged_results = []
    for response in responses:
        merged_results += response['results']


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
                 reverse: bool = False
                 ) -> list | None:

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
            data -> 'image' ->> 'violence' as image__violence,
            date
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
            "DESC" if reverse else "ASC"
        }""")
        result = curs.fetchall()

        return result

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


search_bp = Blueprint('search', __name__, url_prefix='/search')

@search_bp.route('/', methods=['GET'])
def search():

    searchType  = request.args.get('searchType') 

    if searchType == 'local':
        localTitle      = request.args.get('localTitle')
        localDevelopers = request.args.get('localDevelopers')
        localCharacters = request.args.get('localCharacters')
        localTags       = request.args.get('localTags')
        localLength     = request.args.get('localLength')

        results = search_local(title=localTitle, developers=localDevelopers, characters=localCharacters, 
                              tags=localTags, length=localLength)
        results = results if results else []

        # return render_template('test.html', test=localTitle)

    elif searchType == 'vndb':

        params = filters_params()

        vndbQuery       = request.args.get('vndbQuery')
        vndbDevelopers  = request.args.get('vndbDevelopers')
        vndbCharacters  = request.args.get('vndbCharacters')
        vndbStaffs      = request.args.get('vndbStaffs')
        vndbReleasedDate= request.args.get('vndbReleasedDate')
        vndbLength      = request.args.get('vndbLength')
        vndbDevStatus   = request.args.get('vndbDevStatus')
        vndbHasDescription = request.args.get('vndbHasDescription')
        vndbHasAnime    = request.args.get('vndbHasAnime')
        vndbHasScreenshot = request.args.get('vndbHasScreenshot')
        vndbHasReview   = request.args.get('vndbHasReview')

        if vndbQuery:
            params['query'] = vndbQuery
        if vndbDevelopers:
            params['developers'] = [ developer.strip() for developer in vndbDevelopers.split(',') ]
        if vndbStaffs:
            params['staffs'] = [ staff.strip() for staff in vndbStaffs.split(',') ]
        if vndbCharacters:
            params['characters'] = [ character.strip() for character in vndbCharacters.split(',') ]
        if vndbReleasedDate:
            params['released_date_expressions'] = vndbReleasedDate.split(',')
        if vndbLength:
            params['length'] = int(vndbLength)
        if vndbDevStatus:
            params['dev_status'] = int(vndbDevStatus)
        if vndbHasDescription == 'on':
            params['has_description'] = True
        if vndbHasAnime == 'on':
            params['has_anime'] = True
        if vndbHasScreenshot == 'on':
            params['has_screenshot'] = True
        if vndbHasReview == 'on':
            params['has_review'] = True

        fields = generate_fields("""id, title, image.thumbnail, image.sexual, image.violence""")
        filters = generate_filters(**params)
        # return render_template('test.html', test=filters)
        results = search_vndb(filters=filters, fields=fields)
        results = results['results'] if results else []
        results = [[result['id'], result['title'],
                   result['image']['thumbnail'] if result['image'] is not None and 'thumbnail' in result['image'] else '',
                   result['image']['sexual']    if result['image'] is not None and 'sexual' in result['image'] else 0,
                   result['image']['violence']  if result['image'] is not None and 'violence' in result['image'] else 0
                   ] for result in results] if results else []
    else:
        results = []
        
    vns = [{
        'id':               result[0],
        'title':            result[1],
        'thumbnail':        result[2],
        'image__sexual':    judge_sexual(float(result[3])),
        'image__violence':  judge_violence(float(result[4])),
        'date':             result[5] if searchType == 'local' else ''
    } for result in results]
    
    if request.args.get('format') == 'json':
        return jsonify(vns), 200

    return render_template('index/index.html', vns=vns)
