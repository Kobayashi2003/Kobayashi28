from app import db
from app.models import User
from app.utils.db_utils import safe_commit
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash

def get_user_by_id(uid):
    """
    Get user information by ID.
    """
    return User.query.filter_by(id=uid, is_active=True).first()

def get_user_by_username(username):
    """
    Get user information by username.
    """
    return User.query.filter_by(username=username, is_active=True).first()

def get_all_users(page=1, limit=10, sort='id', reverse=False):
    """
    Get a list of all users with pagination.
    """
    if not hasattr(User, sort):
        raise ValueError(f"Invalid sort field: {sort}")
    
    query = User.query.filter_by(is_active=True)
    order = desc(getattr(User, sort)) if reverse else getattr(User, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def search_users(query, page=1, limit=10, sort='id', reverse=False):
    """
    Search for users based on username with pagination.
    """
    if not hasattr(User, sort):
        raise ValueError(f'Invalid sort field: {sort}')
    
    query = User.query.filter(
        User.username.ilike(f'%{query}%'),
        User.is_active == True
    )
    order = desc(getattr(User, sort)) if reverse else getattr(User, sort)
    query.order_by(order)

    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def create_user(username, email, password, bio=None):
    """
    Create a new user account.
    """
    new_user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
        bio=bio
    )
    db.session.add(new_user)
    safe_commit("Username or email already exists")
    return new_user

def update_user(uid, username=None, email=None, bio=None):
    """
    Update user information.
    """
    user = get_user_by_id(uid)
    if not user:
        raise ValueError("User not found")
    
    if username:
        user.username = username
    if email:
        user.email = email
    if bio is not None:
        user.bio = bio
    
    safe_commit("Username or email already exists")
    return user

def delete_user(uid):
    """
    Delete a user account.
    """
    user = get_user_by_id(uid)
    if not user:
        raise ValueError("User not found")
    
    user.delete()
    safe_commit("Failed to delete user")

def verify_user_password(user, password):
    """
    Verify user password.
    """
    return user and check_password_hash(user.password_hash, password)

def change_user_password(uid, old_password, new_password):
    """
    Change user password.
    """
    user = get_user_by_id(uid)
    if not user:
        raise ValueError("User not found")
    
    if not verify_user_password(user, old_password):
        raise ValueError("Incorrect old password")
    
    user.password_hash = generate_password_hash(new_password)
    safe_commit("Failed to change password")