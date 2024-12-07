from app import db
from app.models import User, Collection
from app.utils.db_utils import safe_commit
from sqlalchemy import desc

# Basic CRUD operations
# --------------------------------------------------

def create_user(username, email, password, bio=None):
    """Create a new user with a default collection."""
    new_user = User(username=username, email=email, bio=bio)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.flush()
    
    Collection.create_default_collection(new_user)
    
    safe_commit("Failed to create user")
    return new_user

def get_user(user_id):
    """Retrieve a user by their ID."""
    return User.query.get(user_id)

def get_all_users(page=1, per_page=20, sort_by='created_at', order='desc'):
    """Get all users with pagination and sorting options."""
    query = User.query

    if sort_by == 'username':
        query = query.order_by(desc(User.username) if order == 'desc' else User.username)
    else:
        query = query.order_by(desc(User.created_at) if order == 'desc' else User.created_at)

    return query.paginate(page=page, per_page=per_page, error_out=False)

def update_user(user_id, username=None, email=None, bio=None, password=None):
    """Update a user's information."""
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")
    
    if username:
        user.username = username
    if email:
        user.email = email
    if bio is not None:
        user.bio = bio
    if password:
        user.set_password(password)
    
    safe_commit("Failed to update user")
    return user

def delete_user(user_id):
    """Delete a user by their ID."""
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")
    
    db.session.delete(user)
    safe_commit("Failed to delete user")

def authenticate_user(username, password):
    """Authenticate a user."""
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None

# Advanced operations
# --------------------------------------------------

def get_user_stats(user_id):
    """Get statistics for a user."""
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")
    
    return {
        'image_count': user.published_images.count(),
        'liked_image_count': user.liked_images.count(),
        'follower_count': user.followers.count(),
        'following_count': user.following.count(),
        'created_at': user.created_at
    }

def get_user_followers(user_id, page=1, per_page=20):
    """Get followers of a user with pagination."""
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")
    
    return user.followers.paginate(page=page, per_page=per_page, error_out=False)

def get_user_following(user_id, page=1, per_page=20):
    """Get users that a user is following with pagination."""
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")
    
    return user.following.paginate(page=page, per_page=per_page, error_out=False)