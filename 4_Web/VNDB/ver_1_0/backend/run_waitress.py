import sys
import signal
import multiprocessing
import subprocess
import importlib
from dotenv import load_dotenv
from waitress import serve

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

def run_waitress(app_name):
    app_module = importlib.import_module(f'{app_name}')
    create_app = getattr(app_module, 'create_app')
    app = create_app()
    config = app.config
    print(f"Starting Waitress server for {app_name} on {config['APP_HOST']}:{config['APP_PORT']}")
    serve(
        app, 
        host=config['APP_HOST'], 
        port=config['APP_PORT'],
        threads=100,
        connection_limit=1000,
        channel_timeout=60,
        cleanup_interval=30,
        asyncore_loop_timeout=60,
        send_bytes=4096,
    )

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

    # Start vndb application with Waitress
    vndb_waitress_process = multiprocessing.Process(target=run_waitress, args=('vndb',))
    vndb_waitress_process.start()
    processes.append(vndb_waitress_process)

    # Start imgserve celery worker
    imgserve_celery_process = multiprocessing.Process(target=run_celery_worker, args=('imgserve',))
    imgserve_celery_process.start()
    processes.append(imgserve_celery_process)

    # Start imgserve application with Waitress
    imgserve_waitress_process = multiprocessing.Process(target=run_waitress, args=('imgserve',))
    imgserve_waitress_process.start()
    processes.append(imgserve_waitress_process)

    # Start userserve application with Waitress
    userserve_waitress_process = multiprocessing.Process(target=run_waitress, args=('userserve',))
    userserve_waitress_process.start()
    processes.append(userserve_waitress_process)

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

