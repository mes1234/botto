import zmq
import threading
import matplotlib.pyplot as plt
from collections import defaultdict, deque
import time

import zmq

print(zmq.zmq_version())
print(zmq.pyzmq_version())


# -----------------------------
# Configuration
# -----------------------------
ZMQ_ADDRESS = "tcp://127.0.0.1:8001"  # Change to your PUB address
UPDATE_INTERVAL = 0.5  # Seconds for chart refresh

# -----------------------------
# Data storage
# -----------------------------
message_counts = defaultdict(
    lambda: deque(maxlen=50)
)  # Store timestamps for recent messages


# -----------------------------
# Subscriber thread
# -----------------------------
def subscriber():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(ZMQ_ADDRESS)

    socket.setsockopt_string(zmq.SUBSCRIBE, "all")

    while True:
        msg = socket.recv_string()
        message_counts[msg].append(time.time())


threading.Thread(target=subscriber, daemon=True).start()

# -----------------------------
# Visualization
# -----------------------------
plt.ion()
fig, ax = plt.subplots()

while True:
    ax.clear()
    now = time.time()

    for topic, timestamps in message_counts.items():
        # Calculate messages per second over the last UPDATE_INTERVAL
        counts = [ts for ts in timestamps if now - ts <= 5]  # last 5 seconds
        ax.plot([ts - now for ts in counts], [1] * len(counts), "o", label=topic)

    ax.set_xlim(-5, 0)
    ax.set_ylim(0, 2)
    ax.set_xlabel("Seconds ago")
    ax.set_ylabel("Messages")
    ax.set_title("Real-time ZeroMQ PUB/SUB Traffic")
    ax.legend()
    plt.pause(UPDATE_INTERVAL)
