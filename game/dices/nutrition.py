from dices.dice import Dice


class NutritionDice(Dice):
    level = 1
    add_property = False

    def __init__(self, x=None, y=None, dot=1):
        super().__init__(x, y, dot)
        self.attack_damage = 55
        self.attack_speed = 1.5

    def merge(self, other: "Dice"):
        super().merge(other)
