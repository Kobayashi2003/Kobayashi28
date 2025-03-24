from typing import List, Dict, Callable
from functools import wraps
from operator import itemgetter
from datetime import datetime, timezone

from flask import current_app

from userserve import db
from .models import User, CATEGORY_MODEL, CategoryType

def save_db_operation(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            db.session.rollback()
            print(f"Error in {func.__name__}: {str(e)}")
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
    db.session.flush()
    db.session.commit()
    return user

@save_db_operation
def create_admin(username: str, password: str, admin_password: str) -> User | None:
    if admin_password != current_app.config['ADMIN_PASSWORD']:
        return None
    user = User(username=username, is_admin=True)
    user.set_password(password)
    db.session.add(user)
    db.session.flush()
    db.session.commit()
    return user

@save_db_operation
def grant_admin_privileges(user_id: int, admin_password: str) -> User | None:
    if admin_password != current_app.config['ADMIN_PASSWORD']:
        return None
    user = get_user(user_id)
    if not user:
        return None
    user.is_admin = True
    db.session.flush()
    db.session.commit()
    return user

@save_db_operation
def revoke_admin_privileges(user_id: int, admin_password: str) -> User | None:
    if admin_password != current_app.config['ADMIN_PASSWORD']:
        return None
    user = get_user(user_id)
    if not user:
        return None
    user.is_admin = False
    db.session.flush()
    db.session.commit()
    return user

@save_db_operation
def update_user(user_id: int, username: str = None) -> User | None:
    user = get_user(user_id)
    if not user:
        return None
    if username:
        user.username = username
    db.session.flush()
    db.session.commit()
    return user

@save_db_operation
def change_password(user_id: int, old_password: str, new_password: str) -> User | None:
    user = get_user(user_id)
    if not user:
        return None
    if not user.check_password(old_password):
        return None
    user.set_password(new_password)
    db.session.flush()
    db.session.commit()
    return user

@save_db_operation
def delete_user(user_id: int) -> bool:
    user = get_user(user_id)
    if not user:
        return False
    db.session.delete(user)
    db.session.flush()
    db.session.commit()
    return True


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
    db.session.flush()
    db.session.commit()
    return category

@save_db_operation
def update_category(user_id: int, category_id: int, category_type: str, category_name: str = None) -> CategoryType | None:
    category = get_category(user_id, category_id, category_type)
    if not category:
        return None
    if category_name:
        category.category_name = category_name
    db.session.flush()
    db.session.commit()
    return category

@save_db_operation
def delete_category(user_id: int, category_id: int, category_type: str) -> CategoryType | None:
    category = get_category(user_id, category_id, category_type)
    if not category:
        return None
    if category.category_name == 'Default':
        return None
    db.session.delete(category)
    db.session.flush()
    db.session.commit()
    return category

@save_db_operation
def clear_category(user_id: int, category_id: int, category_type: str) -> CategoryType | None:
    category = get_category(user_id, category_id, category_type)
    if not category:
        return None
    category.marks = []
    db.session.flush()
    db.session.commit()
    return category

@save_db_operation
def contains_mark(user_id: int, category_type: str, category_id: int, mark_id: int) -> bool:
    category = get_category(user_id, category_id, category_type)
    if category:
        return any(mark['id'] == mark_id for mark in category.marks)
    return False

@save_db_operation
def add_mark_to_category(user_id: int, category_id: int, category_type: str, mark_id: int) -> CategoryType | None:
    category = get_category(user_id, category_id, category_type)
    if not category:
        return None
    new_mark = {"id": mark_id, "marked_at": datetime.now(timezone.utc).isoformat()}
    category.marks.append(new_mark)
    db.session.flush()
    db.session.commit()
    return category

@save_db_operation
def remove_mark_from_category(user_id: int, category_id: int, category_type: str, mark_id: int) -> CategoryType | None:
    category = get_category(user_id, category_id, category_type)
    if not category:
        return None
    category.marks = [mark for mark in category.marks if mark['id'] != mark_id]
    db.session.flush()
    db.session.commit()
    return category

@save_db_operation
def get_marks_from_category(user_id: int, category_id: int, category_type: str,
                            page: int = 1, limit: int = 100, sort: str = 'id', 
                            reverse: bool = False, count: bool = True) -> List[Dict] | None:
    category = get_category(user_id, category_id, category_type)
    if not category:
        return None
    
    # Sort marks by the specified field
    sorted_marks = sorted(category.marks, key=itemgetter(sort), reverse=reverse)
    
    # Calculate pagination
    total = len(sorted_marks)
    start = (page - 1) * limit
    end = start + limit
    
    # Paginate the marks
    paginated_marks = sorted_marks[start:end]
    
    # Extract required fields
    results = [{"id": str(mark['id']), "marked_at": mark['marked_at']} for mark in paginated_marks]
    
    # Check if there are more results
    more = end < total
    
    return {'results': results, 'more': more, 'count': total} if count else {'results': results, 'more': more}

@save_db_operation
def get_marks_from_category_without_pagination(user_id: int, category_id: int, category_type: str) -> List[Dict] | None:
    category = get_category(user_id, category_id, category_type)
    if not category:
        return None
    # return category.marks
    return {'results': category.marks, 'more': False, 'count': len(category.marks)}

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


@save_db_operation
def is_marked(user_id: int, category_type: str, mark_id: int) -> bool:
    category_class = CATEGORY_MODEL.get(category_type)
    if not category_class:
        return False
    categories = category_class.query.filter_by(user_id=user_id).all()
    for category in categories:
        if any(mark['id'] == mark_id for mark in category.marks):
            return True
    return False

@save_db_operation
def get_categories_by_mark(user_id: int, category_type: str, mark_id: int) -> List[int] | None:
    category_class = CATEGORY_MODEL.get(category_type)
    if not category_class:
        return None
    
    categories = category_class.query.filter_by(user_id=user_id).all()

    marked_categories = []

    for category in categories:
        if any(mark['id'] == mark_id for mark in category.marks):
            marked_categories.append(category.id)

    return marked_categories
