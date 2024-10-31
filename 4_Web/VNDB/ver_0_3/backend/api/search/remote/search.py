import requests
from typing import Dict, List, Any, Union, Optional
from enum import Enum
from api.search.remote.fields import VNDBFields
from api.search.remote.filters import VNDBFilters, FilterOperator, FilterType

VNDB_API_URL = "https://api.vndb.org/kana"

class VNDBEndpoint(Enum):
    VN = "vn"
    CHARACTER = "character"
    PRODUCER = "producer"
    STAFF = "staff"
    TAG = "tag"
    TRAIT = "trait"

class VNDBAPIWrapper:
    def __init__(self, api_token: Optional[str] = None):
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        if api_token:
            self.session.headers.update({"Authorization": f"Token {api_token}"})

    def _build_filters(self, filters: Dict[str, Any], filter_set: Dict[str, Any]) -> List[Any]:
        vndb_filters = []
        for key, value in filters.items():
            if key in ["and", "or"]:
                vndb_filters.append([key] + [self._build_filters(v, filter_set) if isinstance(v, dict) else self._build_filter(k, v, filter_set) for k, v in value.items()])
            else:
                vndb_filters.append(self._build_filter(key, value, filter_set))
        return vndb_filters[0] if len(vndb_filters) == 1 else ["and"] + vndb_filters

    def _build_filter(self, key: str, value: Any, filter_set: Dict[str, Any]) -> List[Any]:
        if key not in filter_set:
            raise ValueError(f"Unknown filter: {key}")

        filter_def = filter_set[key]
        
        if isinstance(value, tuple):
            operator, value = value
        else:
            operator = FilterOperator.EQUAL

        if filter_def.filter_type == FilterType.ARRAY:
            if isinstance(value, list) and len(value) == 3:
                return [key, operator.value, value]
            else:
                return [key, operator.value, [value, 0, 0]]
        elif filter_def.filter_type == FilterType.NESTED:
            if isinstance(value, dict):
                nested_filters = self._build_filters(value, filter_set)
                return [key, operator.value, nested_filters]
            else:
                return [key, operator.value, value]
        else:
            return [key, operator.value, value]

    def query(self, endpoint: VNDBEndpoint, filters: Dict[str, Any], fields: List[str], sort: str = "id", reverse: bool = False, results: int = 10, page: int = 1, user: Optional[str] = None) -> Dict[str, Any]:
        url = f"{VNDB_API_URL}/{endpoint.value}"
        
        filter_set = getattr(VNDBFilters, endpoint.name)
        
        payload = {
            "filters": self._build_filters(filters, filter_set),
            "fields": ",".join(fields),
            "sort": sort,
            "reverse": reverse,
            "results": results,
            "page": page
        }
        
        if user:
            payload["user"] = user
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def get_vn(self, filters: Dict[str, Any], fields: List[str], **kwargs) -> Dict[str, Any]:
        return self.query(VNDBEndpoint.VN, filters, fields, **kwargs)

    def get_character(self, filters: Dict[str, Any], fields: List[str], **kwargs) ->   Dict[str, Any]:
        return self.query(VNDBEndpoint.CHARACTER, filters, fields, **kwargs)

    def get_producer(self, filters: Dict[str, Any], fields: List[str], **kwargs) -> Dict[str, Any]:
        return self.query(VNDBEndpoint.PRODUCER, filters, fields, **kwargs)

    def get_staff(self, filters: Dict[str, Any], fields: List[str], **kwargs) -> Dict[str, Any]:
        return self.query(VNDBEndpoint.STAFF, filters, fields, **kwargs)

    def get_tag(self, filters: Dict[str, Any], fields: List[str], **kwargs) -> Dict[str, Any]:
        return self.query(VNDBEndpoint.TAG, filters, fields, **kwargs)

    def get_trait(self, filters: Dict[str, Any], fields: List[str], **kwargs) -> Dict[str, Any]:
        return self.query(VNDBEndpoint.TRAIT, filters, fields, **kwargs)

    def get_user_list_labels(self, user: Optional[str] = None, fields: Optional[List[str]] = None) -> Dict[str, Any]:
        url = f"{VNDB_API_URL}/ulist_labels"
        params = {}
        if user:
            params['user'] = user
        if fields:
            params['fields'] = ','.join(fields)
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def update_user_list(self, vn_id: str, data: Dict[str, Any]) -> None:
        url = f"{VNDB_API_URL}/ulist/{vn_id}"
        response = self.session.patch(url, json=data)
        response.raise_for_status()

    def update_release_list(self, release_id: str, status: int) -> None:
        url = f"{VNDB_API_URL}/rlist/{release_id}"
        response = self.session.patch(url, json={"status": status})
        response.raise_for_status()

    def remove_from_user_list(self, vn_id: str) -> None:
        url = f"{VNDB_API_URL}/ulist/{vn_id}"
        response = self.session.delete(url)
        response.raise_for_status()

    def remove_from_release_list(self, release_id: str) -> None:
        url = f"{VNDB_API_URL}/rlist/{release_id}"
        response = self.session.delete(url)
        response.raise_for_status()

    def get_auth_info(self) -> Dict[str, Any]:
        url = f"{VNDB_API_URL}/authinfo"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()