from app import db
from app.models import Collection, User, Image, Tag, UserImageCollection
from app.utils.db_utils import safe_commit
from sqlalchemy import func, desc

# Basic CRUD operations
# --------------------------------------------------

def create_collection(user_id, name, description=""):
    """Create a new collection for a user."""
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")
    
    new_collection = Collection(name=name, description=description, user_id=user_id)
    db.session.add(new_collection)
    safe_commit("Failed to create collection")
    return new_collection

def get_collection(collection_id):
    """Retrieve a collection by its ID."""
    collection = Collection.query.get(collection_id)
    if not collection:
        raise ValueError("Collection not found")
    return collection

def get_all_collections(page=1, per_page=20, sort_by='created_at', order='desc'):
    """Get all collections with pagination and sorting options."""
    query = Collection.query

    if sort_by == 'name':
        query = query.order_by(desc(Collection.name) if order == 'desc' else Collection.name)
    elif sort_by == 'user_id':
        query = query.order_by(desc(Collection.user_id) if order == 'desc' else Collection.user_id)
    else:
        query = query.order_by(desc(Collection.created_at) if order == 'desc' else Collection.created_at)

    return query.paginate(page=page, per_page=per_page, error_out=False)

def update_collection(collection_id, user_id, name=None, description=None):
    """Update a collection's information."""
    collection = Collection.query.get(collection_id)
    if not collection:
        raise ValueError("Collection not found")
    
    if collection.user_id != user_id:
        raise ValueError("User does not have permission to edit this collection")
    
    if name:
        collection.name = name
    if description is not None:
        collection.description = description
    
    safe_commit("Failed to update collection")
    return collection

def delete_collection(collection_id, user_id):
    """Delete a collection."""
    collection = Collection.query.get(collection_id)
    if not collection:
        raise ValueError("Collection not found")
    
    if collection.user_id != user_id:
        raise ValueError("User does not have permission to delete this collection")
    
    if collection.is_default:
        raise ValueError("Cannot delete the default collection")
    
    db.session.delete(collection)
    safe_commit("Failed to delete collection")

# Advanced operations
# --------------------------------------------------

def add_image_to_collection(user_id, collection_id, image_id):
    """Add an image to a collection."""
    user = User.query.get(user_id)
    collection = Collection.query.get(collection_id)
    image = Image.query.get(image_id)
    
    if not user or not collection or not image:
        raise ValueError("User, Collection or Image not found")
    
    if collection.user_id != user_id:
        raise ValueError("User does not own this collection")
    
    existing_collection = UserImageCollection.query.filter_by(
        user_id=user_id, 
        image_id=image_id, 
        collection_id=collection_id
    ).first()
    
    if not existing_collection:
        new_collection = UserImageCollection(user_id=user_id, image_id=image_id, collection_id=collection_id)
        db.session.add(new_collection)
        image.collection_count += 1
        safe_commit("Failed to add image to collection")
    
    return collection

def remove_image_from_collection(user_id, collection_id, image_id):
    """Remove an image from a collection."""
    user_image_collection = UserImageCollection.query.filter_by(
        user_id=user_id, 
        collection_id=collection_id, 
        image_id=image_id
    ).first()
    
    if not user_image_collection:
        raise ValueError("Image not found in this collection for this user")
    
    image = Image.query.get(image_id)
    image.collection_count -= 1
    
    db.session.delete(user_image_collection)
    safe_commit("Failed to remove image from collection")
    
    return Collection.query.get(collection_id)

def get_user_collections(user_id, page=1, per_page=20):
    """Get collections of a user with pagination."""
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")
    
    return Collection.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page, error_out=False)

def get_collection_images(collection_id, page=1, per_page=20):
    """Get images in a collection with pagination."""
    collection = Collection.query.get(collection_id)
    if not collection:
        raise ValueError("Collection not found")
    
    return Image.query.join(UserImageCollection).filter(UserImageCollection.collection_id == collection_id).paginate(page=page, per_page=per_page, error_out=False)

def get_collection_stats(collection_id):
    """Get statistics for a collection."""
    collection = Collection.query.get(collection_id)
    if not collection:
        raise ValueError("Collection not found")

    return {
        'image_count': UserImageCollection.query.filter_by(collection_id=collection_id).count(),
        'last_added_at': UserImageCollection.query.filter_by(collection_id=collection_id).order_by(UserImageCollection.collect_date.desc()).first().collect_date if UserImageCollection.query.filter_by(collection_id=collection_id).first() else None,
        'top_tags': db.session.query(func.count(Image.id).label('tag_count'), Tag.name).join(UserImageCollection).join(Image.image_tags).filter(UserImageCollection.collection_id == collection_id).group_by(Tag.id).order_by(func.count(Image.id).desc()).limit(5).all()
    }
