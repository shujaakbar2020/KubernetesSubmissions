from flask import Flask
import nats
import asyncio
import json
import requests
import threading
import os

app = Flask(__name__)

# NATS_URL = "nats://localhost:4222"
NATS_URL = os.environ["NATS_URL"]
# NATS_SUBJECT = "todos.events"
NATS_SUBJECT = os.environ["NATS_SUBJECT"]

# Example external chat app (Telegram)
TELEGRAM_BOT_TOKEN = "REPLACE_ME"
TELEGRAM_CHAT_ID = "REPLACE_ME"
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

def send_to_telegram(event):
    text = f"Todo {event['event']}: {event['todo']}"
    requests.post(TELEGRAM_URL, data={"chat_id": TELEGRAM_CHAT_ID, "text": text})


async def nats_listener():
    nc = await nats.connect(servers=[NATS_URL])

    async def handler(msg):
        data = json.loads(msg.data.decode())
        print("Received:", data)
        send_to_telegram(data)

    await nc.subscribe(NATS_SUBJECT, cb=handler)
    print("Broadcaster subscribed to NATS…")

    # keep running
    while True:
        await asyncio.sleep(5)


# Run asyncio loop inside thread so Flask won't block
def start_nats_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(nats_listener())

threading.Thread(target=start_nats_thread, daemon=True).start()


@app.route("/")
def home():
    return "Broadcaster running"


if __name__ == "__main__":
    app.run(port=6000, debug=True)
