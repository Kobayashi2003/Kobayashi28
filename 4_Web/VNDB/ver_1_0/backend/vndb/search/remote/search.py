import httpx
from typing import Any, Callable
from enum import Enum

from .filters import get_remote_filters
from .fields import get_remote_fields, validate_sort


VNDB_API_URL = "https://api.vndb.org/kana"

class VNDBEndpoint(Enum):
    VN = "vn"
    CHARACTER = "character"
    PRODUCER = "producer"
    STAFF = "staff"
    TAG = "tag"
    TRAIT = "trait"
    RELEASE = "release"

class VNDBAPIWrapper:
    def __init__(self, api_token: str | None = None):
        self.client = httpx.Client()
        self.client.headers.update({"Content-Type": "application/json"})
        if api_token:
            self.client.headers.update({"Authorization": f"Token {api_token}"})

    def query(self, endpoint: VNDBEndpoint, filters: list, fields: list[str], 
              sort: str = "id", reverse: bool = False, results: int = 10, page: int = 1, count: bool = True) -> dict[str, Any]:
        url = f"{VNDB_API_URL}/{endpoint.value}"
        
        payload = {
            "filters": filters,
            "fields": ",".join(fields),
            "sort": sort,
            "reverse": reverse,
            "results": results,
            "page": page,
            "count": count
        }
        
        response = self.client.post(url, json=payload)

        # TODO:DEBUG
        from vndb.logger import add_log_entry
        if response.status_code != 200:
            level = "error"
            message = f"Error querying {endpoint.value}"
            details = {
                "from": "remote",
                "url": url,
                "payload": payload,
                "status_code": response.status_code,
                "response": response.json()
            }
        else:
            level = "info"
            message = f"Successfully queried {endpoint.value}"
            details = {
                "from": "remote",
                "url": url,
                "payload": payload,
            }
        add_log_entry(level, message, details)

        response.raise_for_status()
        return response.json()

    def get_vn(self, filters: dict[str, Any], fields: list[str], **kwargs) -> dict[str, Any]:
        return self.query(VNDBEndpoint.VN, filters, fields, **kwargs)

    def get_character(self, filters: dict[str, Any], fields: list[str], **kwargs) ->   dict[str, Any]:
        return self.query(VNDBEndpoint.CHARACTER, filters, fields, **kwargs)

    def get_producer(self, filters: dict[str, Any], fields: list[str], **kwargs) -> dict[str, Any]:
        return self.query(VNDBEndpoint.PRODUCER, filters, fields, **kwargs)

    def get_staff(self, filters: dict[str, Any], fields: list[str], **kwargs) -> dict[str, Any]:
        return self.query(VNDBEndpoint.STAFF, filters, fields, **kwargs)

    def get_tag(self, filters: dict[str, Any], fields: list[str], **kwargs) -> dict[str, Any]:
        return self.query(VNDBEndpoint.TAG, filters, fields, **kwargs)

    def get_trait(self, filters: dict[str, Any], fields: list[str], **kwargs) -> dict[str, Any]:
        return self.query(VNDBEndpoint.TRAIT, filters, fields, **kwargs)

    def get_release(self, filters: dict[str, Any], fields: list[str], **kwargs) -> dict[str, Any]:
        return self.query(VNDBEndpoint.RELEASE, filters, fields, **kwargs)

    def update_user_list(self, vn_id: str, data: dict[str, Any]) -> None:
        url = f"{VNDB_API_URL}/ulist/{vn_id}"
        response = self.client.patch(url, json=data)
        response.raise_for_status()

    def update_release_list(self, release_id: str, status: int) -> None:
        url = f"{VNDB_API_URL}/rlist/{release_id}"
        response = self.client.patch(url, json={"status": status})
        response.raise_for_status()

    def remove_from_user_list(self, vn_id: str) -> None:
        url = f"{VNDB_API_URL}/ulist/{vn_id}"
        response = self.client.delete(url)
        response.raise_for_status()

    def remove_from_release_list(self, release_id: str) -> None:
        url = f"{VNDB_API_URL}/rlist/{release_id}"
        response = self.client.delete(url)
        response.raise_for_status()

    def get_auth_info(self) -> dict[str, Any]:
        url = f"{VNDB_API_URL}/authinfo"
        response = self.client.get(url)
        response.raise_for_status()
        return response.json()

api = VNDBAPIWrapper()


def memoize(timeout=60*60*24):
    try:
        from vndb import cache
        return cache.memoize(timeout=timeout)
    except ImportError:
        return lambda f: f

def unpaginated_search(search_function: Callable, **kwargs) -> dict[str, Any]:
    results = []
    page = 1
    more = True
    while more:
        response = search_function(**kwargs, page=page)
        results.extend(response.get('results', []))
        more = response.get('more', False)
        page += 1
    
    return {'results': results, 'total': len(results), 'count': len(results)}

def paginated_results(results: dict[str, Any], sort: str = 'id', reverse: bool = False, limit: int = 10, page: int = 1, count: bool = True) -> dict[str, Any]:
    if not results or 'results' not in results:
        return {'results': [], 'count': 0} if count else {'results': []}
    
    results = results['results']
    count = len(results)
    start_index = (page - 1) * limit
    end_index = start_index + limit

    results.sort(key=lambda x: x.get(sort, 0), reverse=reverse)
    results = results[start_index:end_index]

    results = {'results': results, 'more': end_index < count}
    if count:
        results['count'] = count
    
    return results


def search_vn(filters: dict[str, Any], fields: list[str], page: int = 1, **kwargs) -> dict[str, Any]:
    return api.get_vn(filters, fields, page=page, **kwargs)

def search_character(filters: dict[str, Any], fields: list[str], page: int = 1, **kwargs) -> dict[str, Any]:
    return api.get_character(filters, fields, page=page, **kwargs)

def search_tag(filters: dict[str, Any], fields: list[str], page: int = 1, **kwargs) -> dict[str, Any]:
    return api.get_tag(filters, fields, page=page, **kwargs)

def search_producer(filters: dict[str, Any], fields: list[str], page: int = 1, **kwargs) -> dict[str, Any]:
    return api.get_producer(filters, fields, page=page, **kwargs)

def search_staff(filters: dict[str, Any], fields: list[str], page: int = 1, **kwargs) -> dict[str, Any]:
    return api.get_staff(filters, fields, page=page, **kwargs)

def search_trait(filters: dict[str, Any], fields: list[str], page: int = 1, **kwargs) -> dict[str, Any]:
    return api.get_trait(filters, fields, page=page, **kwargs)

def search_release(filters: dict[str, Any], fields: list[str], page: int = 1, **kwargs) -> dict[str, Any]:
    return api.get_release(filters, fields, page=page, **kwargs)

def search(resource_type: str, params: dict[str, Any], response_size: str = 'small',
           page: int = 1, limit: int = 100, 
           sort: str = 'id', reverse: bool = False, count: bool = True) -> dict[str, Any]:

    search_functions = {
        'vn': search_vn,
        'character': search_character,
        'tag': search_tag,
        'producer': search_producer,
        'staff': search_staff,
        'trait': search_trait,
        'release': search_release
    }

    if resource_type not in search_functions:
        raise ValueError(f"Invalid search type: {resource_type}")

    filters = get_remote_filters(resource_type, params)
    fields = get_remote_fields(resource_type, response_size)
    sort = validate_sort(resource_type, sort)

    if not filters:
        filters = {"search":""}
    if not fields:
        fields = "id"

    if page and limit: 
        results = search_functions[resource_type](filters, fields, page=page, results=limit, sort=sort, reverse=reverse, count=count)
    else:
        results = unpaginated_search(
            search_function=search_functions[resource_type], 
            filters=filters, fields=fields, sort=sort, reverse=reverse, count=count
        )
    
    if (resource_type == 'vn' and response_size == 'large'):
        for vn in results['results']:
            vnid = vn['id']

            characters = unpaginated_search(
                search_function=search_characters_by_resource_id,
                resource_type='vn', resource_id=vnid, response_size='small', limit=100
            )['results']
            characters = [{key: char[key] for key in ['id', 'name', 'sex', 'vns']} for char in characters]
            vn['characters'] = characters if characters else []

            releases = unpaginated_search(
                search_function=search_releases_by_resource_id,
                resource_type='vn', resource_id=vnid, response_size='small', limit=100
            )['results']
            releases = [{key: release[key] for key in ['id', 'title']} for release in releases]
            vn['releases'] = releases if releases else []

    if (resource_type == 'character' and response_size == 'large'):
        for char in results['results']:
            charid = char['id']

            vns = api.get_vn(
                filters=get_remote_filters('vn', {'id': ','.join([ vn['id'] for vn in char['vns']])}),
                fields=['va.staff.id', 'va.staff.name', 'va.staff.original', 'va.character.id', 'va.note']
            )['results']

            seiyuu = list({
                (d['id'], d['name'], d['original'], d['note']): d 
                for d in [
                    {
                        'id': va['staff']['id'],
                        'name': va['staff']['name'],
                        'original': va['staff']['original'],
                        'note': va['note']
                    }
                    for vn in vns
                    for va in vn['va']
                    if va['character']['id'] == charid
            ]}.values())

            char['seiyuu'] = seiyuu if seiyuu else []

    return results


def search_resources_by_release_id(release_id: str, related_resource_type: str, response_size: str = "small") -> dict[str, Any]:
    url = "https://api.vndb.org/kana/release"

    related_resource_fields = get_remote_fields(related_resource_type, response_size)
    fields = {
        'vn': [f'vns.{field}' for field in related_resource_fields] + ['vns.rtype'],
        'producer': [f'producers.{field}' for field in related_resource_fields] + ['producers.developer', 'producers.publisher']
    }.get(related_resource_type)

    payload = {
        "filters": ["id", "=", release_id],
        "fields": ",".join(fields),
        "results": 100
    }

    with httpx.Client() as client:
        response = client.post(url, json=payload)
        response.raise_for_status()
        results = response.json()['results'][0]
        results = results.get(
            {
                'vn': 'vns',
                'producer': 'producers'
            }.get(related_resource_type)
        )

    return {'results': results}

def search_resources_by_charid(charid: str, related_resource_type: str, response_size: str = "small") -> dict[str, Any]:
    url = "https://api.vndb.org/kana/character"

    related_resource_fields = get_remote_fields(related_resource_type, response_size)
    fields = {
        'trait': [f'traits.{field}' for field in related_resource_fields].extend['traits.spoiler', 'traits.lie'],
        'vns': [f'vns.{field}' for field in related_resource_fields].extend['vns.spoiler', 'vns.role', 'vns.release.id']
    }

    payload = {
        "filters": ["id", "=", charid],
        "fields": ",".join(fields),
        "results": 100
    }

    with httpx.Client() as client: 
        response = client.post(url, json=payload)
        response.raise_for_status()
        results = response.json()['results'][0]
        results = results.get(
            {
                'trait': 'traits',
            }.get(related_resource_type)
        )

    return {'results': results}

def search_resources_by_vnid(vnid: str, related_resource_type: str, response_size: str = "small") -> dict[str, Any]:
    url = "https://api.vndb.org/kana/vn"

    related_resource_fields = get_remote_fields(related_resource_type, response_size)
    fields = {
        'vn': [f'relations.{field}' for field in related_resource_fields] + ['relations.relation', 'relations.relation_official'],
        'tag': [f'tags.{field}' for field in related_resource_fields] + ['tags.rating', 'tags.spoiler', 'tags.lie'],
        'producer': [f'developers.{field}' for field in related_resource_fields],
        'staff': [f'staff.{field}' for field in related_resource_fields] + ['staff.eid', 'staff.role'],
    }.get(related_resource_type)

    payload = {
        "filters": ["id", "=", vnid],
        "fields": ",".join(fields),
        "results": 100
    }

    with httpx.Client() as client:
        response = client.post(url, json=payload)
        response.raise_for_status()
        results = response.json()['results'][0]
        results = results.get(
            {
                'vn': 'relations',
                'tag': 'tags',
                'producer': 'developers',
                'staff': 'staff'
            }.get(related_resource_type)
        )

    return {'results': results}

def search_releases_by_resource_id(resource_type: str, resource_id: str, response_size: str = 'small',
                                   sort: str = 'id', reverse: bool = False, limit: int = 10, page: int = 1, count: bool = True) -> dict[str, Any]:
    url = "https://api.vndb.org/kana/release"

    filters = {
        'vn': ['vn', '=', ['id', '=', resource_id]],
        'producer': ['producer', '=', ['id', '=', resource_id]]
    }.get(resource_type)

    release_fields = get_remote_fields("release", response_size)
    sort = validate_sort(resource_type, sort)
    payload = {
        "filters": filters,
        "fields": ",".join(release_fields),
        "sort": sort,
        "reverse": reverse,
        "results": limit,
        "page": page,
        "count": count 
    }

    with httpx.Client() as client:
        response = client.post(url, json=payload)
        response.raise_for_status()
        results = response.json()

    return results

def search_characters_by_resource_id(resource_type: str, resource_id: str, response_size: str = 'small', 
                                      sort: str = 'id', reverse: bool = False, limit: int = 10, page: int = 1, count: bool = True) -> dict[str, Any]:
    url = "https://api.vndb.org/kana/character"

    filters = {
        'trait': ['trait', '=', [resource_id, 0, 0]], 
        'dtrait': ['dtrait', '=', [resource_id, 0, 0]],
        'vn': ['vn', '=', ['id', '=', resource_id]]
    }.get(resource_type)

    character_fields = get_remote_fields("character", response_size)
    sort = validate_sort(resource_type, sort)
    payload = {
        "filters": filters,
        "fields": ",".join(character_fields),
        "sort": sort,
        "reverse": reverse,
        "results": limit,
        "page": page,
        "count": count 
    }

    with httpx.Client() as client:
        response = client.post(url, json=payload)
        response.raise_for_status()
        results = response.json()

    return results

def search_vns_by_resource_id(resource_type: str, resource_id: str, response_size: str = 'small',
                              sort: str = 'id', reverse: bool = False, limit: int = 10, page: int = 1, count: bool = True) -> dict[str, Any]:
    url = "https://api.vndb.org/kana/vn"

    filters = {
        'tag': ['tag', '=', [resource_id, 0, 0]],
        'dtag': ['dtag', '=', [resource_id, 0, 0]],
        'staff': ['staff', '=', ['id', '=', resource_id]],
        'producer': ['developer', '=', ['id', '=', resource_id]],
        'character': ['character', '=', ['id', '=', resource_id]],
        'release': ['release', '=', ['id', '=', resource_id]]
    }.get(resource_type)

    vn_fields = get_remote_fields("vn", response_size)
    sort = validate_sort(resource_type, sort)

    payload = {
        "filters": filters,
        "fields": ",".join(vn_fields),
        "sort": sort,
        "reverse": reverse,
        "results": limit,
        "page": page,
        "count": count 
    }

    with httpx.Client() as client:
        response = client.post(url, json=payload)
        response.raise_for_status()
        results = response.json()

    if response_size == 'small':
        return results

    for vn in results['results']:
        vnid = vn['id']
        characters = unpaginated_search(
            search_function=search_characters_by_resource_id,
            resource_type='vn', resource_id=vnid, response_size='small'
        )
        vn['characters'] = characters['results'] 
    return results


@memoize(timeout=3600)
def search_cache(*args, **kwargs): return search(*args, **kwargs)

@memoize(timeout=3600)
def search_resources_by_vnid_cache(*args, **kwargs): return search_resources_by_vnid(*args, **kwargs)

@memoize(timeout=3600)
def search_resources_by_charid_cache(*args, **kwargs): return search_resources_by_charid(*args, **kwargs)

@memoize(timeout=3600)
def search_resources_by_release_id_cache(*args, **kwargs): return search_resources_by_release_id(*args, **kwargs)

def search_resources_by_vnid_paginated(vnid: str, related_resource_type: str, response_size: str = "small", 
                                       sort: str = 'id', reverse: bool = False, limit: int = 10, page: int = 1, count: bool = True) -> dict[str, Any]:
    return paginated_results(search_resources_by_vnid_cache(vnid, related_resource_type, response_size),
                             sort, reverse, limit, page, count)

def search_resources_by_charid_paginated(charid: str, related_resource_type: str, response_size: str = "small", 
                                         sort: str = 'id', reverse: bool = False, limit: int = 10, page: int = 1, count: bool = True) -> dict[str, Any]:
    return paginated_results(search_resources_by_charid_cache(charid, related_resource_type, response_size), 
                             sort, reverse, limit, page, count)

def search_resources_by_release_id_paginated(release_id: str, related_resource_type: str, response_size: str = "small",
                                             sort: str = 'id', reverse: bool = False, limit: int = 10, page: int = 1, count: bool = True) -> dict[str, Any]:
    return paginated_results(search_resources_by_release_id_cache(release_id, related_resource_type, response_size),
                             sort, reverse, limit, page, count)

@memoize(timeout=3600)
def search_vns_by_resource_id_cache(*args, **kwargs): return search_vns_by_resource_id(*args, **kwargs)

@memoize(timeout=3600)
def search_characters_by_resource_id_cache(*args, **kwargs): return search_characters_by_resource_id(*args, **kwargs)

@memoize(timeout=3600)
def search_releases_by_resource_id_cache(*args, **kwargs): return search_releases_by_resource_id(*args, **kwargs)
