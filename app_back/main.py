from flask import Flask, jsonify, request # type: ignore
import os
from functools import wraps

app = Flask(__name__)

tasks = {
        'id': 999,
        'title': 'Titulo',
        'completed': False  # Por defecto, la tarea no está completada
    }

API_TOKEN = os.getenv("API_TOKEN")
print(API_TOKEN)

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token != f"Bearer {API_TOKEN}":
            return jsonify({'error': 'Token inválido o no proporcionado'}), 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/tasks', methods=['POST'])
@token_required
def create_task():
    """Crear una nueva tarea"""
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'El campo "title" es obligatorio'}), 400

    new_task = {
        'id': len(tasks) + 1,
        'title': data['title'],
        'completed': data.get('completed', False)  # Por defecto, la tarea no está completada
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

@app.route('/tasks/<int:task_id>', methods=['POST'])
@token_required
def update_task(task_id):
    """Actualizar una tarea existente"""
    data = request.get_json()
    task = next((t for t in tasks if t['id'] == task_id), None)

    if not task:
        return jsonify({'error': 'Tarea no encontrada'}), 404

    if 'title' in data:
        task['title'] = data['title']
    if 'completed' in data:
        task['completed'] = data['completed']

    return jsonify(task)

@app.route('/tasks/delete/<int:task_id>', methods=['POST'])
@token_required
def delete_task(task_id):
    """Eliminar una tarea por su ID"""
    global tasks
    task = next((t for t in tasks if t['id'] == task_id), None)

    if not task:
        return jsonify({'error': 'Tarea no encontrada'}), 404

    tasks = [t for t in tasks if t['id'] != task_id]
    return jsonify({'message': 'Tarea eliminada exitosamente'}), 200

@app.route('/tasks/list', methods=['POST'])
@token_required
def list_tasks():
    """Listar todas las tareas"""
    return jsonify(tasks), 200


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
