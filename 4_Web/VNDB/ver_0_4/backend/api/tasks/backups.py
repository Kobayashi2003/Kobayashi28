from typing import Dict, Any 

from api.database import (
    restore_database_pg_dump,
    create_backup, get_backup, get_backups,
    delete_backup, delete_backups,
)
from api.utils import (
    get_backup_path
)
from .common import (
    task_with_memoize, task_with_cache_clear,
    format_results, daily_task
)

@daily_task(hour=0, minute=0)
@task_with_memoize(timeout=600)
def backup_task() -> Dict[str, Any]:
    backup_id = create_backup()
    return format_results(backup_id)

@task_with_cache_clear
def restore_task(backup_id: str) -> Dict[str, Any]:
    backup_path = get_backup_path(backup_id)
    result = restore_database_pg_dump(backup_path)
    return format_results(result)

@task_with_cache_clear
def get_backup_task(backup_id: str) -> Dict[str, Any]:
    backup = get_backup(backup_id)
    return format_results(backup)

@task_with_cache_clear
def get_backups_task() -> Dict[str, Any]:
    backups = get_backups()
    return format_results(backups)

@task_with_cache_clear
def delete_backup_task(backup_id: str) -> Dict[str, Any]:
    result = delete_backup(backup_id)
    return format_results(result)

@task_with_cache_clear
def delete_backups_task() -> Dict[str, Any]:
    deleted_count = delete_backups()
    return format_results(deleted_count)