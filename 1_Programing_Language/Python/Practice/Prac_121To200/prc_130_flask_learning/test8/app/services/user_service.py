from app import db
from app.models import User

def create_user(username, email, password):
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def authenticate_user(username, password):
    user = get_user_by_username(username)
    if user and user.check_password(password):
        return user
    return None

