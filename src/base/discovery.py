from typing import Tuple


class BottoDiscovery:
    """
    BottoDiscovery is the service discovery mechanism
    It allows processes to discover each other by topic"""

    def __init__(self):
        self.topic_to_ports: dict[str, Tuple[int, str]] = {}

    def register(self, topic: str, port: int, address: str):
        self.topic_to_ports[topic] = (port, address)
        pass

    def get_port(self, topic: str) -> int:
        return self.topic_to_ports[topic][0]

    def get_adress(self, topic: str) -> str:
        return self.topic_to_ports[topic][1]
