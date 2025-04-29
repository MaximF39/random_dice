import random
from typing import TYPE_CHECKING, Union

from config import Config
from prettytable import PrettyTable
from utils.message import Message, MessageLevel
from utils.singleton import Singleton
from utils.trace import trace

if TYPE_CHECKING:
    from core.dices.deck import Deck
    from core.dices.dice import Dice


class DicesManager(Singleton):
    @classmethod
    def get_instance(cls):
        return cls._instance

    def __init__(self, deck: "Deck", y=Config.BOARD_WIDTH, x=Config.BOARD_HEIGHT):
        self.map_x = x
        self.map_y = y
        self.dices: list[list["Dice" | None]] = [[None for _ in range(y)] for _ in range(x)]
        self.deck = deck

    def get_flat_dices(self) -> list[Union["Dice", None]]:
        return [dice for row in self.dices for dice in row]

    def get_damages(self) -> list[int]:
        damages = []
        for dice in self.get_flat_dices():
            if dice is None:
                continue
            damages.append(dice.get_damage())
        return damages

    def merge(self, x, y, x2, y2):
        """self.dices[y][x] -> self.dices[y2][x2]
        kill dice1, up dice2
        """
        try:
            dice1 = self.dices[y][x]
            dice2 = self.dices[y2][x2]
        except IndexError:
            trace("Dice merge index error")
            return
        if not dice1:
            trace(f"Dice merge is None {x=} {y=}")
        if not dice2:
            trace(f"Dice merge is None {x2=} {y2=}")
        if not dice1 or not dice2:
            return

        if not dice1.is_merged(dice2):
            return

        dice2.merge(dice1)

    def destroy_dices(self):
        for dice in self.get_flat_dices():
            if dice and dice.is_destroy:
                self.dices[dice.y][dice.x] = None

    def get_free_positions(self):
        free_positions = [
            (y, x)
            for y in range(len(self.dices))
            for x in range(len(self.dices[y]))
            if self.dices[y][x] is None
        ]
        return free_positions

    def create_dice(self):
        dice: "Dice" = random.choice(self.deck.dices)()
        return dice

    def create_and_set_dice(self):
        free_positions = self.get_free_positions()
        if free_positions:
            y, x = random.choice(free_positions)
            dice = self.create_dice()
            self.set_dice(x, y, dice)

    def set_dice(self, x, y, dice: "Dice"):
        self.dices[y][x] = dice
        dice.set_position(x, y)
        trace(f"{self} new dice {x} {y} {dice}")

    def get_output(self):
        table = PrettyTable()
        table.header = False

        for row in self.dices:
            table.add_row(
                [f"{dice.__class__.__name__[:3]}({dice.dot})" if dice else "_" for dice in row]
            )

        return Message(MessageLevel.info, f"\n{table}")

    def level_up(self, dice):
        dice.level_cost += Config.ADD_LEVEL_UP_COST
        dice.__class__.level += 1
