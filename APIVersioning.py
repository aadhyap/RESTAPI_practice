from flask import Flask, jsonify, request

app = Flask(__name__)
v1_tasks = []
v2_tasks = []
task_id = 1

@app.route("/v1/tasks", methods=['POST', 'GET'])
def manage_tasks_v1():
  global task_id

  if request.method == 'POST':
    new_task = {'id': task_id, 'task':request.json['task'] }
    v1_tasks.append(new_task)
    task_id +=1
    return jsonify(new_task), 201

  if request.method == 'GET':
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', len(v1_tasks)))
    paginated_tasks = v1_tasks[offset:offset+limit]
    return jsonify(paginated_tasks)


  return jsonify(v1_tasks)




@app.route("/v2/tasks", methods=['POST', 'GET'])
def manage_tasks_v2():
  global task_id

  if request.method=='POST':
    new_task = {'id':task_id, 'task': request.json['task'], 'status': 'pending'}
    v2_tasks.append(new_task)
    task_id += 1
    return jsonify(new_task)
    
  return jsonify(v2_tasks)

