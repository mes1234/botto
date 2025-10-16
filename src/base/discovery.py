class BottoDiscovery:
    """
    BottoDiscovery is the service discovery mechanism
    It allows processes to discover each other by topic"""

    def __init__(self):
        self.topic_to_ports: dict[str, int] = {}

    def register(self, topic: str, port: int):
        self.topic_to_ports[topic] = port
        pass

    def get_port(self, topic: str) -> int:
        return self.topic_to_ports[topic]
