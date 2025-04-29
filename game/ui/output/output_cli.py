import time

from utils.message import Message


class OutputCLI:

    def __init__(self, start=False):
        if start:
            self.start()

    def send_output(self, messages: list[Message]):
        for message in messages:
            message.print()
        time.sleep(1)

    def start(self):
        ...
