from app import db
from app.models import Tag, Image
from app.utils.db_utils import safe_commit
from sqlalchemy import func, desc

def create_tag(name, user_id):
    """
    Create a new tag.
    """
    new_tag = Tag(name=name, uid=user_id)
    db.session.add(new_tag)
    safe_commit("Failed to create tag. Name may already exist.")
    return new_tag

def get_tag_by_id(tag_id):
    """
    Get tag information by ID.
    """
    return Tag.query.get(tag_id)

def get_tag_by_name(name):
    """
    Get tag information by name.
    """
    return Tag.query.filter_by(name=name).first()

def update_tag(tag_id, name):
    """
    Update tag information.
    """
    tag = get_tag_by_id(tag_id)
    if not tag:
        raise ValueError("Tag not found")
    
    tag.name = name
    safe_commit("Failed to update tag. Name may already exist.")
    return tag

def delete_tag(tag_id):
    """
    Delete a tag.
    """
    tag = get_tag_by_id(tag_id)
    if not tag:
        raise ValueError("Tag not found")
    
    tag.delete()
    safe_commit("Failed to delete tag")

def get_all_tags(page=1, limit=10, sort='id', reverse=False):
    """
    Get a list of all tags with pagination.
    """
    # Validate sort field
    if not hasattr(Tag, sort):
        raise ValueError(f"Invalid sort field: {sort}")
    
    # Create query
    query = Tag.query.filter_by(deleted_at=None)
    
    # Apply sorting
    order = desc(getattr(Tag, sort)) if reverse else getattr(Tag, sort)
    query = query.order_by(order)
    
    # Apply pagination
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    
    return pagination.items, pagination.total, pagination.pages > page

def get_tags_by_user(user_id, page=1, limit=10, sort='id', reverse=False):
    """
    Get all tags created by a specific user with pagination.
    """
    # Validate sort field
    if not hasattr(Tag, sort):
        raise ValueError(f"Invalid sort field: {sort}")
    
    # Create query
    query = Tag.query.filter_by(uid=user_id, deleted_at=None)
    
    # Apply sorting
    order = desc(getattr(Tag, sort)) if reverse else getattr(Tag, sort)
    query = query.order_by(order)
    
    # Apply pagination
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    
    return pagination.items, pagination.total, pagination.pages > page

def get_popular_tags(limit=10):
    """
    Get the most popular tags based on usage.
    """
    return db.session.query(Tag, func.count(Image.id).label('image_count'))\
        .join(Tag.images)\
        .filter(Tag.deleted_at == None)\
        .group_by(Tag.id)\
        .order_by(func.count(Image.id).desc())\
        .limit(limit)\
        .all()

def add_tag_to_image(tag_id, image_id):
    """
    Add a tag to an image.
    """
    tag = get_tag_by_id(tag_id)
    image = Image.query.get(image_id)
    if not tag or not image:
        raise ValueError("Tag or Image not found")
    
    if tag not in image.tags:
        image.tags.append(tag)
        safe_commit("Failed to add tag to image")

def remove_tag_from_image(tag_id, image_id):
    """
    Remove a tag from an image.
    """
    tag = get_tag_by_id(tag_id)
    image = Image.query.get(image_id)
    if not tag or not image:
        raise ValueError("Tag or Image not found")
    
    if tag in image.tags:
        image.tags.remove(tag)
        safe_commit("Failed to remove tag from image")

def get_images_by_tag(tag_id, page=1, limit=10, sort='id', reverse=False):
    """
    Get all images associated with a specific tag with pagination.
    """
    tag = get_tag_by_id(tag_id)
    if not tag:
        raise ValueError("Tag not found")
    
    # Validate sort field
    if not hasattr(Image, sort):
        raise ValueError(f"Invalid sort field: {sort}")
    
    # Create query
    query = tag.images.filter(Image.deleted_at == None)
    
    # Apply sorting
    order = desc(getattr(Image, sort)) if reverse else getattr(Image, sort)
    query = query.order_by(order)
    
    # Apply pagination
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    
    return pagination.items, pagination.total, pagination.pages > page

def search_tags(query, page=1, limit=10):
    """
    Search for tags based on a query string with pagination.
    """
    search_query = Tag.query.filter(Tag.name.ilike(f"%{query}%"), Tag.deleted_at == None)
    pagination = search_query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page
