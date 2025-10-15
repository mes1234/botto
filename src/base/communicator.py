from abc import ABC, abstractmethod

from src.base.utils import configure_logger
from src.base.discovery import BottoDiscovery


class BottoCommunicator(ABC):
    """
    BottoCommunicator is the base class for all communication mechanisms
    """

    def __init__(self, name: str, port: int, discovery: BottoDiscovery):
        self.port = port
        self.name = name
        self.discovery = discovery
        self.discovery.register(name, port)
        self.logger = configure_logger(self.name)
        pass

    @abstractmethod
    def publish(self, message):
        """Publish a message to a topic"""
        pass

    @abstractmethod
    def subscribe(self, topic: str, callback):
        """Subscribe to a topic with a callback"""
        pass


class DebugCommunicator(BottoCommunicator):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def publish(self, message):
        self.logger.info(f"Publishing {message} which is on port {self.port}")

    def subscribe(self, topic: str, callback):
        self.logger.info(
            f"Subscribed to {topic} with callback {callback} which is on port {self.discovery.get_port(topic)}"
        )
