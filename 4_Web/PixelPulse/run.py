import os
from dotenv import load_dotenv
from app import create_app, db
import logging
from logging.handlers import RotatingFileHandler
from flask.cli import FlaskGroup

# Load environment variables
load_dotenv()

# Create the application instance
app = create_app(os.getenv('FLASK_ENV', 'development'))

# Set up logging
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/pixelpulse.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('PixelPulse startup')

def init_db():
    with app.app_context():
        try:
            db.create_all()
            app.logger.info('Database tables created successfully')
        except Exception as e:
            app.logger.error(f'Error creating database tables: {str(e)}')

cli = FlaskGroup(create_app=lambda: create_app(os.getenv('FLASK_ENV', 'development')))

if __name__ == '__main__':
    app.run(
        host='0.0.0.0', 
        debug=os.environ.get('FLASK_DEBUG', 'True').lower() == 'true', 
        port=int(os.environ.get('PORT', 5000))
    )