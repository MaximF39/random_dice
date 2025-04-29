from utils.trace import trace


class Mob:
    def __init__(self, hp, money):
        self.hp = hp
        self.hp_prev = None
        self.money = money

    def take_damage(self, amount):
        self.hp_prev = self.hp
        self.hp -= amount
        trace(f"{self} get damage: {self.hp_prev} - {amount} = {self.hp}")

    def is_live(self):
        return self.hp > 0

    def is_dead(self):
        return not self.is_live()

    def destroy(self):
        trace()
