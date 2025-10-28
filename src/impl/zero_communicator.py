import inspect
import json
import zmq
import threading
from abc import ABC
from typing import Callable, Type, TypeVar, get_type_hints

from src.base.messages import BottoMessage
from src.base.discovery import BottoDiscovery
from src.base.communicator import BottoCommunicator


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

    def subscribe(self, topic: str, callback: Callable[[BottoMessage], None]):
        """
        Subscribe to a topic. Each message on that topic triggers the callback.
        """
        expected_type = self._extract_expected_type(callback)

        port = self.discovery.get_port(topic)
        adress = self.discovery.get_adress(topic)
        sub_socket = self.context.socket(zmq.SUB)

        # Connect subscriber socket to localhost (broadcast)
        sub_socket.connect(f"tcp://{adress}:{port}")
        sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")
        self.logger.info(
            f"ZeroMQ PUB socket subscribed to tcp://{adress}:{port} for '{topic}'"
        )

        def listen():
            while True:
                msg = sub_socket.recv_json()
                try:
                    payload = json.loads(msg)  # type: ignore
                    deserialized_msg = expected_type.from_dict(payload)
                    try:
                        callback(deserialized_msg)
                    except Exception as e_handler:
                        self.logger.error(f"Error in callback handler: {e_handler}")
                except Exception as e_msg:
                    self.logger.error("Failed to decode JSON message: {e_msg}")
                    continue

        thread = threading.Thread(target=listen, daemon=True)
        thread.start()
        self._subscriber_threads.append(thread)

    def _extract_expected_type(
        self, callback: Callable[[BottoMessage], None]
    ) -> Type[BottoMessage]:
        """
        Extract the expected message type from the callback's type hints.
        """
        try:
            hints = get_type_hints(callback)
            sig = inspect.signature(callback)
            params = [
                p
                for p in sig.parameters.values()
                if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
            ]
            if not params:
                raise Exception("Callback must have at least one positional parameter")

            first_param_name = params[0].name
            expected_type: Type[BottoMessage] = hints.get(first_param_name, None)  # type: ignore

            if expected_type is None:
                raise Exception(
                    "Could not determine expected message type from callback"
                )

            return expected_type
        except Exception as e:
            self.logger.error(f"Failed to extract expected type: {e}")
            raise
