from abc import ABC, abstractmethod
from multiprocessing import Process
from typing import Optional, Self
from src.base.communicator import BottoCommunicator, DebugCommunicator
from src.base.process import BottoProcess


class BottoHost:
    """
    BottoHost is the container starting all applications
    """

    def __init__(self, communicator: type[BottoCommunicator] = DebugCommunicator):

        self.processes: dict[str, BottoProcess] = {}

        self.communicator_class = communicator
        self.communicators: dict[str, BottoCommunicator] = {}

        self.base_port = 8000
        pass

    def attach_process(self, process: BottoProcess, port: Optional[int] = None) -> Self:
        """
        Attach a process to the host
        """
        self.processes[process.name] = process

        if port is None:
            s = self.base_port + len(self.processes)
        else:
            s = port

        process.assign_port(s)
        return self

    def start(self):
        """
        Start host
        """

        # Initialize communicator for each process
        for process in self.processes.values():
            self.communicators[process.topic] = self.communicator_class(
                process.topic,
                process.port,
            )
            process.add_communicator(self.communicators[process.topic])

        # Start all processes
        for process in self.processes.values():
            process.connection_bootstrap()
            process.bootstrap()
            process.start()

        # Wait for all processes to finish
        for process in self.processes.values():
            process.join()
        pass
