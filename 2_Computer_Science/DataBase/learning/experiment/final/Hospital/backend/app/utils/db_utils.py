from app import db

def safe_commit():
    """
    Safely commit the current database session.
    """
    try:
        db.session.commit()
        return True, "Operation successful"
    except Exception as e:
        db.session.rollback()
        return False, str(e)
