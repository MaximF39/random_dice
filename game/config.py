class Config:
    # PLAYER
    INITIAL_MONEY = 5000
    MOBS_FOR_LOSE = 3

    # DECK
    BOARD_WIDTH = 5
    BOARD_HEIGHT = 3

    # TIME
    TIME_SPAWN_MOB = 1
    INITIAL_WAIT_START = 3

    # MOB
    INITIAL_MOB_HP = 100
    INITIAL_MOB_MONEY = 10
    COEF_MOB_HP = 0.1
    COEF_MOB_MONEY = 0.1

    # DICE
    INITIAL_DICE_COST = 10
    ADD_DICE_COST = 10

    INITIAL_LEVEL_COST = 100
    ADD_LEVEL_UP_COST = 100

    # GAME

    FPS = 0.5

    # DEBUG
    path_log = "logs/game.log"