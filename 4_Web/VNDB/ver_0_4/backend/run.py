import os
import sys
import shutil
import signal
import multiprocessing
from api.config import Config
from run_flask import run_flask
from run_celery import run_celery_worker
from run_redis import run_redis_server
from clean import delete_empty_folders, delete_pycache_folders

# Function to terminate all processes
def terminate_processes(processes):
    for process in processes:
        if process.is_alive():
            process.terminate()
            process.join()

# Main function to run the application
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

    # Start Flask in the main process
    flask_process = multiprocessing.Process(target=run_flask, args=(config,))
    flask_process.start()
    processes.append(flask_process)

    # Signal handler for graceful shutdown
    def signal_handler(signum, frame):
        print("\nReceived interrupt signal. Terminating processes...")
        terminate_processes(processes)
        delete_pycache_folders()
        delete_empty_folders()
        sys.exit(0)

    # Register the signal handler for SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)

    # Wait for processes to complete
    for process in processes:
        process.join()

    # Delete __pycache__ folders after all processes have completed
    delete_pycache_folders()
    delete_empty_folders()

if __name__ == '__main__':
    main()