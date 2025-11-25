import time, os
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

def read_content_file():
    try:
        with open('information.txt', 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return f"Error: The file 'information.txt' was not found."

@app.route('/')
def index():
    ping_pong_port = os.environ["PORT"]
    ping_pong_url = f"http://pingpong-svc:{ping_pong_port}"
    file_content = read_content_file()
    return jsonify({"message": os.environ["MESSAGE"], "file_content": file_content, "pingpong": requests.get(ping_pong_url).text})

if __name__ == "__main__":
    print("Server started in port 5000")   # printed on startup
    app.run(host="0.0.0.0", port=os.environ["PORT"])
