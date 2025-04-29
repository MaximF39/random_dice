import json
import os
import threading
import time
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any

from game import Game


@dataclass
class Info:
    id: Any


@dataclass
class InfoGame(Info):
    player_money: int
    count_mobs: int
    total_mobs_destroy: int
    dice_to_level: dict[int, int]
    game_time: float
    map: str
    history_calls: list[str]


class Statistics:
    @abstractmethod
    def get_statistics(self) -> Info: ...


class CollectStatic:
    def __init__(self, statistics: Statistics):
        self.file_id = 0
        self.t_collect = None
        self.run = True
        self.statistics = statistics
        self.path = "statistics/statistics"
        while os.path.exists(new_path := f"{self.path}_{self.file_id}.json"):
            self.file_id += 1
        self.new_path = new_path
        log_dir = os.path.dirname(self.new_path)
        os.makedirs(log_dir, exist_ok=True)
        with open(self.new_path, "w"):
            ...

    def run_t_collect(self):
        self.t_collect = threading.Thread(target=self.collect)
        self.t_collect.start()

    def collect(self):
        while self.run:
            self.collect_and_save()
            time.sleep(0.1)

    def finish(self):
        self.run = False
        self.t_collect.join()

    def collect_and_save(self):
        data = self.statistics.get_statistics()
        new_data = {data.id: data.__dict__}

        # Читаем существующий JSON
        if os.path.exists(self.new_path):
            with open(self.new_path, encoding="utf-8") as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = {}  # Файл пуст или повреждён

        else:
            existing_data = {}

        # Обновляем данные
        existing_data.update(new_data)

        # Перезаписываем файл
        with open(self.new_path, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=4, default=str)


class GameStatistics(Statistics):
    def __init__(self):
        self.game = Game.get_instance()

    def get_statistics(self) -> InfoGame:
        if self.game.start_time is None:
            return Info(id=0)
        game_time = round(time.time() - self.game.start_time, 1)
        return InfoGame(
            id=game_time,
            player_money=self.game.player_manager.money,
            count_mobs=len(self.game.mobs_manager.mobs),
            total_mobs_destroy=self.game.mobs_manager.total_mobs_destroy,
            dice_to_level=self.game.dices_manager.deck.id_to_dice,
            game_time=game_time,
            map=self.game.dices_manager.get_output().msg,
            history_calls=self.game.history_player_calls,
        )


class TestStatistics(Statistics):
    id = 0

    def get_statistics(self) -> Info:
        self.id += 1
        return Info(id=self.id)


if __name__ == "__main__":
    stat = TestStatistics()
    CollectStatic(stat).collect()
