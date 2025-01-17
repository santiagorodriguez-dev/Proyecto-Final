from flask import Flask, jsonify
import os

app = Flask(__name__)

tasks = []

@app.route('/tasks', methods=['POST'])
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
def delete_task(task_id):
    """Eliminar una tarea por su ID"""
    global tasks
    task = next((t for t in tasks if t['id'] == task_id), None)

    if not task:
        return jsonify({'error': 'Tarea no encontrada'}), 404

    tasks = [t for t in tasks if t['id'] != task_id]
    return jsonify({'message': 'Tarea eliminada exitosamente'}), 200

@app.route('/tasks/list', methods=['POST'])
def list_tasks():
    """Listar todas las tareas"""
    return jsonify(tasks), 200


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
