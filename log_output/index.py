import time
import uuid
from datetime import datetime, timezone

from flask import Flask, jsonify

app = Flask(__name__)

def get_timestamp():
    # ISO 8601 with milliseconds and Z
    return datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace("+00:00", "Z")

@app.route('/')
def index():
    stored_string = str(uuid.uuid4())
    return jsonify({"message": f"{get_timestamp()}: {stored_string}"})

if __name__ == "__main__":
    print("Server started in port 5000")   # printed on startup
    app.run(host="0.0.0.0", port=5000)
