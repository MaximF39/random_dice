from core.dices.dice import Dice
from utils.my_math import sum_ap


class ComboDice(Dice):
    combo = 0
    level = 1

    def __init__(self, x=None, y=None, dot=1):
        super().__init__(x, y, dot)
        self.attack_damage = 80
        self.attack_speed = 1.2

    def get_damage(self):
        return self.dot * (self.attack_damage + sum_ap(0, 14, ComboDice.combo))

    def merge(self, other):
        ComboDice.combo -= 2
        super().merge(other)
