import zmq
import threading
from abc import ABC
from typing import Callable, Type, TypeVar

from src.base.discovery import BottoDiscovery
from src.base.communicator import BottoCommunicator

T = TypeVar("T")


class BottZeroMqCommunicator(BottoCommunicator):
    """
    ZeroMQ implementation of BottoCommunicator using PUB/SUB pattern.
    """

    def __init__(
        self,
        name: str,
        port: int,
        discovery: BottoDiscovery,
        address: str = "127.0.0.1",
    ):
        super().__init__(name, port, discovery, address)
        self.context = zmq.Context()

        # Publisher socket
        self.pub_socket = self.context.socket(zmq.PUB)
        try:
            self.pub_socket.bind(f"tcp://{self.address}:{self.port}")
            self.logger.info(
                f"ZeroMQ PUB socket bound to tcp://127.0.0.1:{self.port} for '{self.name}'"
            )
        except zmq.ZMQError as e:
            self.logger.error(f"Failed to bind ZeroMQ PUB socket: {e}")
            raise

        # Threads for listening
        self._subscriber_threads = []

    def publish(self, message):
        """
        Publish a message under the given topic.
        Format: "topic message"
        """
        self.pub_socket.send_json(message)

    def subscribe(self, topic: str, callback: Callable[[T], None], expected_type: Type):
        """
        Subscribe to a topic. Each message on that topic triggers the callback.
        """
        port = self.discovery.get_port(topic)
        adress = self.discovery.get_adress(topic)
        sub_socket = self.context.socket(zmq.SUB)

        # Connect subscriber socket to localhost (broadcast)
        sub_socket.connect(f"tcp://{adress}:{port}")
        sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")
        self.logger.info(
            f"ZeroMQ PUB socket subscribed to tcp://{adress}:{port} for '{self.name}'"
        )

        def listen():
            while True:
                msg = sub_socket.recv_json()
                if expected_type is not None and not isinstance(msg, expected_type):
                    self.logger.warning(
                        f"Received message of unexpected type: {type(msg)}"
                    )
                    continue
                callback(msg)  # type: ignore

        thread = threading.Thread(target=listen, daemon=True)
        thread.start()
        self._subscriber_threads.append(thread)
