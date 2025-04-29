def test_initial_game_state(game):
    assert game.player_manager.money > 0
    assert game.mobs_manager.mob_hp > 0
    assert len(game.mobs_manager.mobs) == 0
