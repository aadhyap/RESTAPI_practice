from flask import Flask,jsonify,request


app = Flask(__name__)
tasks = []
task_id = 1

@app.route('/tasks', methods=['Get'])

def get_tasks():
  return jsonify(tasks)


@app.route('/tasks', methods=['POST'])
def add_task():
  global task_id
  new_task = {"id": task_id, "task": request.json['task']}
  tasks.append(new_task)
  task_id += 1

  return jsonify(new_task), 201


@app.route('/tasks/<int:id>', methods=['PUT'])

def update_task(id):
  task = next((item for item in tasks if item['id'] == id), None)
  if task is None:
    return jsonify({"error":"Task not found"}), 404

  task['task'] = request.json['task']
  return jsonify(task)

@app.toute('/tasks/<int:id>', methods=['DELETE'])

def delete_task(id):
  global id
  tasks = [task for task in tasks if task['id'] != id]

  return jsonify({"result":"Task deleted"})

