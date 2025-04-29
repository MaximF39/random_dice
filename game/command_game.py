from dataclasses import dataclass
from typing import TYPE_CHECKING

from utils.message import Message, MessageLevel

if TYPE_CHECKING:
    from game import Game


@dataclass
class CommandGame:
    game: "Game"

    def __post_init__(self):
        self.Game = self.game.__class__

    def spawn_dice(self, count):
        for _ in range(count):
            if not self.game.dices_manager.get_free_positions():
                self.game.output_buffer_calls.append(Message(
                    MessageLevel.warning,
                    f"Not free space for spawn dice"
                ))
                return
            if not self.game.player_manager.try_buy_dice():
                self.game.output_buffer_calls.append(Message(
                    MessageLevel.warning,
                    f"Not money spawn dice {self.game.player_manager.money} / {self.game.player_manager.dice_cost}"
                ))
                return
            self.game.dices_manager.create_and_set_dice()


    def merge_dice(self, x, y, x2, y2):
        self.game.dices_manager.merge(x, y, x2, y2)

    def level_up_dice(self, dice_id):
        dice = self.game.deck.id_to_dice[dice_id]

        if not self.game.player_manager.try_level_up_dice(dice):
            self.game.output_buffer_calls.append(Message(
                MessageLevel.warning,
                f"Not money level up {self.game.player_manager.money} / {dice.level_cost}"
            ))
            return
        self.game.dices_manager.level_up(dice)


