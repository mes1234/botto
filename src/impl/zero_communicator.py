import zmq
import threading
from abc import ABC
from typing import Callable

from src.base.communicator import BottoCommunicator


class BottZeroMqCommunicator(BottoCommunicator):
    """
    ZeroMQ implementation of BottoCommunicator using PUB/SUB pattern on localhost.
    """

    def __init__(self, name: str, port: int, discovery):
        super().__init__(name, port, discovery)
        self.context = zmq.Context()

        # Publisher socket
        self.pub_socket = self.context.socket(zmq.PUB)
        try:
            self.pub_socket.bind(f"tcp://127.0.0.1:{self.port}")
            print(f"ZeroMQ PUB socket bound to tcp://127.0.0.1:{self.port}")
        except zmq.ZMQError as e:
            print(f"Failed to bind ZeroMQ PUB socket: {e}")
            raise

        # Threads for listening
        self._subscriber_threads = []

    def publish(self, message):
        """
        Publish a message under the given topic.
        Format: "topic message"
        """
        self.pub_socket.send_string(f"all {message}")

    def subscribe(self, topic: str, callback: Callable[[str], None]):
        """
        Subscribe to a topic. Each message on that topic triggers the callback.
        """

        # Subscriber socket
        sub_socket = self.context.socket(zmq.SUB)

        # Connect subscriber socket to localhost (broadcast)
        sub_socket.connect(f"tcp://127.0.0.1:{self.discovery.get_port(topic)}")
        sub_socket.setsockopt_string(zmq.SUBSCRIBE, "all")

        def listen():
            while True:
                msg = sub_socket.recv_string()
                callback(msg)

        thread = threading.Thread(target=listen, daemon=True)
        thread.start()
        self._subscriber_threads.append(thread)
