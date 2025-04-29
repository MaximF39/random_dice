from command_game import CommandGame
from dices.deck import Deck
from dices.combo_dice import ComboDice
from game import Game
from dices.dices_manager import DicesManager
from mobs.mobs_manager import MobsManager
from player.player_manager import PlayerManager
from ui.communicator import Communicator
from ui.input.input_cli import InputCLI
from ui.output.output_cli import OutputCLI
from ui.statistics import CollectStatic, GameStatistics


def test():
    game = create_game()
    print()

def create_game():
    game = Game(player_manager=PlayerManager(),
                mobs_manager=MobsManager(),
                dices_manager=DicesManager(Deck([ComboDice])))
    return game

def main():
    game = create_game()
    command_game = CommandGame(game)
    input_cli = InputCLI(command_game, start=True)
    output_cli = OutputCLI(start=True)
    communicator = Communicator(input_cli, output_cli, game)
    communicator.listen()
    collector = CollectStatic(GameStatistics())
    collector.run_t_collect()
    game.game_loop()

    collector.finish()
    communicator.finish()
    input_cli.finish()

if __name__ == '__main__':
    # test()
    main()
