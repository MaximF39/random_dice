import sys
import threading
from functools import partial
from io import StringIO
from typing import Callable

import select

from utils.logger import logger
from command_game import CommandGame


class InputCLI:
    def __init__(self, game_commands: "CommandGame", start=False):
        self.input_buffer_calls = []
        self.game_commands = game_commands
        self.t_input = True
        if start:
            self.start()

    def start(self):
        self.input_thread = threading.Thread(target=self._input)
        self.input_thread.start()

    def finish(self):
        self.t_input = False
        # self.input_thread.join()

    def _input(self):
        while self.t_input:
            try:
                user_input = input("Commands:\n"
                                   "1) Create dice. Arg: count\n"
                                   "2) Merge dice. Arg: x y\n")
                split = user_input.split(" ", maxsplit=1)
                if len(split) > 1:
                    command_id, args = split
                    command_id = int(command_id)
                    args = args.split(" ")
                else:
                    logger.warning(f"Incorrect input {split}")
                    continue
                if command_id == 1:
                    count = int(args[0])
                    logger.info(f"Count add dice: {count}")
                    command_call = partial(self.game_commands.spawn_dice, count)
                elif command_id == 2:
                    x, y, x2, y2 = (int(v) for v in args)
                    logger.info(f"Merge: {x} {y} -> {x2} {y2}")
                    command_call = partial(self.game_commands.merge_dice, x, y, x2, y2)
                else:
                    continue
                self.input_buffer_calls.append(command_call)
            except ValueError:
                logger.info("Invalid input. Please enter a number.")

    def get_input(self) -> list[Callable]:
        calls = self.input_buffer_calls[:]  # copy
        self.input_buffer_calls.clear()
        return calls
