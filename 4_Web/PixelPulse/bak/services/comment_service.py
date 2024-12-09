from app import db
from app.models import Comment
from app.utils.db_utils import safe_commit
from sqlalchemy import desc

def create_comment(content, user_id, image_id, parent_id=None):
    """
    Create a new comment.
    """
    new_comment = Comment(content=content, uid=user_id, imgid=image_id, parent_id=parent_id)
    db.session.add(new_comment)
    safe_commit("Failed to create comment")
    return new_comment

def get_comment_by_id(comment_id):
    """
    Get comment information by ID.
    """
    return Comment.query.get(comment_id)

def update_comment(comment_id, content):
    """
    Update comment content.
    """
    comment = get_comment_by_id(comment_id)
    if not comment:
        raise ValueError("Comment not found")
    
    comment.content = content
    safe_commit("Failed to update comment")
    return comment

def delete_comment(comment_id):
    """
    Delete a comment.
    """
    comment = get_comment_by_id(comment_id)
    if not comment:
        raise ValueError("Comment not found")
    
    comment.delete()
    safe_commit("Failed to delete comment")

def get_comments_by_image(image_id, page=1, limit=10, sort='created_at', reverse=True):
    """
    Get comments for a specific image with pagination.
    """
    if not hasattr(Comment, sort):
        raise ValueError(f"Invalid sort field: {sort}")
    
    query = Comment.query.filter_by(imgid=image_id, deleted_at=None, parent_id=None)
    order = desc(getattr(Comment, sort)) if reverse else getattr(Comment, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def get_comments_by_user(user_id, page=1, limit=10, sort='created_at', reverse=True):
    """
    Get comments made by a specific user with pagination.
    """
    if not hasattr(Comment, sort):
        raise ValueError(f"Invalid sort field: {sort}")
    
    query = Comment.query.filter_by(uid=user_id, deleted_at=None)
    order = desc(getattr(Comment, sort)) if reverse else getattr(Comment, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def get_replies(comment_id, page=1, limit=10, sort='created_at', reverse=True):
    """
    Get replies to a specific comment with pagination.
    """
    if not hasattr(Comment, sort):
        raise ValueError(f"Invalid sort field: {sort}")
    
    query = Comment.query.filter_by(parent_id=comment_id, deleted_at=None)
    order = desc(getattr(Comment, sort)) if reverse else getattr(Comment, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def get_comment_count(image_id):
    """
    Get the number of comments for a specific image.
    """
    return Comment.query.filter_by(imgid=image_id, deleted_at=None).count()

def is_comment_owner(comment_id, user_id):
    """
    Check if a user is the owner of a comment.
    """
    comment = get_comment_by_id(comment_id)
    return comment and comment.uid == user_id
