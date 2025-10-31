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

if __name__ == '__main__':
    app.run(debug=True)
