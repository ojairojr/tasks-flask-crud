from flask import Flask, jsonify, request
from models.task import Task

app = Flask(__name__)

tasks = []
task_id_counter = 1

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_counter
    data = request.get_json()
    new_task = Task(id=task_id_counter, title=data['title'], description=data.get('description', ''))
    task_id_counter += 1
    tasks.append(new_task)
    return jsonify(new_task.to_dict()), 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_list = [task.to_dict() for task in tasks]
    output = {
        "tasks": task_list,
        "total": len(task_list)
    }
    return jsonify(output)

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    for t in tasks:
        if t.id == task_id:
            return jsonify(t.to_dict())
    return jsonify({"message": "Task not found"}), 404

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task=None
    for t in tasks:
        if t.id == task_id:
            task = t
            break

    if task is None:
        return jsonify({"message": "Task not found"}), 404
    
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)

    return jsonify({"message": "Task updated", "task": task.to_dict()})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = None
    for t in tasks:
        if t.id == task_id:
            task = t
            break
    if task is None:
        return jsonify({"message": "Task not found"}), 404
    
    tasks.remove(task)
    return jsonify({"message": "Task deleted"})

if __name__ == '__main__':
    app.run(debug=True)
