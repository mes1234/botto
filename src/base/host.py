from abc import ABC, abstractmethod
from multiprocessing import Process
from typing import Optional, Self
from src.base.communicator import BottoCommunicator
from src.base.discovery import BottoDiscovery
from src.base.process import BottoProcess
import logging


class BottoHost:
    """
    BottoHost is the container starting all applications
    """

    def __init__(self, communicator: type[BottoCommunicator]):

        self.processes: dict[str, BottoProcess] = {}

        self.communicator_class = communicator

        self.base_port = 8000
        self.discovery = BottoDiscovery()
        self.logger = logging.getLogger(__name__)
        pass

    def attach_process(
        self,
        process: BottoProcess,
        port: Optional[int] = None,
        adress: str = "127.0.0.1",
    ) -> Self:
        """
        Attach a process to the host
        """
        self.processes[process.name] = process

        if port is None:
            s = self.base_port + len(self.processes)
        else:
            s = port

        process._assign_port(s)
        process._assign_adress(adress)
        return self

    def start(self):
        """
        Start host
        """
        # Initialize discovery
        for process in self.processes.values():
            self.discovery.register(process.topic, process.port, process.address)

        # Initialize communicator for each process
        for process in self.processes.values():
            process._add_communicator(self.communicator_class)._add_discovery(
                self.discovery
            )

        # Start all processes
        for process in self.processes.values():
            process.start()

        # Wait for all processes to finish
        for process in self.processes.values():
            process.join()
        pass
