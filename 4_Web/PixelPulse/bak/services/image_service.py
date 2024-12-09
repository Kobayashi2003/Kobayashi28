from app import db
from app.models import Image, User, Tag
from app.utils.db_utils import safe_commit
from sqlalchemy import func, desc

def create_image(title, description, user_id):
    """
    Create a new image.
    """
    new_image = Image(title=title, description=description, uid=user_id)
    db.session.add(new_image)
    safe_commit("Failed to create image")
    return new_image

def get_image_by_id(image_id):
    """
    Get image information by ID.
    """
    return Image.query.get(image_id)

def update_image(image_id, title=None, description=None):
    """
    Update image information.
    """
    image = get_image_by_id(image_id)
    if not image:
        raise ValueError("Image not found")
    
    if title:
        image.title = title
    if description is not None:  # Allow setting an empty string
        image.description = description
    
    safe_commit("Failed to update image")
    return image

def delete_image(image_id):
    """
    Delete an image.
    """
    image = get_image_by_id(image_id)
    if not image:
        raise ValueError("Image not found")
    
    image.delete()
    safe_commit("Failed to delete image")

def get_all_images(page=1, limit=10, sort='id', reverse=False):
    """
    Get a list of all images with pagination.
    """
    if not hasattr(Image, sort):
        raise ValueError(f"Invalid sort field: {sort}")
    
    query = Image.query.filter_by(deleted_at=None)
    order = desc(getattr(Image, sort)) if reverse else getattr(Image, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def get_images_by_user(user_id, page=1, limit=10, sort='id', reverse=False):
    """
    Get all images uploaded by a specific user with pagination.
    """
    if not hasattr(Image, sort):
        raise ValueError(f"Invalid sort field: {sort}")
    
    query = Image.query.filter_by(uid=user_id, deleted_at=None)
    order = desc(getattr(Image, sort)) if reverse else getattr(Image, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def get_popular_images(limit=10):
    """
    Get the most popular images based on likes.
    """
    return db.session.query(Image, func.count(User.id).label('like_count'))\
        .join(Image.liked_by)\
        .filter(Image.deleted_at == None)\
        .group_by(Image.id)\
        .order_by(func.count(User.id).desc())\
        .limit(limit)\
        .all()

def search_images(query, page=1, limit=10):
    """
    Search for images based on title or description with pagination.
    """
    search_query = Image.query.filter(
        (Image.title.ilike(f"%{query}%")) | (Image.description.ilike(f"%{query}%")),
        Image.deleted_at == None
    )
    pagination = search_query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def get_related_images(image_id, limit=5):
    """
    Get related images based on common tags.
    """
    image = get_image_by_id(image_id)
    if not image:
        raise ValueError("Image not found")
    
    related_images = db.session.query(Image, func.count(Tag.id).label('common_tags'))\
        .join(Image.tags)\
        .filter(Tag.images.contains(image))\
        .filter(Image.id != image_id)\
        .filter(Image.deleted_at == None)\
        .group_by(Image.id)\
        .order_by(func.count(Tag.id).desc())\
        .limit(limit)\
        .all()
    
    return related_images
