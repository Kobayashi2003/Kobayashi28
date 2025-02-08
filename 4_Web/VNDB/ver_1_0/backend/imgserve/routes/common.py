from flask import jsonify

def execute_task(task, sync=False, *args, **kwargs):
    if sync:
        result = task(*args, **kwargs)
        return jsonify(result)
    else:
        task_result = task.delay(*args, **kwargs)
        return jsonify({"task_id": task_result.id}), 202