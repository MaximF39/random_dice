import threading
import time


class Communicator:

    def __init__(self, input_, output, game):
        self.input_ = input_
        self.output = output
        self.game = game
        self.running = True
        self.run = True
        self.t_listen = None

    def listen(self):
        self.t_listen = threading.Thread(target=self._listen)
        self.t_listen.start()

    def _listen(self):
        while self.run:
            commands = self.input_.get_input()
            self.game.do_commands(commands)
            messages = self.game.get_output()
            self.output.send_output(messages)
        self.running = False
        messages = self.game.get_output()
        self.output.send_output(messages)

    def finish(self):
        self.run = False
        self.t_listen.join()

    @property
    def is_on(self):
        return self.running

    @property
    def is_off(self):
        return not self.is_on
