pong = 0

from flask import Flask, jsonify
import os
import psycopg2

app = Flask(__name__)

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


@app.route('/')
def index():
    global pong 
    pong += 1

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("INSERT INTO pings (ping) VALUES (%s)", (pong,))
    conn.commit()

    return jsonify({"message": pong})



if __name__ == "__main__":
    print("Server started in port 5000")   # printed on startup
    app.run(host="0.0.0.0", port=os.environ["PORT"])
