import os
import time
import requests
import logging
from flask import Flask, send_file, render_template, make_response, request, redirect

app = Flask(__name__, template_folder="templates")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

@app.before_request
def log_request():
    logging.info(f"Incoming request: {request.method} {request.path} - body={request.get_data(as_text=True)}")

DATA_DIR = "/data"
IMAGE_PATH = f"{DATA_DIR}/current.jpg"
TIMESTAMP_PATH = f"{DATA_DIR}/timestamp.txt"
CACHE_DURATION = 600   # 10 minutes
GRACE_DURATION = 1200  # 20 minutes (10 + grace)

TODO_BACKEND_URL = f"http://{os.environ['BACKEND_HOST']}/todos"

def get_cached_timestamp():
    if not os.path.exists(TIMESTAMP_PATH):
        return None
    try:
        with open(TIMESTAMP_PATH, "r") as f:
            return float(f.read().strip())
    except Exception:
        return None

def write_timestamp(ts):
    with open(TIMESTAMP_PATH, "w") as f:
        f.write(str(ts))

def fetch_new_image():
    # Picsum will redirect and return an image; requests follows redirects by default
    r = requests.get("https://picsum.photos/1200", timeout=10)
    r.raise_for_status()
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(IMAGE_PATH, "wb") as f:
        f.write(r.content)
    write_timestamp(time.time())
    app.logger.info("Fetched new image.")

@app.route("/")
def index():
    """
    Simple HTML page that displays the image.
    Browser requests /image to get the actual bytes.
    """
    # optional: pass timestamp to template to show last refresh
    ts = get_cached_timestamp()
    last_fetched = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts)) if ts else "never"
    # Fetch TODOS safely
    try:
        todo_resp = requests.get(TODO_BACKEND_URL, timeout=5)
        todos = todo_resp.json()
    except Exception:
        app.logger.exception("Failed to fetch todos")
        todos = []

    return render_template("index.html", last_fetched=last_fetched, todos=todos)

@app.route("/image")
def serve_image():
    now = time.time()
    ts = get_cached_timestamp()

    # Case 1: No cached image -> fetch
    if ts is None or not os.path.exists(IMAGE_PATH):
        fetch_new_image()
        ts = get_cached_timestamp()

    age = now - ts if ts else float("inf")

    # Case 2: age < CACHE_DURATION -> serve cached
    if age < CACHE_DURATION:
        image_response = send_file(IMAGE_PATH, mimetype="image/jpeg")

    # Case 3: grace period
    elif age < GRACE_DURATION:
        image_response = send_file(IMAGE_PATH, mimetype="image/jpeg")

    # Case 4: fetch new image
    else:
        try:
            fetch_new_image()
            image_response = send_file(IMAGE_PATH, mimetype="image/jpeg")
        except Exception:
            app.logger.exception("Failed to fetch new image")
            if os.path.exists(IMAGE_PATH):
                image_response = send_file(IMAGE_PATH, mimetype="image/jpeg")
            else:
                return ("Failed to fetch image and no cached image available.", 500)

    return image_response



@app.route("/create-todo", methods=["POST"])
def create_todo():
    text = request.form.get("text", "").strip()
    if not text:
        return redirect("/")  # ignore empty
    if len(text) > 140:
        return redirect("/")  # optional: flash message can be added

    # Send to todo-backend API
    try:
        resp = requests.post(
            TODO_BACKEND_URL,
            json={"text": text},
            timeout=5
        )
        resp.raise_for_status()
    except Exception as e:
        # Optional: log or flash error
        print("Failed to create todo:", e)

    return redirect("/")

@app.route("/update-todo/<int:id>", methods=["POST"])
def update_todo(id):
    done = request.form.get("done") == "true"
    try:
        resp = requests.put(
            f"{TODO_BACKEND_URL}/{id}",
            json={"done": done},
            timeout=5
        )
        resp.raise_for_status()
    except Exception as e:
        print(f"Failed to update todo {id}:", e)
    
    return redirect("/")

if __name__ == "__main__":
    # Use 0.0.0.0 so container ports are reachable
    app.run(host="0.0.0.0", port=os.environ["PORT"])
