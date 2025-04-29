from config import Config
from dices.dices_manager import DicesManager
from utils.trace import trace


class Dice:
    level = 1
    level_cost = Config.INITIAL_LEVEL_COST

    def __init__(self, x=None, y=None, dot=1):
        self.x = x
        self.y = y
        self.dot = dot
        self.attack_damage = 0
        self.attack_speed = 0
        self.properties = {"add_dot_merge": 1}
        self.is_destroy = False

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def decrease_points(self, dot=1):
        trace()
        self.dot -= dot
        return self.dot > 0

    def get_damage(self):
        trace()
        return self.attack_damage

    def is_merged(self, other: "Dice"):
        trace(f"dice1.dot != dice2.dot | {self.dot} != {other.dot}")
        return self.dot == other.dot

    def merge(self, other: "Dice"):
        trace()
        self.dot += other.properties["add_dot_merge"]
        other.destroy()

        dices_manager: DicesManager = DicesManager.get_instance()
        dice = dices_manager.create_dice()
        dice.dot = self.dot
        dices_manager.set_dice(self.x, self.y, dice)
        self.destroy()

    def destroy(self):
        trace()
        self.is_destroy = True
