from typing import List, Dict, Any, Optional

from datetime import datetime, timezone

from sqlalchemy import text

from api import db
from .common import db_transaction
from .base import (
    _get, _get_all, _get_inactive, _get_all_inactive,
    _create, _delete, _delete_all, exists
)
from ..models import SaveData


def next_savedata_id() -> str:
    """
    Get the next available savedata ID starting with 's' without using a database session.

    Returns:
        str: The next available savedata ID.
    """
    # Use raw SQL query to get the maximum ID
    query = text("""
        SELECT COALESCE(MAX(CAST(SUBSTRING(id, 2) AS INTEGER)), 0)
        FROM savedata
        WHERE id LIKE 's%'
    """)

    with db.engine.connect() as connection:
        result = connection.execute(query)
        max_num = result.scalar()

    return f's{max_num + 1}'

@db_transaction
def create_savedata(vnid: str, data: Dict[str, Any]) -> Optional[SaveData]:
    vn = _get('vn', vnid)
    if not vn:
        return None
    
    savedata_id = next_savedata_id()
    savedata_data = {
        'id': savedata_id,
        'vnid': vnid,
        'time': data.get('time', datetime.now(timezone.utc)),
        'filename': data.get('filename', ''),
        **data
    }

    savedata = _create('savedata', savedata_id, savedata_data)
    if savedata is None:
        return None

    # Update the relationship
    vn.savedatas.append(savedata)

    return savedata

@db_transaction
def get_savedata(vnid: str, savedata_id: str) -> Optional[SaveData]:
    if not exists('vn', vnid):
        return None

    savedata = _get('savedata', savedata_id)
    
    if not savedata or savedata.vnid != vnid:
        return None
    
    return savedata

@db_transaction
def get_savedatas(vnid: str, page: Optional[int] = None, limit: Optional[int] = None) -> List[SaveData]:
    if not exists('vn', vnid):
        return []

    savedatas = _get_all(
        type='savedata',
        page=page,
        limit=limit,
        sort='time',
        order='desc'
    )
    
    filtered_savedatas = [sd for sd in savedatas if sd.vnid == vnid]
    
    return filtered_savedatas

@db_transaction
def delete_savedata(vnid: str, savedata_id: str) -> Optional[SaveData]:
    if not exists('vn', vnid):
        return None

    savedata = _get('savedata', savedata_id) or _get_inactive('savedata', savedata_id)
    
    if not savedata or savedata.vnid != vnid:
        return None
    
    return _delete('savedata', savedata_id)

@db_transaction
def delete_savedatas(vnid: str) -> int:
    if not exists('vn', vnid):
        return 0

    savedatas = _get_all('savedata') + _get_all_inactive('savedata')
    savedatas = [sd for sd in savedatas if sd.vnid == vnid]
    
    deleted_count = 0
    for savedata in savedatas:
        deleted_savedata = _delete('savedata', savedata.id)
        deleted_count += 1 if deleted_savedata else 0
    
    return deleted_count
