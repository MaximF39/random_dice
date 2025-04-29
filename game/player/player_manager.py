from typing import TYPE_CHECKING

from config import Config
from utils.message import Message, MessageLevel

if TYPE_CHECKING:
    from core.dices.dice import Dice


class PlayerManager:
    def __init__(self):
        self._money = Config.INITIAL_MONEY
        self._dice_cost = Config.INITIAL_DICE_COST
        self.in_game = True
        self.output_buffer = []

    def lose(self):
        self.in_game = False

    def get_output(self):
        return Message(
            MessageLevel.info,
            f"Player money: {self.money}\n" f"Player dice cost: {self._dice_cost}",
        )

    @property
    def money(self):
        return int(self._money)

    @money.setter
    def money(self, value):
        self._money = value

    @property
    def dice_cost(self):
        return int(self._dice_cost)

    def try_buy_dice(self):
        if self._dice_cost > self._money:
            self.output_buffer.append(
                Message(
                    MessageLevel.warning, f"Not money spawn dice {self.money} / {self.dice_cost}"
                )
            )
            return False

        self._money -= self._dice_cost
        self._dice_cost += Config.ADD_DICE_COST
        return True

    def try_level_up_dice(self, dice: "Dice"):
        if dice.level_cost > self._money:
            return False

        self._money -= dice.level_cost
        return True

    def get_money_for_destroyed_mobs(self, mobs_destroyed):
        self._money += sum([mob.money for mob in mobs_destroyed])
