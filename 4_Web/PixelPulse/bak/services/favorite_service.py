from app import db
from app.models import User, Image
from app.utils.db_utils import safe_commit
from sqlalchemy import desc

def favorite_image(user_id, image_id):
    """
    Make a user favorite an image.
    """
    user = User.query.get(user_id)
    image = Image.query.get(image_id)
    if not user or not image:
        raise ValueError("User or Image not found")
    
    if image not in user.favorited_images:
        user.favorited_images.append(image)
        safe_commit("Failed to favorite image")

def unfavorite_image(user_id, image_id):
    """
    Make a user unfavorite an image.
    """
    user = User.query.get(user_id)
    image = Image.query.get(image_id)
    if not user or not image:
        raise ValueError("User or Image not found")
    
    if image in user.favorited_images:
        user.favorited_images.remove(image)
        safe_commit("Failed to unfavorite image")

def get_favorited_images(user_id, page=1, limit=10, sort='created_at', reverse=True):
    """
    Get all images favorited by a specific user with pagination.
    """
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")
    
    if not hasattr(Image, sort):
        raise ValueError(f"Invalid sort field: {sort}")
    
    query = user.favorited_images.filter(Image.deleted_at == None)
    order = desc(getattr(Image, sort)) if reverse else getattr(Image, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def get_users_who_favorited(image_id, page=1, limit=10, sort='username', reverse=False):
    """
    Get all users who favorited a specific image with pagination.
    """
    image = Image.query.get(image_id)
    if not image:
        raise ValueError("Image not found")
    
    if not hasattr(User, sort):
        raise ValueError(f"Invalid sort field: {sort}")
    
    query = image.favorited_by.filter(User.deleted_at == None)
    order = desc(getattr(User, sort)) if reverse else getattr(User, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def is_image_favorited(user_id, image_id):
    """
    Check if a user has favorited a specific image.
    """
    user = User.query.get(user_id)
    image = Image.query.get(image_id)
    if not user or not image:
        raise ValueError("User or Image not found")
    return image in user.favorited_images

def get_favorite_count(image_id):
    """
    Get the number of favorites for a specific image.
    """
    image = Image.query.get(image_id)
    if not image:
        raise ValueError("Image not found")
    return image.favorited_by.count()
