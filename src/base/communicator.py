from abc import ABC, abstractmethod


class BottoCommunicator(ABC):
    """
    BottoCommunicator is the base class for all communication mechanisms
    """

    def __init__(self, name: str, port: int):
        self.port = port
        self.name = name

    @abstractmethod
    def publish(self, topic: str, message):
        """Publish a message to a topic"""
        pass

    @abstractmethod
    def subscribe(self, topic: str, callback):
        """Subscribe to a topic with a callback"""
        pass


class DebugCommunicator(BottoCommunicator):

    def __init__(self, name: str, port: int):
        super().__init__(name, port)

    def publish(self, topic: str, message):
        print(f"Publishing to {topic}: {message}")

    def subscribe(self, topic: str, callback):
        print(f"Subscribed to {topic} with callback {callback}")
