import sys
import signal
import multiprocessing
import subprocess
import importlib
from dotenv import load_dotenv

load_dotenv()

def run_redis_server():
    print("Starting Redis server")
    redis_process = subprocess.Popen([
        'redis-server',
        '--save', '""',  # Disable RDB snapshots
        '--appendonly', 'no',  # Disable AOF persistence
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in redis_process.stdout:
        print(line.decode().strip())
    redis_process.wait()

def run_celery_worker(app_name):
    app_module = importlib.import_module(f'{app_name}')
    create_app = getattr(app_module, 'create_app')
    app = create_app()
    celery = app.celery
    print(f"Starting Celery worker for {app_name}")
    worker = celery.Worker(
        pool='solo',
        loglevel='info',
        quiet=False
    )
    worker.start()

def run_flask(app_name):
    app_module = importlib.import_module(f'{app_name}')
    create_app = getattr(app_module, 'create_app')
    app = create_app()
    config = app.config
    print(f"Starting Flask application for {app_name}")
    app.run(host='0.0.0.0', port=config['APP_PORT'], debug=config['DEBUG'], use_reloader=config['USE_RELOADER'])

def terminate_processes(processes):
    for process in processes:
        if process.is_alive():
            process.terminate()
            process.join()

def main():
    multiprocessing.set_start_method('spawn')
    processes = []

    # Start redis server
    redis_process = multiprocessing.Process(target=run_redis_server)
    redis_process.start()
    processes.append(redis_process)

    # Start vndb celery worker
    vndb_celery_process = multiprocessing.Process(target=run_celery_worker, args=('vndb',))
    vndb_celery_process.start()
    processes.append(vndb_celery_process)

    # Start vndb application
    vndb_flask_process = multiprocessing.Process(target=run_flask, args=('vndb',))
    vndb_flask_process.start()
    processes.append(vndb_flask_process)

    # Start imgserve celery worker
    imgserve_celery_process = multiprocessing.Process(target=run_celery_worker, args=('imgserve',))
    imgserve_celery_process.start()
    processes.append(imgserve_celery_process)

    # Start imgserve application
    imgserve_flask_process = multiprocessing.Process(target=run_flask, args=('imgserve',))
    imgserve_flask_process.start()
    processes.append(imgserve_flask_process)

    # Signal handler for graceful shutdown
    def signal_handler(signum, frame):
        print("\nReceived interrupt signal. Terminating processes...")
        terminate_processes(processes)
        sys.exit(0)

    # Register the signal handler for SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)

    # Wait for processes to complete
    for process in processes:
        process.join()

if __name__ == '__main__':
    main()
