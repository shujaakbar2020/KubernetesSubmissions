import time
import uuid
from datetime import datetime, timezone

def get_timestamp():
    # ISO 8601 with milliseconds and Z
    return datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace("+00:00", "Z")

def main():
    stored_string = str(uuid.uuid4())
    print(f"{get_timestamp()}: {stored_string}")

    while True:
        time.sleep(5)
        print(f"{get_timestamp()}: {stored_string}")

if __name__ == "__main__":
    main()
