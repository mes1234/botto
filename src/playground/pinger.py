import zmq
import time

# -------------------------
# Configuration
# -------------------------
PORT = 8001
TOPIC = "all"

# -------------------------
# ZeroMQ setup
# -------------------------
context = zmq.Context()
publisher = context.socket(zmq.PUB)
publisher.bind(f"tcp://127.0.0.1:{PORT}")

print(f"Publisher started on port {PORT}. Sending '{TOPIC}' messages...")

# Small delay to allow subscribers to connect (important in PUB/SUB)
time.sleep(1)

# -------------------------
# Publish loop
# -------------------------
count = 0
while True:
    message = f"{TOPIC} ping {count}"
    publisher.send_string(message)
    print(f"Sent: {message}")
    count += 1
    time.sleep(1)
