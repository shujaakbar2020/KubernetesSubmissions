import time
import uuid
from datetime import datetime, timezone

from flask import Flask, jsonify
import requests

app = Flask(__name__)

def read_file():
    try:
        with open('/usr/src/randoms.txt', 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return f"Error: The file 'randoms.txt' was not found."

@app.route('/')
def index():
    return jsonify({"message": read_file(), "pingpong": requests.get("http://pingpong-svc:5000/").text})
if __name__ == "__main__":
    print("Server started in port 5000")   # printed on startup
    app.run(host="0.0.0.0", port=5000)
