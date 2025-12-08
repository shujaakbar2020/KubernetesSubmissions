import time, os
import uuid
from datetime import datetime, timezone

from flask import Flask, jsonify
import requests

app = Flask(__name__)

PINGPONG_URL=os.environ["PINGPONG_URL"]
GREETER_URL=os.environ["GREETER_URL"]


@app.route("/healthz")
def healthz():
    try:
        res = requests.get(PINGPONG_URL, timeout=1)
        if res.status_code == 200:
            return "OK", 200
        return "Pingpong not available", 500
    except Exception:
        return "Pingpong not reachable", 500

def read_content_file():
    try:
        with open('serverconfig.txt', 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return f"Error: The file 'serverconfig.txt' was not found."

@app.route('/')
def index():
    # ping_pong_port = os.environ["PORT"]
    # ping_pong_url = f"http://pingpong-svc:{ping_pong_port}"
    file_content = read_content_file()
    return jsonify({"message": os.environ["MESSAGE"], "pingpong": requests.get(PINGPONG_URL).text, "greetings": requests.get(GREETER_URL).text})

if __name__ == "__main__":
    print("Server started in port 5000")   # printed on startup
    app.run(host="0.0.0.0", port=os.environ["PORT"])
