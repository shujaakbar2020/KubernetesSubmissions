from flask import Flask, request, jsonify
import nats
import asyncio
import json
import os

app = Flask(__name__)

# NATS_URL = "nats://localhost:4222"
NATS_URL = os.environ["NATS_URL"]
# NATS_SUBJECT = "todos.events"
NATS_SUBJECT = os.environ["NATS_SUBJECT"]

# Start NATS client globally
loop = asyncio.get_event_loop()
nc = loop.run_until_complete(nats.connect(servers=[NATS_URL]))

todos = {}  # Local in-memory DB

def publish_event(event_type, todo):
    message = {
        "event": event_type,
        "todo": todo
    }
    loop.run_until_complete(nc.publish(NATS_SUBJECT, json.dumps(message).encode()))


@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.json
    todo_id = str(len(todos) + 1)
    todo = {"id": todo_id, "task": data["task"], "done": False}
    todos[todo_id] = todo
    
    publish_event("created", todo)
    return jsonify(todo), 201


@app.route("/todos/<todo_id>", methods=["PUT"])
def update_todo(todo_id):
    if todo_id not in todos:
        return jsonify({"error": "Todo not found"}), 404

    data = request.json
    todos[todo_id].update(data)

    publish_event("updated", todos[todo_id])
    return jsonify(todos[todo_id])


@app.route("/todos", methods=["GET"])
def list_todos():
    return jsonify(list(todos.values()))


if __name__ == "__main__":
    app.run(port=5000, debug=True)
