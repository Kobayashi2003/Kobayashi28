from app import db
from app.models import Tag, Image
from app.utils.db_utils import safe_commit
from sqlalchemy import desc
from .image_services import get_image_by_id

def get_tag_by_id(id):
    """
    Get tag information by ID.
    """
    return Tag.query.filter_by(id=id, is_active=True).first()

def get_tag_by_name(name):
    """
    Get tag information by ID.
    """
    return Tag.query.filter_by(name=name, is_active=True).first()

def get_tags_by_user(uid, page=1, limit=10, sort='id', reverse=False):
    """
    Get all tags created by a specific user with pagination.
    """
    if not hasattr(Tag, sort):
        raise ValueError(f"Invalid sort field: {sort}")
    
    query = Tag.query.filter_by(uid=uid, is_active=True)
    order = desc(getattr(Tag, sort)) if reverse else getattr(Tag, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def get_tags_by_image(imgid, page=1, limit=10, sort='id', reverse=False):
    """
    Get tags for a specific image with pagination.
    """
    if not hasattr(Tag, sort):
        raise ValueError(f'Invalid sort field: {sort}')

    query = Tag.query.filter_by(imgid=imgid, is_active=True)
    order = desc(getattr(Tag, sort)) if reverse else getattr(Tag, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page
    
def get_all_tags(page=1, limit=10, sort='id', reverse=False):
    """
    Get a list of all tags with pagination.
    """
    if not hasattr(Tag, sort):
        raise ValueError(f"Invalid sort field: {sort}")

    query = Tag.query.filter_by(is_active=True)
    order = desc(getattr(Tag, sort)) if reverse else getattr(Tag, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def serach_tags(query, page=1, limit=10, sort='id', reverse=False):
    """
    Search for tags based on a query string with pagination.
    """
    if not hasattr(Tag, sort):
        raise ValueError(f"Invalid sort field: {sort}")
    
    query = Tag.query.filter(
        Tag.name.ilike(f'%{query}%'),
        Tag.is_active == True
    )
    order = desc(getattr(Tag, sort)) if reverse else getattr(Tag, sort)
    query.order_by(order)

    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def create_tag(uid, name):
    """
    Create a new tag.
    """
    new_tag = Tag(name=name, uid=uid)
    db.session.add(new_tag)
    safe_commit("Failed to create tag. Name may already exist.")
    return new_tag

def update_tag(id, uid, name=None):
    """
    Update tag information.
    """
    tag = get_tag_by_id(id)
    if not tag:
        raise ValueError("Tag not found")
    if tag.uid != uid:
        raise ValueError("Not authorized to update this tag")
    
    if name:
        tag.name = name 

    safe_commit("Failed to update tag. Name may already exist.")
    return tag

def delete_tag(id, uid):
    """
    Delete a tag.
    """
    tag = get_tag_by_id(id)
    if not tag:
        raise ValueError("Tag not found")
    if tag.uid != uid:
        raise ValueError("Not authorized to delete this tag")

    tag.delete()
    safe_commit("Failed to delete tag")

def add_tag_to_image(tag_id, image_id, user_id):
    """
    Add a tag to an image.
    """
    tag = get_tag_by_id(tag_id)
    if not tag:
        raise ValueError("Tag not found")
    image = get_image_by_id(image_id)
    if not image:
        raise ValueError("Image not found")
    if not image.uid != user_id:
        raise ValueError("Not authorized to add tag to this image")

    if tag not in image.tags:
        image.tags.append(tag)
        safe_commit("Failed to add tag to image")

def remove_tag_from_image(tag_id, image_id, user_id):
    """
    Remove a tag from an image.
    """
    tag = get_tag_by_id(tag_id)
    if not tag:
        raise ValueError("Tag not found")
    image = get_image_by_id(image_id)
    if not image:
        raise ValueError("Image not found")
    if not image.uid != user_id:
        raise ValueError("Not authorized to remove tag to this image")

    
    if tag in image.tags:
        image.tags.remove(tag)
        safe_commit("Failed to remove tag from image")

def get_images_by_tag(id, page=1, limit=10, sort='id', reverse=False):
    """
    Get all images associated with a specific tag with pagination.
    """
    tag = get_tag_by_id(id)
    if not tag:
        raise ValueError("Tag not found")
    if not hasattr(Image, sort):
        raise ValueError(f"Invalid sort field: {sort}")

    query = tag.images.filter(Image.is_active == True)
    order = desc(getattr(Image, sort)) if reverse else getattr(Image, sort)
    query = query.order_by(order)

    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

