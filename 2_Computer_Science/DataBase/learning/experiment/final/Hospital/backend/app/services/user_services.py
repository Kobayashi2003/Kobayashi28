from app import db
from app.models import User
from app.utils.db_utils import safe_commit
from flask import current_app
from sqlalchemy import desc

def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_all_users(page=1, per_page=10, sort='id', reverse=False):
    if not hasattr(User, sort):
        raise ValueError(f"Invalid sort field: {sort}")
    
    query = User.query
    order = desc(getattr(User, sort)) if reverse else getattr(User, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def create_user(username, phone_number, password, bio=None):
    new_user = User(username=username, phone_number=phone_number, bio=bio)
    new_user.set_password(password)
    db.session.add(new_user)
    success, message = safe_commit()
    if success:
        return True, new_user
    return False, message

def create_admin(username, phone_number, password, bio=None):
    new_admin = User(username=username, phone_number=phone_number, bio=bio, is_admin=True)
    new_admin.set_password(password)
    db.session.add(new_admin)
    success, message = safe_commit()
    if success:
        return True, new_admin
    return False, message

def update_user(user_id, username=None, phone_number=None, bio=None):
    user = User.query.get(user_id)
    if not user:
        return False, "User not found"

    if username:
        user.username = username
    if phone_number:
        user.phone_number = phone_number
    if bio is not None:
        user.bio = bio
    
    success, message = safe_commit()
    if success:
        return True, user
    return False, message

def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return False, "User not found"
    
    db.session.delete(user)
    db.session.flush()
    success, message = safe_commit()
    if success:
        return True, ''
    return False, message

def search_users(query, page=1, per_page=10, sort='id', reverse=False):
    if not hasattr(User, sort):
        raise ValueError(User, sort)

    search = f"%{query}%"
    query = User.query.filter(
        (User.username.ilike(search)) | (User.phone_number.ilike(search))
    )
    order = desc(getattr(User, sort)) if reverse else getattr(User, sort)
    query = query.order_by(order)

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def change_user_password(user_id, old_password, new_password):
    user = User.query.get(user_id)
    if not user:
        return False, "User not found"
    
    if not user.check_password(old_password):
        return False, "Incorrect old password"
    
    user.set_password(new_password)
    success, message = safe_commit()
    if success:
        return True, user
    return False, message

def is_admin(user_id):
    user = User.query.get(user_id)
    if not user:
        return False
    return user.is_admin

def grant_admin_privileges(user_id, admin_password):
    if admin_password != current_app.config['ADMIN_PASSWORD']:
        return False, "Invalid admin password"
    
    user = User.query.get(user_id)
    if not user:
        return False, "User not found"

    user.is_admin = True
    success, message = safe_commit()
    if success:
        return True, user
    return False, message

def revoke_admin_privileges(user_id, admin_password):
    if admin_password != current_app.config['ADMIN_PASSWORD']:
        return False, "Invalid admin password"
    
    user = User.query.get(user_id)
    if not user:
        return False, "User not found"

    user.is_admin = False
    success, message = safe_commit()
    if success:
        return True, user
    return False, message