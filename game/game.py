import time
from typing import Callable, TYPE_CHECKING

from config import Config
from utils.message import Message, MessageLevel
from utils.singleton import Singleton
from utils.trace import trace

if TYPE_CHECKING:
    from player.player_manager import PlayerManager
    from dices.dices_manager import DicesManager
    from mobs.mobs_manager import MobsManager


class Game(Singleton):

    def __init__(self,
                 player_manager: "PlayerManager",
                 mobs_manager: "MobsManager",
                 dices_manager: "DicesManager"):
        self.player_manager = player_manager
        self.dices_manager = dices_manager
        self.deck = self.dices_manager.deck
        self.mobs_manager = mobs_manager
        self.input_buffer_calls: list[Callable] = []
        self.output_buffer_calls: list[Message] = []
        self.start_time = None
        self.history_player_calls: list[str] = []

    def handle_output(self):
        self.output_buffer_calls += [self.dices_manager.get_output(),
                                     self.mobs_manager.get_output(),
                                     self.player_manager.get_output()]

    def game_loop(self):
        self.start_time = time.time()
        self.output_buffer_calls.append(Message(MessageLevel.info,
                                                f"Starting game... First mob will spawn in {Config.INITIAL_WAIT_START} seconds."))
        time.sleep(Config.INITIAL_WAIT_START)
        while self.player_manager.in_game:
            start_time = time.time()
            for call in tuple(self.input_buffer_calls):
                output = call()
                self.input_buffer_calls.remove(call)
                self.history_player_calls.append(str(output))
                if output:
                    self.output_buffer_calls.append(output)

            self.dices_manager.destroy_dices()
            self.mobs_manager.create_mobs()
            damages = self.dices_manager.get_damages()
            self.mobs_manager.update_mobs(damages)

            self.player_manager.get_money_for_destroyed_mobs(self.mobs_manager.get_destroyed())

            self.handle_output()

            if len(self.mobs_manager.mobs) > Config.MOBS_FOR_LOSE:
                self.player_manager.lose()
            end_time = time.time()
            run_time_second = end_time - start_time
            run_time_millisecond = round((end_time - start_time) * 1_000)
            trace(f"Calculate game loop: {run_time_millisecond} milli Second")
            time.sleep(1 / Config.FPS - run_time_second)

        self.output_buffer_calls.append(Message(MessageLevel.info,
                                                f"Finish game max_mob_hp: {self.mobs_manager.mob_hp}"))

    def do_commands(self, commands: list[Callable]):
        self.input_buffer_calls += commands

    def get_output(self):
        output = self.output_buffer_calls[:]
        self.output_buffer_calls.clear()
        return output
