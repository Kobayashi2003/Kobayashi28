from app import db
from sqlalchemy.exc import IntegrityError

def safe_commit(error_message="Database operation failed"):
    """
    Safely commit the current database session.
    """
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError(error_message)
