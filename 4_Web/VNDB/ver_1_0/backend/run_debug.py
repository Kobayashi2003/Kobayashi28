import sys
import time
import signal
import subprocess
import threading
from typing import List


def run_redis_server():
    print("Starting Redis server")
    redis_process = subprocess.Popen([
        'redis-server',
        '--save', '""',  # Disable RDB snapshots
        '--appendonly', 'no',  # Disable AOF persistence
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    def log_redis():
        for line in redis_process.stdout:
            print(f"[REDIS] {line.strip()}")
    
    threading.Thread(target=log_redis, daemon=True).start()
    return redis_process

def run_celery_worker(app_name):
    print(f"Starting Celery worker for {app_name}")
    celery_process = subprocess.Popen([
        'celery', '-A', app_name, 'worker', '--pool=solo', '--loglevel=info',
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    def log_celery():
        for line in celery_process.stdout:
            print(f"[{app_name.upper()} CELERY] {line}", end='')

    threading.Thread(target=log_celery, daemon=True).start()
    return celery_process

def run_flask_debug(app_name: str, host: str, port: int):
    print(f"Starting Flask server for {app_name} on {host}:{port}")
    process = subprocess.Popen([
        'flask', '--app', app_name, 'run', '--debug', '--host', host, '--port', str(port)
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    def log_flask():
        for line in process.stdout:
            print(f"[{app_name.upper()} FLASK] {line}", end='')

    threading.Thread(target=log_flask, daemon=True).start()
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

    start_vndb = True
    start_imgserve = True
    start_userserve = True

    processes = []

    if start_vndb | start_imgserve:
        # Start redis server
        redis_process = run_redis_server()
        processes.append(redis_process)

    if start_vndb:
        # Start vndb celery worker
        vndb_celery_process = run_celery_worker('vndb')
        processes.append(vndb_celery_process)
        # Start vndb flask
        vndb_flask_process = run_flask_debug('vndb', '0.0.0.0', 5000)
        processes.append(vndb_flask_process)
    
    if start_imgserve:
        # Start imgserve celery worker
        imgserve_celery_process = run_celery_worker('imgserve')
        processes.append(imgserve_celery_process)
        # Start imgserve flask
        imgserve_flask_process = run_flask_debug('imgserve', '0.0.0.0', 5001)
        processes.append(imgserve_flask_process)

    if start_userserve:
        # Start userserve flask
        userserve_flask_process = run_flask_debug('userserve', '0.0.0.0', 5002)
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