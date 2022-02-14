COLS_NB = 10
ROWS_NB = 16

BORDER = -1
GROUND = -2

DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'
CHANGE = 'X'
ACTIONS = [CHANGE, DOWN, LEFT, RIGHT]

EMPTY = 0
RED = 1
YELLOW = 2
GREEN = 3
BLUE = 4
PURPLE = 5
ORANGE = 6
SPECIAL = 7
COLORS = [EMPTY, RED, YELLOW, GREEN, BLUE, PURPLE, ORANGE, SPECIAL]

REWARD_LOSE = -100000
REWARD_BORDER = -100
REWARD_GROUND = 100
REWARD_CHANGE = -1
REWARD_MOVE = -1
REWARD_MOVE_DOWN = -1
REWARD_ON_TOP = -2
REWARD_BREAK = 100

EXPLORATION = 0

SPRITE_SIZE = 64
