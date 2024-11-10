import requests
from typing import Dict, List, Any, Union, Optional
from enum import Enum

from api.utils.logger import search_logger
from api.search.remote.fields import VNDBFields
from api.search.remote.filters import VNDBFilters, FilterOperator, FilterType
from api.search.remote.common import get_remote_fields

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
        """
        Recursively build VNDB filters from a dictionary of filter conditions.

        Args:
            filters (Dict[str, Any]): The filter conditions to process.
            filter_set (Dict[str, Any]): The set of valid filters for the current domain.

        Returns:
            List[Any]: A list representing the VNDB filter structure.
        """
        result = []
        for key, value in filters.items():
            if key in ["and", "or"]:
                # Handle logical operators by recursively processing their contents
                result.append([key] + [self._build_filters(item, filter_set) for item in value])
            else:
                # Process individual filter conditions
                result.append(self._build_filter(key, value, filter_set))
        
        # If there's only one filter, return it directly; otherwise, wrap in an "and" operation
        return result[0] if len(result) == 1 else ["and"] + result

    def _build_filter(self, key: str, value: Any, filter_set: Dict[str, Any]) -> List[Any]:
        """
        Build a single VNDB filter condition.

        Args:
            key (str): The filter key.
            value (Any): The filter value or nested filter structure.
            filter_set (Dict[str, Any]): The set of valid filters for the current domain.

        Returns:
            List[Any]: A list representing a single VNDB filter condition.

        Raises:
            ValueError: If the filter key is unknown.
        """
        if key not in filter_set:
            raise ValueError(f"Unknown filter: {key}")

        filter_def = filter_set[key]
        
        # Handle nested filters with associated domains
        if isinstance(value, dict) and filter_def.filter_type == FilterType.NESTED:
            if filter_def.associated_domain:
                # Use the associated domain's filter set for nested filters
                associated_filter_set = getattr(VNDBFilters, filter_def.associated_domain)
                nested_filters = self._build_filters(value, associated_filter_set)
            else:
                # Use the current filter set if no associated domain is specified
                nested_filters = self._build_filters(value, filter_set)
            return [key, "=", nested_filters]
        
        # Extract operator and value from tuple, or use default equality operator
        if isinstance(value, tuple):
            operator, filter_value = value
        else:
            operator, filter_value = FilterOperator.EQUAL, value

        # Special handling for array type filters
        if filter_def.filter_type == FilterType.ARRAY and not isinstance(filter_value, list):
            filter_value = [filter_value, 0, 0]

        return [key, operator.value, filter_value]

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

api = VNDBAPIWrapper()

def paginated_search(search_function, filters: Dict[str, Any], fields: List[str]) -> Dict[str, Any]:
    all_results = []
    page = 1
    while True:
        try:
            response = search_function(filters, fields, page=page)
            all_results.extend(response['results'])

            if not response.get('more', False):
                break

            page += 1
        except Exception as e:
            search_logger.error(f"Error fetching data from VNDB: {e}", exc_info=True)
            break

    return {"results": all_results, "count": len(all_results)}

def search_vn(filters: Dict[str, Any], fields: List[str], page: int = 1) -> Dict[str, Any]:
    return api.get_vn(filters, fields, page=page)

def search_character(filters: Dict[str, Any], fields: List[str], page: int = 1) -> Dict[str, Any]:
    return api.get_character(filters, fields, page=page)

def search_tag(filters: Dict[str, Any], fields: List[str], page: int = 1) -> Dict[str, Any]:
    return api.get_tag(filters, fields, page=page)

def search_producer(filters: Dict[str, Any], fields: List[str], page: int = 1) -> Dict[str, Any]:
    return api.get_producer(filters, fields, page=page)

def search_staff(filters: Dict[str, Any], fields: List[str], page: int = 1) -> Dict[str, Any]:
    return api.get_staff(filters, fields, page=page)

def search_trait(filters: Dict[str, Any], fields: List[str], page: int = 1) -> Dict[str, Any]:
    return api.get_trait(filters, fields, page=page)

def search(search_type: str, filters: Dict[str, Any], response_size: str = 'small') -> Dict[str, Any]:
    search_functions = {
        'vn': search_vn,
        'character': search_character,
        'tag': search_tag,
        'producer': search_producer,
        'staff': search_staff,
        'trait': search_trait
    }

    if search_type not in search_functions:
        raise ValueError(f"Invalid search type: {search_type}")

    fields = get_remote_fields(search_type, response_size)

    return paginated_search(search_functions[search_type], filters, fields)