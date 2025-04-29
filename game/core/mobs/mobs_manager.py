from config import Config
from core.mobs.mob import Mob
from utils.message import Message, MessageLevel


class MobsManager:
    mob_cost = Config.INITIAL_MOB_MONEY
    mob_hp = Config.INITIAL_MOB_HP

    def __init__(self):
        self.mobs = []
        self.count_destroy = []
        self.total_mobs_destroy = 0

    def get_output(self):
        return Message(
            MessageLevel.info,
            f"\nMobs ({len(self.mobs)}):\n" + (" ".join([f"[{int(mob.hp)}]" for mob in self.mobs])),
        )

    def update_mobs(self, damage_count):
        self.count_destroy = []
        for damage in damage_count:
            if not self.mobs:
                return
            mob = self.mobs[0]
            mob.take_damage(damage)
            if mob.is_dead():
                mob.destroy()
                self.mobs.pop(0)
                self.count_destroy.append(mob)
                self.total_mobs_destroy += 1

    def get_destroyed(self):
        return self.count_destroy

    def create_mobs(self):
        cls = self.__class__
        self.mobs.append(Mob(hp=cls.mob_hp, money=cls.mob_cost))
        cls.mob_cost *= 1 + Config.COEF_MOB_MONEY
        cls.mob_hp *= 1 + Config.COEF_MOB_HP
