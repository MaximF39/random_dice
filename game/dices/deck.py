from dices.dice import Dice


class Deck:
    def __init__(self, dices: list[type[Dice]]):
        self.dices = dices
        self.id_to_dice = dict(zip(range(len(self.dices)), self.dices, strict=False))
