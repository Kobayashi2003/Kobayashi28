from app import db
from app.models import User
from app.utils.db_utils import safe_commit
from sqlalchemy import desc

def follow_user(follower_id, followed_id):
    """
    Make a user follow another user.
    """
    follower = User.query.get(follower_id)
    followed = User.query.get(followed_id)
    if not follower or not followed:
        raise ValueError("User not found")
    
    if follower == followed:
        raise ValueError("Users cannot follow themselves")
    
    if followed not in follower.following:
        follower.following.append(followed)
        safe_commit("Failed to follow user")

def unfollow_user(follower_id, followed_id):
    """
    Make a user unfollow another user.
    """
    follower = User.query.get(follower_id)
    followed = User.query.get(followed_id)
    if not follower or not followed:
        raise ValueError("User not found")
    
    if followed in follower.following:
        follower.following.remove(followed)
        safe_commit("Failed to unfollow user")

def get_user_followers(user_id, page=1, limit=10, sort='username', reverse=False):
    """
    Get a list of users following the specified user with pagination.
    """
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")
    
    if not hasattr(User, sort):
        raise ValueError(f"Invalid sort field: {sort}")
    
    query = user.followers.filter(User.deleted_at == None)
    order = desc(getattr(User, sort)) if reverse else getattr(User, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def get_user_following(user_id, page=1, limit=10, sort='username', reverse=False):
    """
    Get a list of users that the specified user is following with pagination.
    """
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")
    
    if not hasattr(User, sort):
        raise ValueError(f"Invalid sort field: {sort}")
    
    query = user.following.filter(User.deleted_at == None)
    order = desc(getattr(User, sort)) if reverse else getattr(User, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def is_following(follower_id, followed_id):
    """
    Check if a user is following another user.
    """
    follower = User.query.get(follower_id)
    followed = User.query.get(followed_id)
    if not follower or not followed:
        raise ValueError("User not found")
    
    return followed in follower.following

def get_follower_count(user_id):
    """
    Get the number of followers for a user.
    """
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")
    
    return user.followers.filter(User.deleted_at == None).count()

def get_following_count(user_id):
    """
    Get the number of users a user is following.
    """
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")
    
    return user.following.filter(User.deleted_at == None).count()
