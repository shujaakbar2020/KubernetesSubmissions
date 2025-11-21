import time
import uuid
from datetime import datetime, timezone

from flask import Flask, jsonify

app = Flask(__name__)

pong = 0

@app.route('/')
def index():
    global pong
    pong += 1
    return jsonify({"pong": pong})

if __name__ == "__main__":
    print("Server started in port 5000")   # printed on startup
    app.run(host="0.0.0.0", port=5000)
