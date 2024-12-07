from app import db
from app.models import User, Image, Tag, UserImageLike
from app.utils.db_utils import safe_commit
from sqlalchemy import func

# Basic CRUD operations
# --------------------------------------------------

def like_image(user_id, image_id):
    """Like an image for a user."""
    user = User.query.get(user_id)
    image = Image.query.get(image_id)
    
    if not user or not image:
        raise ValueError("User or Image not found")
    
    existing_like = UserImageLike.query.filter_by(
        user_id=user_id, 
        image_id=image_id
    ).first()
    
    if not existing_like:
        new_like = UserImageLike(user=user, image=image)
        db.session.add(new_like)
        image.like_count += 1
        safe_commit("Failed to like image")
    
    return image

def unlike_image(user_id, image_id):
    """Unlike an image for a user."""
    user_image_like = UserImageLike.query.filter_by(
        user_id=user_id, 
        image_id=image_id
    ).first()
    
    if not user_image_like:
        raise ValueError("User has not liked this image")
    
    image = Image.query.get(image_id)
    if not image:
        raise ValueError("Image not found")
    
    image.like_count -= 1
    
    db.session.delete(user_image_like)
    safe_commit("Failed to unlike image")
    
    return image

# Advanced operations
# --------------------------------------------------

def get_image_likes_count(image_id):
    """Get the number of likes for an image."""
    image = Image.query.get(image_id)
    if not image:
        raise ValueError("Image not found")
    return image.like_count

def get_user_liked_images(user_id):
    """Get all images liked by a user."""
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")
    return [like.image for like in user.liked_images]

def get_users_who_liked_image(image_id, page=1, per_page=20):
    """Get users who liked a specific image with pagination."""
    image = Image.query.get(image_id)
    if not image:
        raise ValueError("Image not found")
    
    return User.query.join(UserImageLike).filter(UserImageLike.image_id == image_id).paginate(page=page, per_page=per_page, error_out=False)

def get_like_suggestions(user_id, page=1, per_page=20):
    """Get image like suggestions for a user based on their liked images' tags."""
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")

    # Get tags of images the user has liked
    liked_tags = Tag.query.join(Image.image_tags).join(UserImageLike).filter(UserImageLike.user_id == user_id).distinct()

    # Get images with these tags that the user hasn't liked yet
    suggested_images = Image.query.join(Image.image_tags).\
        filter(Tag.id.in_([tag.id for tag in liked_tags])).\
        filter(~Image.liked_by.any(UserImageLike.user_id == user_id)).\
        group_by(Image.id).\
        order_by(func.count(Tag.id).desc(), Image.created_at.desc())

    return suggested_images.paginate(page=page, per_page=per_page, error_out=False)

def check_user_liked_image(user_id, image_id):
    """Check if a user has liked a specific image."""
    user = User.query.get(user_id)
    image = Image.query.get(image_id)
    
    if not user or not image:
        raise ValueError("User or Image not found")
    
    return UserImageLike.query.filter_by(user_id=user_id, image_id=image_id).first() is not None
