from typing import List, Dict, Any, Optional

import os
import subprocess
import uuid
from datetime import datetime, timezone 
from functools import wraps

from flask import current_app

from sqlalchemy import desc, text
from sqlalchemy.orm import joinedload 
from sqlalchemy.exc import SQLAlchemyError

from api import db
from . import models

from .models import META_MODEL_MAP, MODEL_MAP, IMAGE_MODEL_MAP, MetaModelType, ModelType, ImageModelType

def db_transaction(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            with db.session.begin_nested():
                result = func(*args, **kwargs)
            if result is None:
                return None
            db.session.commit()
            return result
        except (SQLAlchemyError, ValueError) as e:
            db.session.rollback()
            print(f"Error in {func.__name__}: {str(e)}")
            return None
    return wrapper

def exists(type: str, id: str) -> bool:
    model = MODEL_MAP.get(type)
    meta_model = META_MODEL_MAP.get(type)
    if not model or not meta_model:
        raise ValueError(f"Invalid model type: {type}")
    metadata = meta_model.query.filter_by(id=id).first()
    return metadata is not None and metadata.is_active

def _create(type: str, id: str, data: Dict[str, Any]) -> Optional[ModelType]:
    model = MODEL_MAP.get(type)
    meta_model = META_MODEL_MAP.get(type)
    if not model or not meta_model: 
        raise ValueError(f"Invalid model type: {type}")
    data.pop('id', None)

    if exists(type, id):
        return None

    model.query.filter_by(id=id).delete()
    meta_model.query.filter_by(id=id).delete()

    item = model(id=id, **data)
    db.session.add(item)

    metadata_item = meta_model(id=id)
    setattr(item, f"{type}_metadata", metadata_item)

    return item

def _update(type: str, id: str, data: Dict[str, Any]) -> Optional[ModelType]:
    model = MODEL_MAP.get(type)
    meta_model = META_MODEL_MAP.get(type)
    if not model or not meta_model:
        raise ValueError(f"Invalid model type: {type}")

    item = model.query.get(id)
    if not item:
        return None

    for key, value in data.items():
        setattr(item, key, value)
            
    metadata_attr = f"{type}_metadata"
    metadata_item = getattr(item, metadata_attr, None)
    if metadata_item is None:
        metadata_item = meta_model(id=id)
        setattr(item, metadata_attr, metadata_item)
    metadata_item.last_modified_at = datetime.now(timezone.utc)
    metadata_item.is_active = True
    
    return item

def _delete(type: str, id: str) -> Optional[ModelType]:
    model = MODEL_MAP.get(type)
    meta_model = META_MODEL_MAP.get(type)
    if not model or not meta_model:
        raise ValueError(f"Invalid model type: {type}")

    item = model.query.get(id)
    if not item:
        return None 

    metadata_attr = f"{type}_metadata"
    metadata_item = getattr(item, metadata_attr, None)

    if metadata_item and metadata_item.is_active:
        metadata_item.is_active = False
    else:
        db.session.delete(item)

    return item

def _delete_all(type: str) -> int:
    model = MODEL_MAP.get(type)
    meta_model = META_MODEL_MAP.get(type)
    if not model or not meta_model:
        raise ValueError(f"Invalid model type: {type}")

    # Count the number of active items
    count = meta_model.query.filter_by(is_active=True).count()

    # Bulk update to set is_active to False for all metadata items
    meta_model.query.update({meta_model.is_active: False}, synchronize_session=False)
    # Delete all items that are not in the active metadata items
    model.query.filter(~model.id.in_(db.session.query(meta_model.id).filter_by(is_active=True))).delete(synchronize_session=False)

    return count

def _get(type: str, id: str) -> Optional[ModelType]:
    model = MODEL_MAP.get(type)
    meta_model = META_MODEL_MAP.get(type)
    if not model or not meta_model:
        raise ValueError(f"Invalid model type: {type}")

    metadata_attr = f"{type}_metadata"

    item = (
        db.session.query(model)
        .options(joinedload(getattr(model, metadata_attr)))
        .filter(model.id == id)
        .filter(getattr(meta_model, 'is_active') == True)
        .first()
    )

    if not item:
        return None

    metadata = getattr(item, metadata_attr)
    metadata.last_accessed_at = datetime.now(timezone.utc)
    metadata.view_count += 1

    return item 

def _get_all(type: str, page: Optional[int] = None, limit: Optional[int] = None, sort: Optional[str] = None, order: str = 'asc') -> List[ModelType]:
    model = MODEL_MAP.get(type)
    meta_model = META_MODEL_MAP.get(type)
    if not model or not meta_model:
        raise ValueError(f"Invalid model type: {type}")

    metadata_attr = f"{type}_metadata"

    query = (
        db.session.query(model)
        .join(getattr(model, metadata_attr))
        .filter(getattr(meta_model, 'is_active') == True)
    )

    # Apply sorting if specified
    if sort:
        sort_column = getattr(model, sort, None)
        if sort_column is not None:
            query = query.order_by(desc(sort_column) if order.lower() == 'desc' else sort_column)

    # Apply pagination if both page and limit are specified
    if page and limit:
        page = max(1, page)  # Ensure page is at least 1
        limit = min(max(1, limit), 100)  # Ensure limit is between 1 and 100
        query = query.offset((page - 1) * limit).limit(limit)

    # Eager load the metadata to avoid N+1 query problem
    query = query.options(joinedload(getattr(model, metadata_attr)))

    # Execute the query and get the results
    results = query.all()

    # Update last_accessed_at and view_count for all retrieved items
    if results:
        item_ids = [item.id for item in results]
        db.session.query(meta_model).filter(
            getattr(model, 'id').in_(item_ids)
        ).update({
            meta_model.last_accessed_at: datetime.now(timezone.utc),
            meta_model.view_count: meta_model.view_count + 1
        }, synchronize_session=False)

    return results

def _cleanup(type: str) -> int:
    model = MODEL_MAP.get(type)
    meta_model = META_MODEL_MAP.get(type)
    if not model or not meta_model:
        raise ValueError(f"Invalid model type: {type}")

    metadata_attr = f"{type}_metadata"

    # Subquery to get IDs of items with active metadata
    active_ids = db.session.query(model.id).join(
        getattr(model, metadata_attr)
    ).filter(
        getattr(meta_model, 'is_active') == True
    ).subquery()

    # Delete items that are not in the active_ids subquery
    deleted = db.session.query(model).filter(
        ~model.id.in_(active_ids)
    ).delete(synchronize_session=False)

    return deleted

def _cleanup_all() -> Dict[str, int]:
    return { type: cleanup(type) for type in MODEL_MAP.keys() }

def _get_inactive(type: str, id: str) -> Optional[ModelType]:
    model = MODEL_MAP.get(type)
    meta_model = META_MODEL_MAP.get(type)
    if not model or not meta_model:
        raise ValueError(f"Invalid model type: {type}")

    metadata_attr = f"{type}_metadata"

    item = (
        db.session.query(model)
        .options(joinedload(getattr(model, metadata_attr)))
        .filter(model.id == id)
        .filter(getattr(meta_model, 'is_active') == False)
        .first()
    )

    return item

def _get_all_inactive(type: str, page: Optional[int] = None, limit: Optional[int] = None, sort: Optional[str] = None, order: str = 'asc') -> List[ModelType]:
    model = MODEL_MAP.get(type)
    meta_model = META_MODEL_MAP.get(type)
    if not model or not meta_model:
        raise ValueError(f"Invalid model type: {type}")

    metadata_attr = f"{type}_metadata"

    query = (
        db.session.query(model)
        .join(getattr(model, metadata_attr))
        .filter(getattr(meta_model, 'is_active') == False)
    )

    # Apply sorting if specified
    if sort:
        sort_column = getattr(model, sort, None)
        if sort_column is not None:
            query = query.order_by(desc(sort_column) if order.lower() == 'desc' else sort_column)

    # Apply pagination if both page and limit are specified
    if page and limit:
        page = max(1, page)  # Ensure page is at least 1
        limit = min(max(1, limit), 100)  # Ensure limit is between 1 and 100
        query = query.offset((page - 1) * limit).limit(limit)

    # Eager load the metadata to avoid N+1 query problem
    query = query.options(joinedload(getattr(model, metadata_attr)))

    # Execute the query and get the results
    results = query.all()

    return results

@db_transaction
def create(*args, **kwargs) -> Optional[ModelType]: return _create(*args, **kwargs)

@db_transaction
def update(*args, **kwargs) -> Optional[ModelType]: return _update(*args, **kwargs)

@db_transaction
def delete(*args, **kwargs) -> Optional[ModelType]: return _delete(*args, **kwargs)

@db_transaction
def delete_all(*args, **kwargs) -> int: return _delete_all(*args, **kwargs)

@db_transaction
def get(*args, **kwargs) -> Optional[ModelType]: return _get(*args, **kwargs)

@db_transaction
def get_all(*args, **kwargs) -> List[ModelType]: return _get_all(*args, **kwargs)

@db_transaction
def cleanup(*args, **kwargs) -> int: return _cleanup(*args, **kwargs)

@db_transaction
def cleanup_all(*args, **kwargs) -> Dict[str, int]: return _cleanup_all(*args, **kwargs)

@db_transaction
def get_inactive(*args, **kwargs) -> Optional[ModelType]: return _get_inactive(*args, **kwargs)

@db_transaction
def get_all_inactive(*args, **kwargs) -> List[ModelType]: return _get_all_inactive(*args, **kwargs)


def next_image_id(resource_type: str) -> str:
    """
    Get the next available image ID starting with 'u' without using a database session.

    Args:
        resource_type (str): The type of resource ('vn' or 'character').

    Returns:
        str: The next available image ID.

    Raises:
        ValueError: If an invalid resource_type is provided.
    """
    table_name = IMAGE_MODEL_MAP.get(resource_type).__tablename__
    if not table_name:
        raise ValueError(f"Invalid image resource_type: {resource_type}")

    # Use raw SQL query to get the maximum ID
    query = text(f"""
        SELECT COALESCE(MAX(CAST(SUBSTRING(id, 2) AS INTEGER)), 0)
        FROM {table_name}
        WHERE id LIKE 'u%'
    """)

    with db.engine.connect() as connection:
        result = connection.execute(query)
        max_num = result.scalar()

    return f'u{max_num + 1}'

@db_transaction
def create_image(resource_type: str, resource_id: str, image_id: str, data: Dict[str, Any]) -> Optional[ImageModelType]:
    if resource_type not in ['vn', 'character']:
        raise ValueError(f"Invalid resource_type for image creation: {resource_type}")

    resource = _get(resource_type, resource_id)
    if not resource:
        return None
    
    image_type = f'{resource_type}_image'
    image_data = {
        'id': image_id,
        'image_type': data.get('image_type', 'unknown'),
        f'{resource_type}_id': resource_id
    }

    image = _create(type=image_type, id=image_id, data=image_data)
    if image is None:
        return None

    resource.images.append(image)
    return image

def create_upload_image(resource_type: str, resource_id: str, data: Dict[str, Any]) -> Optional[ImageModelType]:
    image_id = next_image_id(resource_type)
    return create_image(resource_type, resource_id, image_id, data)

@db_transaction
def get_image(resource_type: str, resource_id: str, image_id: str) -> Optional[ImageModelType]:
    if resource_type not in ['vn', 'character']:
        raise ValueError(f"Invalid resource_type for image retrieval: {resource_type}")
    
    if not exists(resource_type, resource_id):
        return None

    image = _get(f'{resource_type}_image', image_id)

    if not image or getattr(image, f'{resource_type}_id') != resource_id:
        return None
    
    return image

@db_transaction
def get_images(resource_type: str, resource_id: str, page: Optional[int] = None, limit: Optional[int] = None) -> List[ImageModelType]:
    if resource_type not in ['vn', 'character']:
        raise ValueError(f"Invalid resource_type for image retrieval: {resource_type}")
    
    resource = _get(resource_type, resource_id)
    if not resource:
        return []

    image_type = f'{resource_type}_image'
    
    # Use the existing get_all function with additional filtering
    images = _get_all(
        type=image_type,
        page=page,
        limit=limit,
        sort='id',  # You can change this if you want a different default sorting
        order='asc'
    )
    
    # Filter images to only those associated with the specific resource
    filtered_images = [img for img in images if getattr(img, f'{resource_type}_id') == resource_id]
    
    return filtered_images

@db_transaction
def delete_image(resource_type: str, resource_id: str, image_id: str) -> Optional[ImageModelType]:
    if resource_type not in ['vn', 'character']:
        raise ValueError(f"Invalid resource_type for image deletion: {resource_type}")
    
    if not exists(resource_type, resource_id):
        return None

    image_type = f'{resource_type}_image'
    image = _get(image_type, image_id) or _get_inactive(image_type, image_id)
    
    if not image or getattr(image, f'{resource_type}_id') != resource_id:
        return None
    
    return _delete(image_type, image_id)

@db_transaction
def delete_images(resource_type: str, resource_id: str) -> int:
    if resource_type not in ['vn', 'character']:
        raise ValueError(f"Invalid resource_type for image deletion: {resource_type}")
    
    if not exists(resource_type, resource_id):
        return 0

    image_type = f'{resource_type}_image'
    
    # Get all images associated with the resource
    images = _get_all(image_type) + _get_all_inactive(image_type)
    images = [img for img in images if getattr(img, f'{resource_type}_id') == resource_id]
    
    deleted_count = 0
    for image in images:
        deleted_image = _delete(image_type, image.id)
        deleted_count += 1 if deleted_image else 0
    
    return deleted_count


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
def create_savedata(vnid: str, data: Dict[str, Any]) -> Optional[models.SaveData]:
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
def get_savedata(vnid: str, savedata_id: str) -> Optional[models.SaveData]:
    if not exists('vn', vnid):
        return None

    savedata = _get('savedata', savedata_id)
    
    if not savedata or savedata.vnid != vnid:
        return None
    
    return savedata

@db_transaction
def get_savedatas(vnid: str, page: Optional[int] = None, limit: Optional[int] = None) -> List[models.SaveData]:
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
def delete_savedata(vnid: str, savedata_id: str) -> Optional[models.SaveData]:
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


def get_next_backup_id() -> str:
    return str(uuid.uuid4()) 

def backup_database_pg_dump() -> str:
    """Create a database backup and return the filename."""
    backup_folder = current_app.config['BACKUP_FOLDER']
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    backup_id = get_next_backup_id()
    backup_filename = f"{backup_id}.dump"
    backup_path = os.path.join(backup_folder, backup_filename)
    
    # Get database connection information from config
    db_name = current_app.config['DB_NAME']
    db_user = current_app.config['DB_USER']
    db_password = current_app.config['DB_PASSWORD']
    db_host = current_app.config['DB_HOST']
    db_port = current_app.config['DB_PORT']

    # Set environment variable to avoid exposing password in command line
    env = os.environ.copy()
    env['PGPASSWORD'] = db_password

    # Build pg_dump command
    command = [
        'pg_dump',
        '-h', db_host,
        '-p', db_port,
        '-U', db_user,
        '-F', 'c',  # custom format
        '-f', backup_path,
        db_name
    ]

    try:
        # Execute pg_dump command
        result = subprocess.run(command, env=env, check=True, capture_output=True, text=True)
        print(f"Database backup created: {backup_filename}")
        return backup_id 
    except subprocess.CalledProcessError as e:
        print(f"Error during database backup: {e}")
        print(f"Error output: {e.stderr}")
        if os.path.exists(backup_path):
            os.remove(backup_path)
        raise
    finally:
        # Clear password from environment variable
        env.pop('PGPASSWORD', None)

def restore_database_pg_dump(filename) -> bool:

    # Check if the backup file exists
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Backup file not found: {filename}")

    # Get database connection information from config
    db_name = current_app.config['DB_NAME']
    db_user = current_app.config['DB_USER']
    db_password = current_app.config['DB_PASSWORD']
    db_host = current_app.config['DB_HOST']
    db_port = current_app.config['DB_PORT']

    # Set environment variable to avoid exposing password in command line
    env = os.environ.copy()
    env['PGPASSWORD'] = db_password

    # Build psql command for restoration
    command = [
        'pg_restore',
        '-h', db_host,
        '-p', db_port,
        '-U', db_user,
        '-d', db_name,
        '--clean',  # drop existing objects before restoring
        '--if-exists',  # skip objects that don't exist
        '--no-owner', # skip restoration of object ownership
        '--no-privileges',  # skip restoration of access privileges
        filename 
    ]

    try:
        # Execute psql command to restore the database
        result = subprocess.run(command, env=env, check=True, capture_output=True, text=True)
        print(f"Database restored from: {filename}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during database restore: {e}")
        print(f"Error output: {e.stderr}")
        raise
    except Exception as e:
        print(f"Unexpected error during database restore: {str(e)}")
        raise
    finally:
        # Clear password from environment variable
        env.pop('PGPASSWORD', None)

@db_transaction
def create_backup() -> Optional[str]:
    try:
        # Perform the actual backup
        backup_id = backup_database_pg_dump()

        # Create a new backup entry in the database
        backup_data = {
            'time': datetime.now(timezone.utc),
        }
        
        new_backup = _create('backup', backup_id, backup_data)
        if new_backup is None:
            raise ValueError("Failed to create backup entry in database")

        return backup_id

    except Exception as e:
        print(f"Error during backup creation: {str(e)}")
        # If the backup file was created but database entry failed, remove the file
        backup_folder = current_app.config['BACKUP_FOLDER']
        backup_path = os.path.join(backup_folder, f'{backup_id}.dump')
        if os.path.exists(backup_path):
            os.remove(backup_path)
        raise

@db_transaction
def get_backup(backup_id: str) -> Optional[Dict[str, Any]]:
    backup = _get('backup', backup_id)
    if backup is None:
        print(f"No backup found with ID: {backup_id}")
        return None
    
    return {
        'id': backup.id,
        'time': backup.time.isoformat(),
    }

@db_transaction
def get_backups(page: Optional[int] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    backups = _get_all('backup', page=page, limit=limit, sort='time', order='desc')
    return [
        {
            'id': backup.id,
            'time': backup.time.isoformat(),
        }
        for backup in backups
    ]

@db_transaction
def delete_backup(backup_id: str) -> Optional[ModelType]:
    deleted_backup = _delete('backup', backup_id)
    if deleted_backup is None:
        print(f"No backup found with ID: {backup_id}")
        return None

    print(f"Backup with ID {backup_id} successfully deleted")
    return deleted_backup

@db_transaction
def delete_backups() -> int:
    backups = _get_all('backup') + _get_all_inactive('backup')
    
    deleted_count = 0
    for backup in backups:
        deleted_backup = _delete('backup', backup.id)
        deleted_count += 1 if deleted_backup else 0

    return deleted_count
