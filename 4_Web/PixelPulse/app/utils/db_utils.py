from app import db
from sqlalchemy.exc import IntegrityError

def safe_commit(error_message="Database operation failed"):
    """
    Safely commit the current database session.
    
    Args:
        error_message (str): The error message to raise if the commit fails.
    
    Raises:
        ValueError: If the database commit fails.
    """
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError(error_message)

