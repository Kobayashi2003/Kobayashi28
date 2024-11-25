from typing import Dict, Any 

from api import celery, scheduled_task
from api.database import (
    create_backup, delete_backup, delete_backups,
    get_backup, get_backups, restore_database_pg_dump,
    convert_model_to_dict
)
from api.utils import get_backup_path
from .common import error_handler

@error_handler
def _backup_task() -> Dict[str, Any]:
    backup_id = create_backup()
    return {
        "status": "SUCCESS" if backup_id else "ERROR",
        "result": backup_id
    }

@error_handler
def _restore_task(backup_id: str) -> Dict[str, Any]:
    backup_path = get_backup_path(backup_id)
    return {
        "status": "SUCCESS" if backup_path else "NOT_FOUND",
        "result": restore_database_pg_dump(backup_path) if backup_path else False 
    }

@error_handler
def _delete_backup_task(backup_id: str) -> Dict[str, Any]:
    result = delete_backup(backup_id)
    return {
        "status": "SUCCESS" if result else "NOT_FOUND",
        "result": convert_model_to_dict(result) if result else None
    }

@error_handler
def _delete_backups_task() -> Dict[str, Any]:
    deleted_count = delete_backups()
    return {
        "status": "SUCCESS" if deleted_count else "NOT_FOUND",
        "result": deleted_count
    }

@error_handler
def _get_backup_task(backup_id: str) -> Dict[str, Any]:
    backup = get_backup(backup_id)
    return {
        "status": "SUCCESS" if backup else "NOT_FOUND",
        "result": convert_model_to_dict(backup) if backup else None
    }

@error_handler
def _get_backups_task() -> Dict[str, Any]:
    backups = get_backups()
    return {
        "status": "SUCCESS" if backups else "NOT_FOUND",
        "result": [convert_model_to_dict(backup) for backup in backups] if backups else []
    }

# ----------------------------------------
# Register celery tasks and schedule tasks
# ----------------------------------------

@celery.task
def backup_task(*args, **kwargs) -> Dict[str, Any]:
    return _backup_task(*args, **kwargs)

@celery.task
def restore_task(*args, **kwargs) -> Dict[str, Any]:
    return _restore_task(*args, **kwargs)

@celery.task
def delete_backup_task(*args, **kwargs) -> Dict[str, Any]:
    return _delete_backup_task(*args, **kwargs)

@celery.task
def delete_backups_task(*args, **kwargs) -> Dict[str, Any]:
    return _delete_backups_task(*args, **kwargs)

@celery.task
def get_backup_task(*args, **kwargs) -> Dict[str, Any]:
    return _get_backup_task(*args, **kwargs)

@celery.task
def get_backups_task(*args, **kwargs) -> Dict[str, Any]:
    return _get_backups_task(*args, **kwargs)

@scheduled_task(trigger='cron', id='weekly_backup_task', day_of_week='sun', hour=0, minute=0)
def scheduled_backup_task() -> Dict[str, Any]: _backup_task()