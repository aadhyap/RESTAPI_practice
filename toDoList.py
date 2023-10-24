from flask import Flask,jsonify,request, abort, make_response

from time import time

from functools import wraps


app = Flask(__name__)
tasks = []
task_id = 1

client_times ={}

@app.route('/tasks', methods=['Get'])

def get_tasks():
  #pagination
  offset = int(request.args.get('offset', 0))
  limit = int(request.args.get('limit', len(tasks)))
  paginated_tasks = tasks[offset:offset+limit]
  return jsonify(paginated_tasks)

#implement authentication
def check_auth(username, password):
  return username =="admin" and password=="password"


def requires_auth(f):
  @wraps(f)
  
  def decorated(*args, **kwargs):
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
      abort(401)
    return f(*args, **kwargs)
  return decorated

@app.route('/tasks', methods=['POST', 'PUT', 'DELETE'])
@requires_auth


def rate_limit(f):
  @wraps(f)

  def decorated(*args, **kwargs):
    client_ip = request.remote_addr
    current_time = int(time())
    requests = client_times.get(client_ip, [])

    #Filter requests in the last minute
    requests = [req_time for req_time in requests if current_time - req_time < 60]

    if len(requests) >= 10:
      return make_response(jsonify({"error":"Too many requests"}), 429)

    requests.append(current_time)
    client_times[client_ip] = requests
    return f(*args, **kwargs)
  return decorated

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

@app.route('/tasks/<int:id>', methods=['DELETE'])

def delete_task(id):
    global tasks
    tasks = [task for task in tasks if task['id'] != id]

    return jsonify({"result":"Task deleted"})


