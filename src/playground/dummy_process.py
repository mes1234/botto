import time

from src.base.process import BottoProcess


class DummyBottoProcess(BottoProcess[str]):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run_code(self):
        while True:
            self.publish("Hello from DummyProcess")
            time.sleep(10)

    def bootstrap(self):
        pass

    def handle_message(self, message):
        print(f"Received message: {message}")
        pass
