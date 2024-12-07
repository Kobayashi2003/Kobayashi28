from app import db
from app.models import Image, User, Tag, UserImagePublish
from app.utils.db_utils import safe_commit
from app.utils.file_utils import get_image_path
from sqlalchemy import desc
from datetime import datetime, timezone, timedelta
from werkzeug.utils import secure_filename

# Basic CRUD operations
# --------------------------------------------------

def create_image(user_id, title, description, tags):
    """Create a new image with associated tags."""
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")

    new_image = Image(title=title, description=description)
    db.session.add(new_image)
    db.session.flush()

    publish = UserImagePublish(user_id=user_id, image_id=new_image.id)
    db.session.add(publish)

    for tag_name in tags:
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name, creator_id=user_id)
            db.session.add(tag)
        new_image.image_tags.append(tag)

    safe_commit("Failed to create image")
    return new_image

def get_image(image_id):
    """Retrieve an image by its ID."""
    return Image.query.get(image_id)

def get_all_images(page=1, per_page=20, sort_by='created_at', order='desc', tag=None, min_likes=0):
    """Get all images with pagination and filtering options."""
    query = Image.query

    if tag:
        query = query.filter(Image.image_tags.any(Tag.name == tag))

    if min_likes > 0:
        query = query.filter(Image.like_count >= min_likes)

    if sort_by == 'likes':
        query = query.order_by(desc(Image.like_count) if order == 'desc' else Image.like_count)
    else:
        query = query.order_by(desc(Image.created_at) if order == 'desc' else Image.created_at)

    return query.paginate(page=page, per_page=per_page, error_out=False)

def update_image(image_id, user_id, title=None, description=None, tags=None):
    """Update an image's information and tags."""
    image = Image.query.get(image_id)
    if not image:
        raise ValueError("Image not found")

    publish = UserImagePublish.query.filter_by(image_id=image_id, user_id=user_id).first()
    if not publish:
        raise ValueError("User does not have permission to edit this image")

    if title:
        image.title = title
    if description:
        image.description = description

    if tags:
        image.image_tags = []
        for tag_name in tags:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name, creator_id=user_id)
                db.session.add(tag)
            image.image_tags.append(tag)

    safe_commit("Failed to update image")
    return image

def delete_image(image_id, user_id):
    """Delete an image."""
    image = Image.query.get(image_id)
    if not image:
        raise ValueError("Image not found")

    publish = UserImagePublish.query.filter_by(image_id=image_id, user_id=user_id).first()
    if not publish:
        raise ValueError("User does not have permission to delete this image")

    db.session.delete(image)
    safe_commit("Failed to delete image")

# Advanced operations
# --------------------------------------------------

def create_image(user_id, title, description, tags, file):
    """Create a new image with associated tags and save the file."""
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")

    new_image = Image(title=title, description=description)
    db.session.add(new_image)
    db.session.flush()  # This will assign an ID to new_image

    # Save the file
    filename = secure_filename(file.filename)
    file_path = get_image_path(new_image.id)
    file.save(file_path)

    publish = UserImagePublish(user_id=user_id, image_id=new_image.id)
    db.session.add(publish)

    for tag_name in tags:
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name, creator_id=user_id)
            db.session.add(tag)
        new_image.image_tags.append(tag)

    safe_commit("Failed to create image")
    return new_image

def search_images(query, page=1, per_page=20):
    """Search images by title, description, or tags."""
    return Image.query.filter(
        (Image.title.ilike(f'%{query}%')) |
        (Image.description.ilike(f'%{query}%')) |
        (Image.image_tags.any(Tag.name.ilike(f'%{query}%')))
    ).order_by(Image.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

def get_user_images(user_id, page=1, per_page=20):
    """Get images published by a user with pagination."""
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")

    return Image.query.join(UserImagePublish).filter(UserImagePublish.user_id == user_id).order_by(Image.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

def get_feed_images(user_id, page=1, per_page=20):
    """Get feed images for a user with pagination."""
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")

    followed_users = [follow.followed_id for follow in user.following]
    return Image.query.join(UserImagePublish).filter(UserImagePublish.user_id.in_(followed_users)).order_by(Image.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

def get_trending_images(time_period='day', page=1, per_page=20):
    """Get trending images for a specific time period."""
    if time_period == 'day':
        start_date = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    elif time_period == 'week':
        start_date = datetime.now(timezone.utc) - timedelta(days=7)
    elif time_period == 'month':
        start_date = datetime.now(timezone.utc) - timedelta(days=30)
    else:
        raise ValueError("Invalid time period. Choose 'day', 'week', or 'month'.")

    return Image.query.filter(Image.created_at >= start_date).order_by(
        (Image.like_count + Image.comment_count).desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
