import os
import subprocess
from datetime import datetime
from flask import current_app
from typing import List, Dict, Any, Union, Optional

from sqlalchemy import func
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
    'character_image': models.CharacterImage
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

def get_all(type: str) -> List[ModelType]:
    model = MODEL_MAP.get(type)
    if not model:
        raise ValueError(f"Invalid model type: {type}")

    return model.query.all()

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

def get_new_image_upload_id(type: str) -> str:
    """Get the next available image ID starting with 'u'."""
    if type not in ['vn', 'character']:
        raise ValueError(f"Invalid image type: {type}")

    image_model = models.VNImage if type == 'vn' else models.CharacterImage

    # Query the maximum ID that starts with 'u'
    max_id = db.session.query(func.max(image_model.id)).filter(image_model.id.like('u%')).scalar()

    if max_id:
        # Extract the numeric part and increment
        try:
            next_num = int(max_id[1:]) + 1
        except ValueError:
            # Handle the case where the ID doesn't follow the expected
            next_num = 1
    else:
        # Extract the numeric part and increment
        next_num = 1
    
    # Format the new ID
    new_id = f'u{next_num}'

    return new_id

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