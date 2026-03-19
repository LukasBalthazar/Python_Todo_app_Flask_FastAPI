from flask import Flask, jsonify
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

if __name__ == '__main__':
    app.run(debug=True, port=3000)