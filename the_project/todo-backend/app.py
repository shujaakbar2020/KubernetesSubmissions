from flask import Flask, request, jsonify
import logging
import os
import psycopg2
import psycopg2.extras

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

@app.before_request
def log_request():
    logging.info(f"Incoming request: {request.method} {request.path} - body={request.get_data(as_text=True)}")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")


def get_db_connection():
    """Return a fresh PostgreSQL connection each time."""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def init_db():
    """Create the todos table if it doesn't exist."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id SERIAL PRIMARY KEY,
                text VARCHAR(140) NOT NULL,
                done BOOLEAN DEFAULT FALSE
            );
        """)
        # Attempt to add the column if it doesn't exist (simple migration)
        try:
            cur.execute("ALTER TABLE todos ADD COLUMN IF NOT EXISTS done BOOLEAN DEFAULT FALSE;")
        except Exception:
            conn.rollback()
        else:
            conn.commit()
        cur.close()
        conn.close()
        logging.info("Database initialized.")
    except Exception as e:
        logging.error(f"Error initializing database: {e}")

@app.route('/healthz')
def healthz():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute('SELECT * FROM todos')
        cur.close()
        conn.close()
        return "OK", 200
    except Exception as e:
        return "DB not ready", 500



@app.route("/todos", methods=["GET"])
def get_todos():
    """Return all todos as JSON"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM todos ORDER BY id ASC;")
        todos = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(todos)
    except Exception as e:
        logging.error(f"Error fetching todos: {e}")
        return jsonify({"error": "Database error"}), 500

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
        logging.warning(f"Rejected TODO (too long): {text[:60]}...")
        return jsonify({"error": "Todo text must be <= 140 characters"}), 400

    logging.info(f"Accepted TODO: {text}")
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("INSERT INTO todos (text, done) VALUES (%s, %s) RETURNING id, text, done;", (text, False))
        new_todo = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(new_todo), 201
    except Exception as e:
        logging.error(f"Error creating todo: {e}")
        return jsonify({"error": "Database error"}), 500

@app.route("/todos/<int:id>", methods=["PUT"])
def update_todo(id):
    """
    Update a todo.
    Expects JSON: {"text": "new text", "done": true}
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        # Build update query dynamically
        fields = []
        values = []
        if "text" in data:
            fields.append("text = %s")
            values.append(data["text"])
        if "done" in data:
            fields.append("done = %s")
            values.append(bool(data["done"]))
        
        if not fields:
             return jsonify({"error": "No fields to update"}), 400

        values.append(id)
        query = f"UPDATE todos SET {', '.join(fields)} WHERE id = %s RETURNING id, text, done;"
        
        cur.execute(query, tuple(values))
        updated_todo = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        if updated_todo:
            return jsonify(updated_todo)
        else:
            return jsonify({"error": "Todo not found"}), 404

    except Exception as e:
        logging.error(f"Error updating todo: {e}")
        return jsonify({"error": "Database error"}), 500

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=os.environ["PORT"])
