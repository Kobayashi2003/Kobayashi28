from typing import List, Callable
from functools import wraps
from operator import itemgetter
from datetime import datetime, timezone

from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

from userserve import db
from .models import User, CATEGORY_MODEL, CategoryType

def save_db_operation(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            db.session.commit()
            return result
        except SQLAlchemyError:
            db.session.rollback()
            return None
    return wrapper

@save_db_operation
def get_user(user_id: int) -> User | None:
    return User.query.get(user_id)

@save_db_operation
def get_user_by_username(username: str) -> User | None:
    return User.query.filter_by(username=username).first()

@save_db_operation
def create_user(username: str, password: str) -> User | None:
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    return user

@save_db_operation
def create_admin(username: str, password: str, admin_password: str) -> User | None:
    if admin_password != current_app.config['ADMIN_PASSWORD']:
        return None
    user = User(username=username, is_admin=True)
    user.set_password(password)
    db.session.add(user)
    return user

@save_db_operation
def grant_admin_privileges(user_id: int, admin_password: str) -> User | None:
    if admin_password != current_app.config['ADMIN_PASSWORD']:
        return None
    user = get_user(user_id)
    if not user:
        return None
    user.is_admin = True
    return user

@save_db_operation
def revoke_admin_privileges(user_id: int, admin_password: str) -> User | None:
    if admin_password != current_app.config['ADMIN_PASSWORD']:
        return None
    user = get_user(user_id)
    if not user:
        return None
    user.is_admin = False
    return user

@save_db_operation
def update_user(user_id: int, username: str = None) -> User | None:
    user = get_user(user_id)
    if not user:
        return None
    if username:
        user.username = username
    return user

@save_db_operation
def change_password(user_id: int, old_password: str, new_password: str) -> User | None:
    user = get_user(user_id)
    if not user:
        return None
    if not user.check_password(old_password):
        return None
    user.set_password(new_password)
    return user

@save_db_operation
def delete_user(user_id: int) -> bool:
    user = get_user(user_id)
    if user:
        db.session.delete(user)
        return True
    return False

@save_db_operation
def get_category(user_id: int, category_id: int, category_type: str) -> CategoryType | None:
    category_class = CATEGORY_MODEL.get(category_type)
    if not category_class:
        return None
    return category_class.query.filter_by(id=category_id, user_id=user_id).first()

@save_db_operation
def create_category(user_id: int, category_type: str, category_name: str) -> CategoryType | None:
    category_class = CATEGORY_MODEL.get(category_type)
    if not category_class:
        return None
    category = category_class(user_id=user_id, category_name=category_name)
    db.session.add(category)
    return category

@save_db_operation
def update_category(user_id: int, category_id: int, category_type: str, category_name: str = None) -> CategoryType | None:
    category = get_category(user_id, category_id, category_type)
    if not category:
        return None
    if category_name:
        category.category_name = category_name
    return category

@save_db_operation
def delete_category(user_id: int, category_id: int, category_type: str) -> CategoryType | None:
    category = get_category(user_id, category_id, category_type)
    if category.category_name == 'Default':
        return None
    if category:
        db.session.delete(category)
        return category
    return None

@save_db_operation
def clear_category(user_id: int, category_id: int, category_type: str) -> CategoryType | None:
    category = get_category(user_id, category_id, category_type)
    if category:
        category.marks = []
        return category
    return None

@save_db_operation
def add_mark_to_category(user_id: int, category_id: int, category_type: str, mark_id: int) -> CategoryType | None:
    category = get_category(user_id, category_id, category_type)
    if category:
        new_mark = {"id": mark_id, "marked_at": datetime.now(timezone.utc).isoformat()}
        category.marks.append(new_mark)
        return category
    return None

@save_db_operation
def remove_mark_from_category(user_id: int, category_id: int, category_type: str, mark_id: int) -> CategoryType | None:
    category = get_category(user_id, category_id, category_type)
    if category:
        category.marks = [mark for mark in category.marks if mark['id'] != mark_id]
        return category
    return None

@save_db_operation
def get_marks_from_category(user_id: int, category_id: int, category_type: str) -> List[str] | None:
    category = get_category(user_id, category_id, category_type)
    if not category:
        return None
    
    # Sort marks by marked_at in descending order
    sorted_marks = sorted(category.marks, key=itemgetter('marked_at'), reverse=True)
    
    # Extract mark_ids as strings
    mark_ids = [str(mark['id']) for mark in sorted_marks]
    
    return mark_ids

@save_db_operation
def get_categories_for_user(user_id: int, category_type: str) -> List[CategoryType] | None:
    category_class = CATEGORY_MODEL.get(category_type)
    if not category_class:
        return None
    return category_class.query.filter_by(user_id=user_id).all()

@save_db_operation
def search_categories(user_id: int, category_type: str, query: str) -> List[CategoryType] | None:
    category_class = CATEGORY_MODEL.get(category_type)
    if not category_class:
        return None
    return category_class.query.filter(
        category_class.user_id == user_id,
        category_class.category_name.ilike(f"%{query}%")
    ).all()