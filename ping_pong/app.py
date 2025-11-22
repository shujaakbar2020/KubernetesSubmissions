import time
import uuid
from datetime import datetime, timezone

pong = 0

def get_timestamp():
    # ISO 8601 with milliseconds and Z
    return datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace("+00:00", "Z")

def main():
    stored_string = str(uuid.uuid4())
    print(f"{get_timestamp()}: {stored_string}")

    while True:
        global pong
        pong += 1
        with open('/usr/src/randoms.txt', 'w') as file:
            file.write(f"{get_timestamp()}: {stored_string}. \n Ping / Pongs: {pong}")
        time.sleep(5)

if __name__ == "__main__":
    main()
