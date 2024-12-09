from app import db
from app.models import User, Image, Tag, Comment
from sqlalchemy import func, desc
from datetime import datetime, timedelta, timezone

def get_recommended_images(user_id, page=1, limit=10):
    """
    Get persistent recommended images based on the user's behavior and similar users' behavior.
    """
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")

    # Find similar users based on liked and favorited images
    similar_users = db.session.query(User.id).filter(
        (User.id != user_id) &
        (User.liked_images.any(Image.id.in_(db.session.query(Image.id).filter(Image.liked_by.contains(user)))) |
         User.favorited_images.any(Image.id.in_(db.session.query(Image.id).filter(Image.favorited_by.contains(user))))
    ).subquery())

    # Get images liked or favorited by similar users, but not by the current user
    query = db.session.query(Image, func.count(User.id).label('score'))\
        .join(Image.liked_by)\
        .outerjoin(Image.favorited_by)\
        .filter(User.id.in_(similar_users))\
        .filter(~Image.liked_by.contains(user))\
        .filter(~Image.favorited_by.contains(user))\
        .group_by(Image.id)\
        .order_by(desc('score'))
    
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def get_recommended_users(user_id, page=1, limit=10):
    """
    Get persistent recommended users to follow based on the user's behavior and similar users' behavior.
    """
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")

    # Find users who have similar interests (liked or favorited similar images)
    query = db.session.query(User, func.count(Image.id).label('common_interests'))\
        .join(User.liked_images)\
        .outerjoin(User.favorited_images)\
        .filter(Image.id.in_(
            db.session.query(Image.id)\
            .filter((Image.liked_by.contains(user)) | (Image.favorited_by.contains(user)))
        ))\
        .filter(User.id != user_id)\
        .filter(~User.followers.contains(user))\
        .group_by(User.id)\
        .order_by(desc('common_interests'))
    
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def get_recommended_images_after_interaction(user_id, interacted_image_id, page=1, limit=5):
    """
    Get recommended images after a user likes or favorites an image.
    """
    user = User.query.get(user_id)
    interacted_image = Image.query.get(interacted_image_id)
    if not user or not interacted_image:
        raise ValueError("User or Image not found")

    # Get tags of the interacted image
    interacted_tags = [tag.id for tag in interacted_image.tags]

    # Find images with similar tags that the user hasn't interacted with
    query = db.session.query(Image, func.count(Tag.id).label('matching_tags'))\
        .join(Image.tags)\
        .filter(Tag.id.in_(interacted_tags))\
        .filter(Image.id != interacted_image_id)\
        .filter(~Image.liked_by.contains(user))\
        .filter(~Image.favorited_by.contains(user))\
        .group_by(Image.id)\
        .order_by(desc('matching_tags'))
    
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def get_recommended_users_after_follow(user_id, followed_user_id, page=1, limit=5):
    """
    Get recommended users to follow after a user follows another user.
    """
    user = User.query.get(user_id)
    followed_user = User.query.get(followed_user_id)
    if not user or not followed_user:
        raise ValueError("User not found")

    # Find users who are followed by the user we just followed
    query = db.session.query(User)\
        .filter(User.followers.contains(followed_user))\
        .filter(User.id != user_id)\
        .filter(~User.followers.contains(user))\
        .order_by(func.random())
    
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def get_popular_images(time_period='day', page=1, limit=10):
    """
    Get popular images based on recent likes, comments, and favorites.
    """
    if time_period == 'day':
        start_time = datetime.now(timezone.utc) - timedelta(days=1)
    elif time_period == 'week':
        start_time = datetime.now(timezone.utc) - timedelta(weeks=1)
    elif time_period == 'month':
        start_time = datetime.now(timezone.utc) - timedelta(days=30)
    else:
        raise ValueError("Invalid time period. Choose 'day', 'week', or 'month'.")

    query = db.session.query(Image, func.count(User.id).label('interaction_count'))\
        .outerjoin(Image.liked_by)\
        .outerjoin(Image.favorited_by)\
        .outerjoin(Image.comments)\
        .filter((User.last_login > start_time) | (Image.comments.any(Comment.created_at > start_time)))\
        .group_by(Image.id)\
        .order_by(desc('interaction_count'))
    
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def get_trending_users(time_period='week', page=1, limit=10):
    """
    Get trending users based on recent follower growth and activity.
    """
    if time_period == 'day':
        start_time = datetime.now(timezone.utc) - timedelta(days=1)
    elif time_period == 'week':
        start_time = datetime.now(timezone.utc) - timedelta(weeks=1)
    elif time_period == 'month':
        start_time = datetime.now(timezone.utc) - timedelta(days=30)
    else:
        raise ValueError("Invalid time period. Choose 'day', 'week', or 'month'.")

    query = db.session.query(User, func.count(Image.id).label('activity_score'))\
        .outerjoin(User.images)\
        .outerjoin(User.comments)\
        .filter((Image.created_at > start_time) | (Comment.created_at > start_time))\
        .group_by(User.id)\
        .order_by(desc('activity_score'))
    
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def get_personalized_feed(user_id, page=1, limit=20):
    """
    Generate a personalized feed for a user based on their interests and social connections.
    """
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")

    # Images from users the current user is following
    following_images = db.session.query(Image)\
        .join(Image.user)\
        .filter(User.followers.contains(user))\
        .order_by(desc(Image.created_at))\
        .limit(limit // 2)\
        .subquery()

    # Images with tags similar to those the user has interacted with
    user_tags = db.session.query(Tag.id)\
        .join(Tag.images)\
        .filter((Image.liked_by.contains(user)) | (Image.favorited_by.contains(user)))\
        .distinct()\
        .subquery()

    tag_based_images = db.session.query(Image)\
        .join(Image.tags)\
        .filter(Tag.id.in_(user_tags))\
        .filter(Image.uid != user_id)\
        .order_by(func.random())\
        .limit(limit // 2)\
        .subquery()

    # Combine and shuffle the results
    query = db.session.query(Image)\
        .filter((Image.id.in_(following_images)) | (Image.id.in_(tag_based_images)))\
        .order_by(func.random())
    
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page
