from abc import ABC, abstractmethod
import json
from multiprocessing import Process
from typing import Callable, Generic, Tuple, Type, TypeVar
from typing import Self

from src.base.messages import BottoMessage
from src.base.utils import configure_logger
from src.base.discovery import BottoDiscovery
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
        self.subscribe_callbacks: dict[str, Callable[[BottoMessage], None]] = {}
        self.logger = configure_logger(self.name)

    def run(self):
        self.connection_bootstrap()
        self.run_code()
        pass

    @abstractmethod
    def get_topic_type(self) -> type[BottoMessage]:
        """
        Return the type of the topic
        """
        pass

    @abstractmethod
    def run_code(self):
        """
        The main code of the process should be implemented here.
        This method is called when the process is started."""
        pass

    def connection_bootstrap(self):
        """Bootstrap the process"""
        self.communicator = self.communicator_class(
            self.name, self.__port, self.discovery, self.__address
        )
        self.__subscribe()
        pass

    @property
    def topic(self):
        """Return the topic of the process"""
        return self.__publish_topic

    @property
    def port(self):
        """Return the port of the process"""
        return self.__port

    @property
    def address(self):
        """Return the adress of the process"""
        return self.__address

    def _assign_port(self, port: int) -> Self:
        self.__port = port
        return self

    def _assign_adress(self, address: str) -> Self:
        self.__address = address
        return self

    def _add_communicator(self, communicator_class: type[BottoCommunicator]) -> Self:
        self.communicator_class = communicator_class
        return self

    def _add_discovery(self, discovery: BottoDiscovery) -> Self:
        self.discovery = discovery
        return self

    def register_subscribe_callback(
        self,
        publisher_process: "BottoProcess",
        callback: Callable,
    ) -> Self:
        """Register a callback for a topic subscription"""
        topic = publisher_process.topic
        self.subscribe_callbacks[topic] = callback
        return self

    def __subscribe(self):
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
        serialized_message = json.dumps(message.to_dict())  # type: ignore
        self.communicator.publish(serialized_message)
        pass
