from abc import ABC, abstractmethod
import json
from multiprocessing import Process
from typing import Generic, TypeVar
from typing import Self

from src.base.communicator import BottoCommunicator

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

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def bootstrap(self):
        pass

    def connection_bootstrap(self):
        """Bootstrap the process"""
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

    def add_communicator(self, botto_communicator: BottoCommunicator) -> Self:
        self.communicator = botto_communicator
        return self

    def register_subscribe_callback(self, topic: str, callback: callable) -> Self:  # type: ignore
        # TODO validate if callback is of type which it subscribes to
        self.subscribe_callbacks[topic] = callback
        return self

    def subscribe(self):
        # TODO check if communicator is set
        for topic, callback in self.subscribe_callbacks.items():
            self.communicator.subscribe(topic, callback)
        return

    def publish(self, message: T):
        # TODO check if communicator is set
        #  and if message is of correct type
        serialized_message = json.dumps(message)
        self.communicator.publish(self.__publish_topic, serialized_message)
        pass
