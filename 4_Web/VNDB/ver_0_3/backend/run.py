import multiprocessing
import signal
import sys
import subprocess
import os
import logging
import shutil
from flask import request
from api import create_app
from api.celery_app import create_celery_app
from api.config import Config

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(logs_dir, exist_ok=True)

def setup_logger(name, log_file, level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)

    return logger

def run_celery_worker(config):
    app = create_app(config)
    celery_app = create_celery_app(app)
    logger = setup_logger('celery', os.path.join(logs_dir, 'celery.log'))

    logger.info("Starting Celery worker")
    worker = celery_app.Worker(
        pool='solo',
        loglevel='info',
        logfile=os.path.join(logs_dir, 'celery.log'),
        quiet=True
    )
    worker.start()

def run_redis_server():
    logger = setup_logger('redis', os.path.join(logs_dir, 'redis.log'))

    logger.info("Starting Redis server")
    with open(os.path.join(logs_dir, 'redis.log'), 'a') as redis_log:
        redis_process = subprocess.Popen([
            'redis-server',
            '--save', '""',  # Disable RDB snapshots
            '--appendonly', 'no',  # Disable AOF persistence
            '--logfile', '/dev/stdout'
        ], stdout=redis_log, stderr=subprocess.STDOUT)
        redis_process.wait()

def terminate_processes(processes):
    for process in processes:
        if process.is_alive():
            process.terminate()
            process.join()

def setup_flask_logging(app, log_file):
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    
    # Remove default handlers
    app.logger.handlers = []
    
    # Add our custom handler
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)

    # Log all requests
    @app.before_request
    def log_request_info():
        app.logger.info('Request: %s %s %s %s', request.remote_addr, request.method, request.url, dict(request.args))

    # Log all responses
    @app.after_request
    def log_response_info(response):
        app.logger.info('Response: %s %s %s %s', request.remote_addr, request.method, request.url, response.status)
        return response

def run_flask(config):
    app = create_app(config)
    setup_flask_logging(app, os.path.join(logs_dir, 'flask.log'))
    app.logger.info("Starting Flask application")
    app.run(host='0.0.0.0', port=config.APP_PORT, debug=config.DEBUG, use_reloader=False)

def delete_pycache_folders():
    for root, dirs, files in os.walk('.'):
        for dir in dirs:
            if dir == '__pycache__':
                pycache_path = os.path.join(root, dir)
                shutil.rmtree(pycache_path)
                print(f"Deleted __pycache__ folder: {pycache_path}")

def main():
    multiprocessing.set_start_method('spawn')
    processes = []
    config = Config()

    # Start Redis server
    redis_process = multiprocessing.Process(target=run_redis_server)
    redis_process.start()
    processes.append(redis_process)

    # Start Celery worker
    celery_process = multiprocessing.Process(target=run_celery_worker, args=(config,))
    celery_process.start()
    processes.append(celery_process)

    # Start Flask in a separate process
    # flask_process = multiprocessing.Process(target=run_flask, args=(config,))
    # flask_process.start()
    # processes.append(flask_process)

    def signal_handler(signum, frame):
        print("\nReceived interrupt signal. Terminating processes...")
        terminate_processes(processes)
        delete_pycache_folders()
        sys.exit(0)

    # Register the signal handler for SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)

    # Wait for processes to complete
    for process in processes:
        process.join()

    # Delete __pycache__ folders after all processes have completed
    delete_pycache_folders()

if __name__ == '__main__':
    main()