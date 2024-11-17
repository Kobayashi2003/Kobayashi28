import os
import subprocess
from datetime import datetime
from flask import current_app
from typing import List, Dict, Any, Union, Optional

from sqlalchemy import func, cast, desc, Integer
from sqlalchemy.exc import SQLAlchemyError

from . import models
from api import db

ModelType = Union[models.VN, models.Tag, models.Producer, models.Staff, models.Character, models.Trait, models.LocalVN, models.LocalTag, models.LocalProducer, models.LocalStaff, models.LocalCharacter, models.LocalTrait]

MODEL_MAP = {
    'vn': models.VN,
    'tag': models.Tag,
    'producer': models.Producer,
    'staff': models.Staff,
    'character': models.Character,
    'trait': models.Trait,
    'local_vn': models.LocalVN,
    'local_tag': models.LocalTag,
    'local_producer': models.LocalProducer,
    'local_staff': models.LocalStaff,
    'local_character': models.LocalCharacter,
    'local_trait': models.LocalTrait,
    'vn_image': models.VNImage,
    'character_image': models.CharacterImage,
    'savedata': models.SaveData
}

def safe_commit():
    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        raise


def create(type: str, id: str, data: Dict[str, Any]) -> ModelType:
    model = MODEL_MAP.get(type)
    if not model:
        raise ValueError(f"Invalid model type: {type}")
    
    item = model(id=id, **data)
    db.session.add(item)
    safe_commit()
    return item

def update(type: str, id: str, data: Dict[str, Any]) -> Optional[ModelType]:
    model = MODEL_MAP.get(type)
    if not model:
        raise ValueError(f"Invalid model type: {type}")
    
    item = model.query.get(id)
    if item:
        for key, value in data.items():
            setattr(item, key, value)
        safe_commit()
    return item

def delete(type: str, id: str) -> bool:
    model = MODEL_MAP.get(type)
    if not model:
        raise ValueError(f"Invalid model type: {type}")
    
    item = model.query.get(id)
    if item:
        db.session.delete(item)
        safe_commit()
        return True
    return False

def exists(type: str, id: str) -> bool:
    model = MODEL_MAP.get(type)
    if not model:
        raise ValueError(f"Invalid model type: {type}")
    return model.query.filter_by(id=id).first() is not None

def get(type: str, id: str) -> Optional[ModelType]:
    model = MODEL_MAP.get(type)
    if not model: 
        raise ValueError(f"Invalid model type: {type}")
    
    return model.query.get(id)

def get_all(type: str, page: Optional[int] = None, limit: Optional[int] = None, sort: Optional[str] = None, order: str = 'asc') -> List[ModelType]:
    model = MODEL_MAP.get(type)
    if not model:
        raise ValueError(f"Invalid model type: {type}")

    query = model.query

   # Apply sorting if specified
    if sort:
        sort_column = getattr(model, sort, None)
        if sort_column is not None:
            query = query.order_by(desc(sort_column) if order.lower() == 'desc' else sort_column)

    # Apply pagination if both page and limit are specified
    if page is not None and limit is not None:
        page = max(1, page)  # Ensure page is at least 1
        limit = min(max(1, limit), 100)  # Ensure limit is between 1 and 100
        query = query.offset((page - 1) * limit).limit(limit)

    return query.all()


def cleanup(type: str) -> int:
    local_model = MODEL_MAP.get(f'local_{type}')
    if not local_model:
        raise ValueError(f"Invalid model type: {type}")
    model = MODEL_MAP.get(type)

    local_ids = db.session.query(local_model.id)
    deleted = db.session.query(model).filter(~model.id.in_(local_ids)).delete(synchronize_session=False)
    safe_commit()

    return deleted

def cleanup_all() -> Dict[str, int]:
    return { type: cleanup(type) for type in ['vn', 'tag', 'producer', 'staff', 'character', 'trait'] }


def next_image_id(type: str) -> str:
    """Get the next available image ID starting with 'u'."""
    if type not in ['vn', 'character']:
        raise ValueError(f"Invalid image type: {type}")

    image_model = models.VNImage if type == 'vn' else models.CharacterImage

    # Query the maximum ID that starts with 'u'
    try:
        max_num = db.session.query(
            func.max(
                cast(func.substr(image_model.id, 2), Integer)
            )
        ).filter(image_model.id.like('u%')).scalar()

        if max_num: return f'u{max_num + 1}'

    except SQLAlchemyError as exc:
        ...

    return 'u1'

def get_image(type: str, id: str) -> Dict[str, str]:
    if type not in ['vn', 'character']:
        raise ValueError(f"Invalid type for image retrieval: {type}")

    image_model = models.VNImage if type == 'vn' else models.CharacterImage
    
    image = image_model.query.get(id)
    if image:
        image_path = os.path.join(current_app.config[f'IMAGE_{type.upper()}_FOLDER'], f"{image.id}.jpg")
        return {
            "id": image.id,
            "type": image.image_type,
            "path": image_path if os.path.exists(image_path) else None,
            f"{type}_id": getattr(image, f"{type}_id")
        }
    return {}

def get_images(type: str, id: str) -> List[Dict[str, str]]:
    if type not in ['vn', 'character']:
        raise ValueError(f"Invalid type for image retrieval: {type}")

    image_model = models.VNImage if type == 'vn' else models.CharacterImage
    foreign_key = 'vn_id' if type == 'vn' else 'character_id'

    images = image_model.query.filter_by(**{foreign_key: id}).all()
    result = []
    for image in images:
        image_path = os.path.join(current_app.config[f'IMAGE_{type.upper()}_FOLDER'], f"{image.id}.jpg")
        result.append({
            "id": image.id,
            "type": image.image_type,
            "path": image_path if os.path.exists(image_path) else None,
            f"{type}_id": getattr(image, foreign_key)
        })
    return result

def delete_image(type: str, id: str) -> bool:
    if type not in ['vn', 'character']:
        raise ValueError(f"Invalid type for image deletion: {type}")

    image_model = models.VNImage if type == 'vn' else models.CharacterImage
    
    # Query for the image to delete
    image = image_model.query.get(id)
    
    if image:
        # Delete the image file
        image_path = os.path.join(current_app.config[f'IMAGE_{type.upper()}_FOLDER'], f"{image.id}.jpg")
        if os.path.exists(image_path):
            os.remove(image_path)
        
        # Delete the database entry
        db.session.delete(image)
        safe_commit()
        return True
    
    return False

def delete_images(type: str, id: str) -> int:
    if type not in ['vn', 'character']:
        raise ValueError(f"Invalid type for image deletion: {type}")

    image_model = models.VNImage if type == 'vn' else models.CharacterImage
    foreign_key = 'vn_id' if type == 'vn' else 'character_id'

    # Query for images to delete
    images_to_delete = image_model.query.filter_by(**{foreign_key: id}).all()

    # Delete image files
    for image in images_to_delete:
        image_path = os.path.join(current_app.config[f'IMAGE_{type.upper()}_FOLDER'], f"{image.id}.jpg")
        if os.path.exists(image_path):
            os.remove(image_path)

    # Delete database entries
    deleted_count = image_model.query.filter_by(**{foreign_key: id}).delete()
    safe_commit()

    return deleted_count

def get_image_path(resource_type: str, resource_id: str, image_id: str) -> Optional[str]:
    """
    Get the path of an image file if it exists and is associated with the given resource.
    
    :param resource_type: The type of resource ('vn' or 'character')
    :param resource_id: The ID of the resource (VN or character)
    :param image_id: The ID of the image
    :return: The path to the image file if it exists and is associated with the resource, None otherwise
    """
    if resource_type not in ['vn', 'character']:
        raise ValueError(f"Invalid resource type: {resource_type}")

    image_model = models.VNImage if resource_type == 'vn' else models.CharacterImage
    foreign_key = f"{resource_type}_id"

    # Check if the image exists in the database and is associated with the resource
    image = image_model.query.filter_by(id=image_id, **{foreign_key: resource_id}).first()
    
    if image:
        # Construct the path to the image file
        image_path = os.path.join(current_app.config[f'IMAGE_{resource_type.upper()}_FOLDER'], f"{image.id}.jpg")
        
        # Check if the file exists
        if os.path.exists(image_path):
            return image_path
    
    return None


def next_savedata_id() -> str:
    """Get the next available savedata ID starting with 's'."""
    try:
        max_num = db.session.query(
            func.max(
                cast(func.substr(models.SaveData.id, 2), Integer)
            )
        ).filter(models.SaveData.id.like('s%')).scalar()

        if max_num: return f's{max_num + 1}'

    except SQLAlchemyError:
        pass

    return 's1'

def get_savedata(id: str) -> Dict[str, str]:
    savedata = models.SaveData.query.get(id)
    if savedata:
        return {
            "id": savedata.id,
            "vnid": savedata.vnid,
            "time": savedata.time.isoformat(),
            "filename": savedata.filename
        }
    return {}

def get_savedatas(vnid: str) -> List[Dict[str, str]]:
    savedatas = models.SaveData.query.filter_by(vnid=vnid).all()
    result = []
    for savedata in savedatas:
        result.append({
            "id": savedata.id,
            "vnid": savedata.vnid,
            "time": savedata.time.isoformat(),
            "filename": savedata.filename
        })
    return result

def delete_savedata(id: str) -> bool:
    savedata = models.SaveData.query.get(id)
    
    if savedata:

        savedata_path = os.path.join(current_app.config['SAVEDATA_FOLDER'], f"{savedata.id}")
        if os.path.exists(savedata_path):
            os.remove(savedata_path)

        db.session.delete(savedata)
        safe_commit()
        return True
    
    return False

def delete_savedatas(vnid: str) -> int:

    savedatas_to_delete = models.SaveData.query.filter_by(vnid=vnid).all()

    for savedata in savedatas_to_delete:
        savedata_path = os.path.join(current_app.config['SAVEDATA_FOLDER'], f"{savedata.id}")
        if os.path.exists(savedata_path):
            os.remove(savedata_path)

    deleted_count = models.SaveData.query.filter_by(vnid=vnid).delete()
    safe_commit()

    return deleted_count

def get_savedata_path(vn_id: str, savedata_id: str) -> Optional[str]:
    """
    Get the path of a savedata file if it exists and is associated with the given VN.
    
    :param vn_id: The ID of the visual novel
    :param savedata_id: The ID of the savedata
    :return: The path to the savedata file if it exists and is associated with the VN, None otherwise
    """
    # Check if the savedata exists in the database and is associated with the VN
    savedata = models.SaveData.query.filter_by(id=savedata_id, vnid=vn_id).first()
    
    if savedata:
        # Construct the path to the savedata file
        savedata_path = os.path.join(current_app.config['SAVEDATA_FOLDER'], savedata.id)
        
        # Check if the file exists
        if os.path.exists(savedata_path):
            return savedata_path
    
    return None


def backup_database_pg_dump(filename=None):
    if filename is None:
        filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
    
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
        '-F', 'c',  # plain text format
        '-f', filename,
        db_name
    ]

    try:
        # Execute pg_dump command
        result = subprocess.run(command, env=env, check=True, capture_output=True, text=True)
        print(f"Database backup created: {filename}")
        return filename
    except subprocess.CalledProcessError as e:
        print(f"Error during database backup: {e}")
        print(f"Error output: {e.stderr}")
        raise
    finally:
        # Clear password from environment variable
        env.pop('PGPASSWORD', None)

def restore_database_pg_dump(filename):
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
    finally:
        # Clear password from environment variable
        env.pop('PGPASSWORD', None)