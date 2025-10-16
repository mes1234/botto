from abc import ABC, abstractmethod

from src.base.utils import configure_logger
from src.base.discovery import BottoDiscovery


class BottoCommunicator(ABC):
    """
    BottoCommunicator is the base class for all communication mechanisms
    """

    def __init__(
        self,
        name: str,
        port: int,
        discovery: BottoDiscovery,
        address: str,
    ):
        self.port = port
        self.address = address
        self.name = name
        self.discovery = discovery
        self.discovery.register(name, port, address)
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
