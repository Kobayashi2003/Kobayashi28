from app import db
from app.models import Comment, Image
from app.utils.db_utils import safe_commit
from sqlalchemy import desc
from .image_services import get_image_by_id

def get_comment_by_id(id):
    """
    Get comment information by ID.
    """
    return Comment.query.filter_by(id=id, is_active=True).first()

def get_comments_by_user(uid, page=1, limit=10, sort='created_at', reverse=True):
    """
    Get all comments create by a specific user with pagination.
    """
    if not hasattr(Comment, sort):
        raise ValueError(f'Invalid sort field: {sort}')
    
    query = Comment.query.filter_by(uid=uid, is_active=True)
    order = desc(getattr(Comment, sort)) if reverse else getattr(Comment, sort)
    query = query.order_by(order)

    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def get_comments_by_image(imgid, page=1, limit=10, sort='created_at', reverse=True):
    """
    Get comments for a specific image with pagination.
    """
    if not hasattr(Comment, sort):
        raise ValueError(f'Invalid sort field: {sort}')
    
    query = Comment.query.filter_by(imgid=imgid, is_active=True, parent_id=None)
    order = desc(getattr(Comment, sort)) if reverse else getattr(Comment, sort)
    query = query.order_by(order)

    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def get_replies(id, page=1, limit=10, sort='created_at', reverse=True):
    """
    Get replies to a specific comment with pagination.
    """
    if not hasattr(Comment, sort):
        raise ValueError(f'Invalid sort field: {sort}')
    
    query = Comment.query.filter_by(parent_id=id, is_active=True)
    order = desc(getattr(Comment, sort)) if reverse else getattr(Comment, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def get_all_comments(page=1, limit=10, sort='created_at', reverse=True):
    """
    Get a list of all comments with pagination.
    """
    if not hasattr(Comment, sort):
        raise ValueError(f'Invalid sort field: {sort}')

    query = Comment.query.filter_by(is_active=True)
    order = desc(getattr(Comment, sort)) if reverse else getattr(Comment, sort)
    query = query.order_by(order)

    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def create_comment(uid, imgid, content, parent_id=None):
    """
    Create a new comment.
    """
    new_comment = Comment(uid=uid, imgid=imgid, content=content, parent_id=parent_id)
    db.session.add(new_comment)
    safe_commit("Failed to create comment")
    return new_comment

def update_comment(id, uid, content):
    """
    Update comment content.
    """
    comment = get_comment_by_id(id)
    if not comment:
        raise ValueError("Comment not found")
    if comment.uid != uid:
        raise ValueError("Not authorized to update this comment")
    
    if content:
        comment.content = content
    
    safe_commit("Failed to update comment")
    return comment

def delete_comment(id, uid):
    """
    Delete a comment.
    """
    comment = get_comment_by_id(id)
    if not comment:
        raise ValueError("Comment not found")
    if comment.uid != uid:
        raise ValueError("Not authorized to delete this comment")
    
    comment.delete()
    safe_commit("Failed to delete comment")
