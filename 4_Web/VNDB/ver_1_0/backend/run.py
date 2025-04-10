import os
import sys
import time
import signal
import subprocess
import threading
import argparse
import logging
from logging.handlers import RotatingFileHandler
from typing import List

os.makedirs('logs', exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler(
    'logs/run.log', 
    maxBytes=1024 * 1024 * 5, 
    # backupCount=5
)
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

def run_redis_server():
    print("Starting Redis server")
    redis_process = subprocess.Popen([
        'redis-server',
        '--save', '""',  # Disable RDB snapshots
        '--appendonly', 'no',  # Disable AOF persistence
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    def log_redis():
        for line in redis_process.stdout:
            logger.info(f"[REDIS] {line.strip()}")
            print(f"[REDIS] {line.strip()}")
    
    threading.Thread(target=log_redis, daemon=True).start()
    return redis_process

def run_celery_worker(app_name):
    print(f"Starting Celery worker for {app_name}")
    celery_process = subprocess.Popen([
        'python', '-c',
        f"from {app_name} import create_app;"
        f"app = create_app(enable_scheduler=False);"
        f"config = app.config;"
        f"celery = app.celery;"
        f"celery.Worker(pool='solo', loglevel='info', quiet=False).start();"
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    def log_celery():
        for line in celery_process.stdout:
            logger.info(f"[{app_name.upper()} CELERY] {line}")
            print(f"[{app_name.upper()} CELERY] {line}", end='')

    threading.Thread(target=log_celery, daemon=True).start()
    return celery_process

def run_flower(app_name: str):
    print(f"Starting Flower for {app_name}")
    import celery_worker
    config = getattr(celery_worker, f"{app_name}_config")
    broker = config['CELERY_BROKER_URL']
    port = config['FLOWER_PORT']
    flower_process = subprocess.Popen([
        'celery', f'--broker={broker}', 'flower', f"--port={port}"
        # 'celery', '-A', f"celery_worker:{app_name}_celery", 'flower', f"--port={port}"
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    def log_flower():
        for line in flower_process.stdout:
            logger.info(f"[{app_name.upper()} FLOWER] {line}")
            print(f"[{app_name.upper()} FLOWER] {line}", end='')

    threading.Thread(target=log_flower, daemon=True).start()
    return flower_process

def run_flask(app_name: str):
    print(f"Starting Flask server for {app_name}")
    process = subprocess.Popen([
        'python', '-c',
        f"from {app_name} import create_app;"
        f"app = create_app();"
        f"config = app.config;"
        f"app.run(host=config['APP_HOST'],"
        f"port=config['APP_PORT'],"
        f"debug=config['DEBUG'],"
        f"use_reloader=config['USE_RELOADER']);"
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    def log_flask():
        for line in process.stdout:
            logger.info(f"[{app_name.upper()} FLASK] {line}")
            print(f"[{app_name.upper()} FLASK] {line}", end='')

    threading.Thread(target=log_flask, daemon=True).start()
    return process

def run_flask_waitress(app_name: str):
    print(f"Starting Waitress server for {app_name}")
    process = subprocess.Popen([
        'python', '-c', 
        f"from waitress import serve;"
        f"import {app_name};"
        f"app = {app_name}.create_app();"
        f"config = app.config;"
        f"serve(app, host=config['APP_HOST'], port=config['APP_PORT']);"
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    def log_waitress():
        for line in process.stdout:
            logger.info(f"[{app_name.upper()} WAITRESS] {line}")
            print(f"[{app_name.upper()} WAITRESS] {line}", end='')

    threading.Thread(target=log_waitress, daemon=True).start()
    return process


def terminate_processes(processes: List[subprocess.Popen]):
    """Gracefully terminate debug processes"""
    for proc in processes:
        try:
            if proc.poll() is None:
                proc.terminate()
                proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()
        except Exception as e:
            print(f"Error terminating process: {str(e)}")

def main():

    parser = argparse.ArgumentParser(description='Run debug servers with options')
    parser.add_argument('--waitress', action='store_true', 
                        help='Use Waitress WSGI server instead of Flask development server')
    args = parser.parse_args()

    processes = []

    # Start redis server
    redis_process = run_redis_server()
    processes.append(redis_process)


    # Start vndb celery worker
    vndb_celery_process = run_celery_worker('vndb')
    processes.append(vndb_celery_process)

    # Start vndb flower
    vndb_flower_process = run_flower('vndb')
    processes.append(vndb_flower_process)

    # Start vndb flask
    if args.waitress:
        vndb_flask_process = run_flask_waitress('vndb')
    else:
        vndb_flask_process = run_flask('vndb')
    processes.append(vndb_flask_process)
    

    # Start imgserve celery worker
    imgserve_celery_process = run_celery_worker('imgserve')
    processes.append(imgserve_celery_process)

    # Start imgserve flower
    imgserve_flower_process = run_flower('imgserve')
    processes.append(imgserve_flower_process)

    # Start imgserve flask
    if args.waitress:
        imgserve_flask_process = run_flask_waitress('imgserve')
    else:
        imgserve_flask_process = run_flask('imgserve')
    processes.append(imgserve_flask_process)


    # Start userserve flask
    if args.waitress:
        userserve_flask_process = run_flask_waitress('userserve')
    else:
        userserve_flask_process = run_flask('userserve')
    processes.append(userserve_flask_process)


    def signal_handler(signum, frame):
        print("\nReceived interrupt signal. Terminating processes...")
        terminate_processes(processes)
        sys.exit(0)

    if sys.platform == 'win32':
        signal.signal(signal.SIGBREAK, signal_handler)
    else:
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)

if __name__ == '__main__':
    main()