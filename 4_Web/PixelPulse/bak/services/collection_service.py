from app import db
from app.models import Collection, Image
from app.utils.db_utils import safe_commit
from sqlalchemy import desc

def create_collection(name, description, user_id, is_default=False):
    """
    Create a new collection.
    """
    new_collection = Collection(name=name, description=description, uid=user_id, is_default=is_default)
    db.session.add(new_collection)
    safe_commit("Failed to create collection")
    return new_collection

def get_collection_by_id(collection_id):
    """
    Get collection information by ID.
    """
    return Collection.query.get(collection_id)

def update_collection(collection_id, name=None, description=None):
    """
    Update collection information.
    """
    collection = get_collection_by_id(collection_id)
    if not collection:
        raise ValueError("Collection not found")
    
    if name:
        collection.name = name
    if description is not None:  # Allow setting an empty string
        collection.description = description
    
    safe_commit("Failed to update collection")
    return collection

def delete_collection(collection_id):
    """
    Delete a collection.
    """
    collection = get_collection_by_id(collection_id)
    if not collection:
        raise ValueError("Collection not found")
    
    collection.delete()
    safe_commit("Failed to delete collection")

def get_collections_by_user(user_id, page=1, limit=10, sort='created_at', reverse=True):
    """
    Get all collections created by a specific user with pagination.
    """
    if not hasattr(Collection, sort):
        raise ValueError(f"Invalid sort field: {sort}")
    
    query = Collection.query.filter_by(uid=user_id, deleted_at=None)
    order = desc(getattr(Collection, sort)) if reverse else getattr(Collection, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def add_image_to_collection(collection_id, image_id):
    """
    Add an image to a collection.
    """
    collection = get_collection_by_id(collection_id)
    image = Image.query.get(image_id)
    if not collection or not image:
        raise ValueError("Collection or Image not found")
    
    if image not in collection.images:
        collection.images.append(image)
        safe_commit("Failed to add image to collection")

def remove_image_from_collection(collection_id, image_id):
    """
    Remove an image from a collection.
    """
    collection = get_collection_by_id(collection_id)
    image = Image.query.get(image_id)
    if not collection or not image:
        raise ValueError("Collection or Image not found")
    
    if image in collection.images:
        collection.images.remove(image)
        safe_commit("Failed to remove image from collection")

def get_images_in_collection(collection_id, page=1, limit=10, sort='created_at', reverse=True):
    """
    Get all images in a specific collection with pagination.
    """
    collection = get_collection_by_id(collection_id)
    if not collection:
        raise ValueError("Collection not found")
    
    if not hasattr(Image, sort):
        raise ValueError(f"Invalid sort field: {sort}")
    
    query = collection.images.filter(Image.deleted_at == None)
    order = desc(getattr(Image, sort)) if reverse else getattr(Image, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def get_collection_count(user_id):
    """
    Get the number of collections for a specific user.
    """
    return Collection.query.filter_by(uid=user_id, deleted_at=None).count()

def is_collection_owner(collection_id, user_id):
    """
    Check if a user is the owner of a collection.
    """
    collection = get_collection_by_id(collection_id)
    return collection and collection.uid == user_id
