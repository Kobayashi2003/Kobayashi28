import os
import subprocess
from datetime import datetime
from flask import current_app
from typing import List, Dict, Any, Union, Optional

from sqlalchemy.exc import SQLAlchemyError

from api import db
from . import models

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