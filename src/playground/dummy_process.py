import time

from src.base.process import BottoProcess


class DummyBottoProcess(BottoProcess[str]):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run_code(self):
        while True:
            self.publish(f"Hello from DummyProcess { self.name} ")
            self.logger.debug("Published message")
            time.sleep(10)

    def bootstrap(self):
        pass

    def handle_message(self, message):
        self.logger.info(f"Received message: {message}")
        pass
