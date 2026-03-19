from flask import Flask, jsonify, request
from flask_cors import CORS

app =  Flask(__name__)
CORS(app)

todos = []
todo_id_counter = 1

@app.route('/')
def home():
    return 'Todo API is running'

@app.route('/api/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/api/todos', methods=['POST'])
def add_todo():
    global todo_id_counter

    data = request.get_json()

    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    new_todo  = {
        'id': todo_id_counter,
        'title': data['title'],
        'completed': data.get('completed', False)
    }

    todos.append(new_todo)
    todo_id_counter += 1

    return jsonify(new_todo), 201

@app.route('/api/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = next((t for t in todos if t['id'] == todo_id), None)

    if todo is None:
        return({'error': 'Todo not found'}), 404
    
    return jsonify(todo)

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = next((t for t in todos if t['id'] == todo_id), None)

    if todo is None:
        return jsonify({'error': 'Todo not found '}), 404
    
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if 'title' in data:
        todo['title'] = data['title']

    if 'completed' in data:
        todo['completed'] = data['completed']

    return jsonify(todo)

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos

    todo = next((t for t in todos if t['id'] == todo_id), None)

    if todo is None:
        return jsonify({'error': 'Todo not found'}), 404
    
    todos = [t for t in todos if t['id'] != todo_id]

    return jsonify({'message': 'Todo deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=3000)