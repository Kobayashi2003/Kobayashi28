import subprocess

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

if __name__ == '__main__':
    run_redis_server()