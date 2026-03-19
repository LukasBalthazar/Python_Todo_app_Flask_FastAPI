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

if __name__ == '__main__':
    app.run(debug=True, port=3000)