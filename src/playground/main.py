from src.base.host import BottoHost
from src.playground.dummy_process import DummyBottoProcess


proc1 = DummyBottoProcess("dummy1", "topic1")
proc2 = DummyBottoProcess("dummy2", "topic2")

proc1.register_subscribe_callback(proc2.topic, proc1.handle_message)
proc2.register_subscribe_callback(proc1.topic, proc2.handle_message)

host = BottoHost()

host = host.attach_process(proc1).attach_process(proc2).start()
