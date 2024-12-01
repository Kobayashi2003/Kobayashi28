from imgserve import create_app
from imgserve.config import Config

def run_flask(config):
    app = create_app(config)
    print("Starting Flask application")
    if __name__ == '__main__':
        # Set debug and use_reloader to True only when run directly
        app.run(host='0.0.0.0', port=config.APP_PORT, debug=True, use_reloader=True)
    else:
        # Use the config settings when run from another script
        app.run(host='0.0.0.0', port=config.APP_PORT, debug=config.DEBUG, use_reloader=config.USE_RELOADER)

if __name__ == '__main__':
    config = Config()
    run_flask(config)