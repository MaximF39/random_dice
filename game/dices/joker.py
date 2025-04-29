import copy

from dices.dice import Dice


class JokerDice(Dice):
    level = 1

    def __init__(self, x=None, y=None, dot=1):
        super().__init__(x, y, dot)
        self.attack_damage = 55
        self.attack_speed = 1.5

    def merge(self, other: "Dice"):
        self.__class__ = copy.copy(other.__class__)
        self.__dict__ = copy.copy(other.__dict__)
