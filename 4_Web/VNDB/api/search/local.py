from typing import Dict, Any, List, Optional, Tuple
from api.db.operations import search as db_search
from api.utils.logger import search_logger

def search_local(filters: List[Tuple[str, Any]], fields: str, sort_field: Optional[str] = None, reverse: bool = False, limit: int = 1000, offset: int = 0) -> List[Dict[str, Any]]:
    try:
        search_logger.info(f"Searching local database.")
        results = db_search(filters=filters, fields=fields, sort_field=sort_field, reverse=reverse, limit=limit, offset=offset)
        search_logger.info(f"Local search completed. Found {len(results)} results.")
        
        return results
    except Exception as e:
        search_logger.error(f"Error in local search: {str(e)}")
