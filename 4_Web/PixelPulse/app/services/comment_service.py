from app import db
from app.models import Comment, User, Image
from app.utils.db_utils import safe_commit
from sqlalchemy import func, desc
from datetime import datetime, timezone

# Basic CRUD operations
# --------------------------------------------------

def create_comment(user_id, image_id, content):
    """Create a new comment for an image."""
    user = User.query.get(user_id)
    image = Image.query.get(image_id)
    
    if not user or not image:
        raise ValueError("User or Image not found")
    
    new_comment = Comment(content=content, user_id=user_id, image_id=image_id)
    db.session.add(new_comment)
    image.comment_count += 1
    
    safe_commit("Failed to create comment")
    return new_comment

def get_comment(comment_id):
    """Retrieve a comment by its ID."""
    comment = Comment.query.get(comment_id)
    if not comment:
        raise ValueError("Comment not found")
    return comment

def get_all_comments(page=1, per_page=20, sort_by='created_at', order='desc'):
    """Get all comments with pagination and sorting options."""
    query = Comment.query

    if sort_by == 'user_id':
        query = query.join(User).order_by(desc(User.id) if order == 'desc' else User.id)
    elif sort_by == 'image_id':
        query = query.order_by(desc(Comment.image_id) if order == 'desc' else Comment.image_id)
    else:
        query = query.order_by(desc(Comment.created_at) if order == 'desc' else Comment.created_at)

    return query.paginate(page=page, per_page=per_page, error_out=False)

def update_comment(comment_id, user_id, new_content):
    """Update a comment's content."""
    comment = Comment.query.get(comment_id)
    if not comment:
        raise ValueError("Comment not found")
    
    if comment.user_id != user_id:
        raise ValueError("User does not have permission to edit this comment")
    
    comment.content = new_content
    comment.updated_at = datetime.now(timezone.utc)
    safe_commit("Failed to update comment")
    return comment

def delete_comment(comment_id, user_id):
    """Delete a comment."""
    comment = Comment.query.get(comment_id)
    if not comment:
        raise ValueError("Comment not found")
    
    if comment.user_id != user_id:
        raise ValueError("User does not have permission to delete this comment")
    
    image = Image.query.get(comment.image_id)
    image.comment_count -= 1
    
    db.session.delete(comment)
    safe_commit("Failed to delete comment")

# Advanced operations
# --------------------------------------------------

def get_image_comments(image_id, page=1, per_page=20):
    """Get comments for a specific image with pagination."""
    image = Image.query.get(image_id)
    if not image:
        raise ValueError("Image not found")
    
    return Comment.query.filter_by(image_id=image_id).order_by(Comment.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

def get_user_comments(user_id, page=1, per_page=20):
    """Get comments made by a specific user with pagination."""
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")
    
    return Comment.query.filter_by(user_id=user_id).order_by(Comment.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

def get_recent_comments(page=1, per_page=20):
    """Get recent comments across all images with pagination."""
    return Comment.query.order_by(Comment.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

def search_comments(query, page=1, per_page=20):
    """Search comments by content."""
    return Comment.query.filter(Comment.content.ilike(f'%{query}%')).order_by(Comment.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

def get_comment_stats(image_id):
    """Get comment statistics for an image."""
    image = Image.query.get(image_id)
    if not image:
        raise ValueError("Image not found")

    return {
        'comment_count': image.comment_count,
        'last_comment_at': Comment.query.filter_by(image_id=image_id).order_by(Comment.created_at.desc()).first().created_at if image.comment_count > 0 else None,
        'top_commenters': User.query.join(Comment).filter(Comment.image_id == image_id).group_by(User.id).order_by(func.count(Comment.id).desc()).limit(5).all()
    }
