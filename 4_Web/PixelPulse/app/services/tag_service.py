from app import db
from app.models import Tag, User, Image, ImageTagAssociation, UserTagIgnore
from app.utils.db_utils import safe_commit
from sqlalchemy import func, desc

# Basic CRUD operations
# --------------------------------------------------

def create_tag(name, creator_id):
    """Create a new tag or return an existing one."""
    user = User.query.get(creator_id)
    if not user:
        raise ValueError("User not found")
    
    tag = Tag.query.filter_by(name=name).first()
    if tag:
        return tag, False  # Tag already exists

    new_tag = Tag(name=name, creator_id=creator_id)
    db.session.add(new_tag)
    safe_commit("Failed to create tag")
    return new_tag, True  # New tag created

def get_tag(tag_id):
    """Retrieve a tag by its ID."""
    tag = Tag.query.get(tag_id)
    if not tag:
        raise ValueError("Tag not found")
    return tag

def get_all_tags(page=1, per_page=20, sort_by='name', order='asc'):
    """Get all tags with pagination and sorting options."""
    query = Tag.query

    if sort_by == 'image_count':
        query = query.order_by(desc(Tag.image_count) if order == 'desc' else Tag.image_count)
    elif sort_by == 'created_at':
        query = query.order_by(desc(Tag.created_at) if order == 'desc' else Tag.created_at)
    else:
        query = query.order_by(desc(Tag.name) if order == 'desc' else Tag.name)

    return query.paginate(page=page, per_page=per_page, error_out=False)

def update_tag(tag_id, new_name, user_id):
    """Update a tag's name."""
    tag = Tag.query.get(tag_id)
    if not tag:
        raise ValueError("Tag not found")
    
    if tag.creator_id != user_id:
        raise ValueError("User does not have permission to edit this tag")
    
    tag.name = new_name
    safe_commit("Failed to update tag")
    return tag

def delete_tag(tag_id, user_id):
    """Delete a tag."""
    tag = Tag.query.get(tag_id)
    if not tag:
        raise ValueError("Tag not found")
    
    if tag.creator_id != user_id:
        raise ValueError("User does not have permission to delete this tag")
    
    db.session.delete(tag)
    safe_commit("Failed to delete tag")

# Advanced operations
# --------------------------------------------------

def get_tag_by_name(name):
    """Retrieve a tag by its name."""
    tag = Tag.query.filter_by(name=name).first()
    if not tag:
        raise ValueError("Tag not found")
    return tag

def add_tag_to_image(tag_id, image_id):
    """Add a tag to an image."""
    tag = Tag.query.get(tag_id)
    image = Image.query.get(image_id)
    if not tag or not image:
        raise ValueError("Tag or Image not found")
    
    association = ImageTagAssociation.query.filter_by(tag_id=tag_id, image_id=image_id).first()
    if not association:
        new_association = ImageTagAssociation(tag_id=tag_id, image_id=image_id)
        db.session.add(new_association)
        tag.image_count += 1
        safe_commit("Failed to add tag to image")
    return tag

def remove_tag_from_image(tag_id, image_id):
    """Remove a tag from an image."""
    association = ImageTagAssociation.query.filter_by(tag_id=tag_id, image_id=image_id).first()
    if not association:
        raise ValueError("Tag is not associated with this image")
    
    tag = Tag.query.get(tag_id)
    tag.image_count -= 1
    
    db.session.delete(association)
    safe_commit("Failed to remove tag from image")
    return tag

def get_images_by_tag(tag_id, page=1, per_page=20):
    """Get images associated with a tag with pagination."""
    tag = Tag.query.get(tag_id)
    if not tag:
        raise ValueError("Tag not found")
    
    return Image.query.join(ImageTagAssociation).filter(ImageTagAssociation.tag_id == tag_id).paginate(page=page, per_page=per_page, error_out=False)

def get_popular_tags(limit=10):
    """Get the most popular tags based on image count."""
    return Tag.query.order_by(Tag.image_count.desc()).limit(limit).all()

def ignore_tag(user_id, tag_id):
    """Add a tag to a user's ignored tags list."""
    user = User.query.get(user_id)
    tag = Tag.query.get(tag_id)
    if not user or not tag:
        raise ValueError("User or Tag not found")
    
    ignore = UserTagIgnore.query.filter_by(user_id=user_id, tag_id=tag_id).first()
    if not ignore:
        new_ignore = UserTagIgnore(user_id=user_id, tag_id=tag_id)
        db.session.add(new_ignore)
        safe_commit("Failed to ignore tag")
    return tag

def unignore_tag(user_id, tag_id):
    """Remove a tag from a user's ignored tags list."""
    ignore = UserTagIgnore.query.filter_by(user_id=user_id, tag_id=tag_id).first()
    if not ignore:
        raise ValueError("Tag is not in the user's ignored list")
    
    db.session.delete(ignore)
    safe_commit("Failed to unignore tag")

def get_user_ignored_tags(user_id, page=1, per_page=20):
    """Get tags ignored by a user with pagination."""
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")
    
    return Tag.query.join(UserTagIgnore).filter(UserTagIgnore.user_id == user_id).paginate(page=page, per_page=per_page, error_out=False)

def get_tag_stats(tag_id):
    """Get statistics for a tag."""
    tag = Tag.query.get(tag_id)
    if not tag:
        raise ValueError("Tag not found")

    return {
        'image_count': tag.image_count,
        'user_count': User.query.join(Image).join(ImageTagAssociation).filter(ImageTagAssociation.tag_id == tag_id).distinct().count(),
        'last_used': ImageTagAssociation.query.filter_by(tag_id=tag_id).order_by(ImageTagAssociation.created_at.desc()).first().created_at if tag.image_count > 0 else None,
        'top_users': User.query.join(Image).join(ImageTagAssociation).filter(ImageTagAssociation.tag_id == tag_id).group_by(User.id).order_by(func.count(Image.id).desc()).limit(5).all()
    }
