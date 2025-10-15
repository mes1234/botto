from abc import ABC, abstractmethod
import json
from multiprocessing import Process
from typing import Generic, TypeVar
from typing import Self
import logging

from src.base.utils import configure_logger
from src.base.discovery import BottoDiscovery
from src.base.communicator import BottoCommunicator, DebugCommunicator

T = TypeVar("T")


class BottoProcess(Generic[T], ABC, Process):
    """
    BottoProcess is the base class for all processes running in BottoHost
    """

    def __init__(self, name: str, publish_topic: str):
        super().__init__()
        self.name = name
        self.__publish_topic = publish_topic
        self.subscribe_callbacks: dict[str, callable] = {}  # type: ignore
        self.logger = configure_logger(self.name)

    def run(self):
        self.connection_bootstrap()
        self.run_code()
        pass

    @abstractmethod
    def run_code(self):
        pass

    def connection_bootstrap(self):
        """Bootstrap the process"""
        self.communicator = self.communicator_class(
            self.name,
            self.__port,
            self.discovery,
        )
        self.subscribe()
        pass

    @property
    def topic(self):
        """Return the topic of the process"""
        return self.__publish_topic

    @property
    def port(self):
        """Return the port of the process"""
        return self.__port

    def assign_port(self, port: int) -> Self:
        self.__port = port
        return self

    def add_communicator(
        self, communicator_class: type[BottoCommunicator] = DebugCommunicator
    ) -> Self:
        self.communicator_class = communicator_class
        return self

    def add_discovery(self, discovery: BottoDiscovery) -> Self:
        self.discovery = discovery
        return self

    def register_subscribe_callback(self, topic: str, callback: callable) -> Self:  # type: ignore
        # TODO validate if callback is of type which it subscribes to
        self.subscribe_callbacks[topic] = callback
        return self

    def subscribe(self):

        if not hasattr(self, "communicator"):
            raise Exception("Communicator not set")

        for topic, callback in self.subscribe_callbacks.items():
            self.communicator.subscribe(topic, callback)
        return

    def publish(self, message: T):

        if not hasattr(self, "communicator"):
            raise Exception("Communicator not set")

        self.logger.debug(
            f"Process {self.name} publishing message to topic {self.__publish_topic}"
        )
        serialized_message = json.dumps(message)
        self.communicator.publish(serialized_message)
        pass
