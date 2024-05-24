from flask import Flask
from flask import request
from flask import jsonify
from models.task import Task


app = Flask(__name__)

tasks = []
task_id_control = 1

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(id=task_id_control, title=data['title'], description=data['description'])
    task_id_control += 1

    tasks.append(new_task)

    return jsonify({'message': 'Nova tarefa criada com sucesso'})


@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_list = [task.to_dict() for task in tasks]

    output = {
            "tasks": task_list,
            "total_tasks": len(task_list)
    }

    return jsonify(output)

tsk = ''
@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    global tsk
    tsk = jsonify({'message': 'Tarefa não encontrada'}), 404

    for task in tasks:
        if task.id == id:
            tsk = jsonify(task.to_dict())
            break

        # return jsonify({'message': 'Tarefa não encontrada'}), 404
        
    return tsk


@app.route('/tasks/<int:id>', methods=['PUT'])

def update_task(id):
    for task in tasks:
        if task.id == id:
            data = request.get_json()
            task.title = data['title']
            task.description = data['description']
            task.completed = data['completed']

            break

        return jsonify({'message': 'Tarefa não encontrada'}), 404

    return jsonify({'message': 'Tarefa atualizada com sucesso'})


@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    for task in tasks:
        if task.id == id:
            tasks.remove(task)
            break

        return jsonify({'message': 'Tarefa não encontrada'}), 404
        
    return jsonify({'message': 'Tarefa deletada com sucesso'})

if __name__ == "__main__":
    app.run(debug=True)