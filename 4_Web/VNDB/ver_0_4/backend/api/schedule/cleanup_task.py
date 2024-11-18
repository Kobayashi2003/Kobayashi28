from datetime import datetime
from flask import current_app

from api import scheduled_task
from ..database import cleanup, cleanup_all

@scheduled_task(trigger='cron', id='cleanup_task', hour=0, minute=0)
def cleanup_task():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_app.logger.info(f"Starting database cleanup at {current_time}")

    try:
        result = cleanup_all()
        total_removed = sum(result.values())

        success_message = f"Database cleanup completed successfully. Total removed: {total_removed}"
        current_app.logger.info(success_message)
        print(success_message)

        return {
            'status': 'SUCCESS',
            'result': result,
            'total_removed': total_removed
        }
    except ValueError as e:
        error_message = f"Invalid type during cleanup: {str(e)}"
        current_app.logger.error(error_message)
        print(error_message)
        raise
    except Exception as e:
        error_message = f"Database cleanup failed: {str(e)}"
        current_app.logger.error(error_message)
        print(error_message)
        raise
