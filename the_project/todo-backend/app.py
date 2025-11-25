from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage of todos
todos = [
    {"id": 1, "text": "Learn Javascript"},
    {"id": 2, "text": "Learn React"},
    {"id": 3, "text": "Build a project"},
]

# Helper to generate new ID
def get_next_id():
    if not todos:
        return 1
    return max(todo["id"] for todo in todos) + 1

@app.route("/todos", methods=["GET"])
def get_todos():
    """Return all todos as JSON"""
    return jsonify(todos)

@app.route("/todos", methods=["POST"])
def create_todo():
    """
    Add a new todo.
    Expects JSON: {"text": "my todo"}
    """
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' field"}), 400

    text = data["text"].strip()
    if not text:
        return jsonify({"error": "Todo text cannot be empty"}), 400
    if len(text) > 140:
        return jsonify({"error": "Todo text must be <= 140 characters"}), 400

    todo = {"id": get_next_id(), "text": text}
    todos.append(todo)
    return jsonify(todo), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ["PORT"])
