import requests
from typing import Dict, Optional
from api.search.local import search_local
from api.search.utils import generate_local_filters
from api.utils.logger import search_logger
from api.utils.logger import test_logger

def search_vndb(
    filters:    list,
    fields:     str,
    results:    int=100,
    sort_field: str="",
    reverse:    bool=False
) -> Optional[Dict]:

    url = "https://api.vndb.org/kana/vn"
    headers = {
        "Content-Type": "application/json"
    }

    valid_sort_fields = {'id', 'title', 'released'}
    sort_field = sort_field if sort_field in valid_sort_fields else 'title'

    data = {
        "filters":  filters,
        "fields":   fields,
        "results":  results,
        "sort":     sort_field,
        "reverse":  reverse,
        "page":     1
    }

    all_results = []

    search_logger.info(f"Sending request to VNDB API.")

    while True:
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            response_json = response.json()
            all_results.extend(response_json['results'])

            if not response_json.get('more', False): break

            data['page'] += 1
        except requests.RequestException as e:
            search_logger.error(f"Error fetching data from VNDB: {e}", exc_info=True)
            search_logger.error(f"Response from VNDB: {response.text}")
            break

    if not all_results: return None

    for result in all_results:
        try:
            local_result = search_local(generate_local_filters(id=result['id']), fields=fields)
            if local_result:
                result.update(local_result[0])
            else:
                result['download'] = False
                result['date'] = ''
        except Exception as e:
            search_logger.error(f"Error processing local data for ID {result['id']}: {e}", exc_info=True)

    search_logger.info(f"Search completed. Total results: {len(all_results)}")
    return {
        "results": all_results,
        "count": len(all_results)
    }