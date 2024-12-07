from app import db
from app.models import User, UserFollow
from app.utils.db_utils import safe_commit
from sqlalchemy.exc import IntegrityError

# Basic CRUD operations
# --------------------------------------------------

def follow_user(follower_id, followed_id):
    """Create a new follow relationship."""
    if follower_id == followed_id:
        raise ValueError("Users cannot follow themselves")

    follower = User.query.get(follower_id)
    followed = User.query.get(followed_id)

    if not follower or not followed:
        raise ValueError("User not found")

    if follower.is_following(followed):
        raise ValueError("Already following this user")

    follow = UserFollow(follower_id=follower_id, followed_id=followed_id)
    db.session.add(follow)
    safe_commit("Failed to follow user")
    return follow

def unfollow_user(follower_id, followed_id):
    """Remove a follow relationship."""
    if follower_id == followed_id:
        raise ValueError("Users cannot unfollow themselves")

    follower = User.query.get(follower_id)
    followed = User.query.get(followed_id)

    if not follower or not followed:
        raise ValueError("User not found")

    follow = UserFollow.query.filter_by(follower_id=follower_id, followed_id=followed_id).first()

    if not follow:
        raise ValueError("Not following this user")

    db.session.delete(follow)
    safe_commit("Failed to unfollow user")

# Advanced operations
# --------------------------------------------------

def get_user_followers(user_id, page=1, per_page=20):
    """Get followers of a user with pagination."""
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")

    return user.followers.paginate(page=page, per_page=per_page, error_out=False)

def get_user_following(user_id, page=1, per_page=20):
    """Get users that a user is following with pagination."""
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")

    return user.following.paginate(page=page, per_page=per_page, error_out=False)

def get_mutual_followers(user_id1, user_id2, page=1, per_page=20):
    """Get mutual followers of two users with pagination."""
    user1 = User.query.get(user_id1)
    user2 = User.query.get(user_id2)

    if not user1 or not user2:
        raise ValueError("User not found")

    mutual_followers = User.query.join(UserFollow, User.id == UserFollow.follower_id).\
        filter(UserFollow.followed_id.in_([user_id1, user_id2])).\
        group_by(User.id).\
        having(db.func.count(UserFollow.followed_id) == 2)

    return mutual_followers.paginate(page=page, per_page=per_page, error_out=False)

def get_follow_suggestions(user_id, page=1, per_page=20):
    """Get follow suggestions for a user based on their followings' followings."""
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")

    # Get users that the user's followings are following
    suggestions = User.query.join(UserFollow, User.id == UserFollow.followed_id).\
        filter(UserFollow.follower_id.in_([f.id for f in user.following])).\
        filter(User.id != user_id).\
        filter(~User.followers.any(UserFollow.follower_id == user_id)).\
        group_by(User.id).\
        order_by(db.func.count(UserFollow.follower_id).desc())

    return suggestions.paginate(page=page, per_page=per_page, error_out=False)

def get_follow_stats(user_id):
    """Get follow statistics for a user."""
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")

    return {
        'follower_count': user.followers.count(),
        'following_count': user.following.count()
    }

def check_user_following(follower_id, followed_id):
    """Check if a user is following another user."""
    follower = User.query.get(follower_id)
    followed = User.query.get(followed_id)

    if not follower or not followed:
        raise ValueError("User not found")

    return UserFollow.query.filter_by(follower_id=follower_id, followed_id=followed_id).first() is not None
