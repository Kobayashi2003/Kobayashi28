from flask import Flask, request, jsonify
from celery import Celery
from tasks import long_running_task

app = Flask(__name__)

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@app.route('/start_task', methods=['POST'])
def start_task():
    seconds = request.json.get('seconds', 10)
    task = long_running_task.delay(seconds)
    return jsonify({"task_id": task.id}), 202

@app.route('/task_status/<task_id>')
def task_status(task_id):
    task = long_running_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Task is waiting to start...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'status': 'Task is in progress...'
        }
        if task.info:
            response['result'] = task.info
    else:
        response = {
            'state': task.state,
            'status': 'Task has failed',
            'result': str(task.info)
        }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)