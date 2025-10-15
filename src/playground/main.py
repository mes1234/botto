from src.base.host import BottoHost
from src.impl.zero_communicator import BottZeroMqCommunicator
from src.playground.dummy_process import DummyBottoProcess

import src.base.config as config

config.LOG_LEVEL = "INFO"

proc1 = DummyBottoProcess("dummy1", "topic1")
proc2 = DummyBottoProcess("dummy2", "topic2")
proc3 = DummyBottoProcess("dummy3", "topic3")

proc1.register_subscribe_callback(proc2.topic, proc1.handle_message)
proc2.register_subscribe_callback(proc1.topic, proc2.handle_message)
proc3.register_subscribe_callback(proc1.topic, proc3.handle_message)

host = BottoHost(BottZeroMqCommunicator)

host = host.attach_process(proc1).attach_process(proc2).attach_process(proc3).start()
