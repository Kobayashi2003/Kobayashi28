from app import db
from app.models import Image 
from app.utils.db_utils import safe_commit
from sqlalchemy import desc

def get_image_by_id(id):
    """
    Get image information by ID.
    """
    return Image.query.filter_by(id=id, is_active=True).first()

def get_images_by_user(uid, page=1, limit=10, sort='id', reverse=False):
    """
    Get all images uploaded by a specific user with pagination.
    """
    if not hasattr(Image, sort):
        raise ValueError(f"Invalid sort field: {sort}")
    
    query = Image.query.filter_by(uid=uid, is_active=True)
    order = desc(getattr(Image, sort)) if reverse else getattr(Image, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def get_all_images(page=1, limit=10, sort='id', reverse=False):
    """
    Get a list of all images with pagination.
    """
    if not hasattr(Image, sort):
        raise ValueError(f"Invalid sort field: {sort}")

    query = Image.query.filter_by(is_active=True)
    order = desc(getattr(Image, sort)) if reverse else getattr(Image, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def search_images(query, page=1, limit=10, sort='id', reverse=False):
    """
    Search for images based on title, description or tags with pagination.
    """
    if not hasattr(Image, sort):
        raise ValueError(f"Invalid sort field: {sort}")

    query = Image.query.filter(
        Image.title.ilike(f'%{query}%') |
        Image.description.ilike(f'%{query}%'),
        Image.is_active == True
    )
    order = desc(getattr(Image, sort)) if reverse else getattr(Image, sort)
    query.order_by(order)

    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def create_image(uid, title, description, url):
    """
    Create a new image.
    """
    new_image = Image(
        title=title, 
        url=url, 
        description=description, 
        uid=uid
    )
    db.session.add(new_image)
    safe_commit('Failed to create image')
    return new_image

def update_image(id, uid, title=None, description=None, url=None):
    """
    Update image information
    """
    image = get_image_by_id(id)
    if not image:
        raise ValueError("Image not found")
    if image.uid != uid:
        raise ValueError("Not authorized to update this image")

    if title:
        image.title = title
    if url:
        image.url = url
    if description is not None:
        image.description = description
    
    safe_commit('Failed to update image')
    return image

def delete_image(id, uid):
    """
    Delete an image.
    """
    image = get_image_by_id(id)
    if not image:
        raise ValueError("Image not found")
    if image.uid != uid:
        raise ValueError("Not authorized to delete this image")
    
    image.delete()
    safe_commit("Failed to delete image") 