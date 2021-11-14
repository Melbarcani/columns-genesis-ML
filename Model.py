DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'
CHANGE = 'X'
ACTIONS = [CHANGE, DOWN, LEFT, RIGHT]

TOP = 0
MIDDLE = 1
BOTTOM = 2

COLS_NB = 6
ROWS_NB = 13

EMPTY = "EMPTY"
RED = "RED"
YELLOW = "YELLOW"
GREEN = "GREEN"
BLUE = "BLUE"
PURPLE = "PURPLE"
ORANGE = "ORANGE"
SPECIAL = "SPECIAL"
COLORS = [EMPTY, RED, YELLOW, GREEN, BLUE, PURPLE, ORANGE, SPECIAL]

REWARD_CELL = 20
REWARD_ROW_THREE = -25
REWARD_ROW_SIX = -50
REWARD_NINE = -75
REWARD_TWELVE = -100
REWARD_LOSE = -1000
REWARD_BORDER = -10
REWARD_FILLED_CELL = -10


class Environment:
    def __init__(self):
        board = [[ROWS_NB], [COLS_NB]]
        self.__current = {TOP: EMPTY, MIDDLE: EMPTY, BOTTOM: EMPTY}
        #self.__next = {}
        self.__states = {}
        for row in range(ROWS_NB):
            for col in range(COLS_NB):
                board[row][col] = EMPTY
                self.__states[(row, col)] = board[row][col]

    def apply(self, agent, action):
        state = agent.state
        if action == DOWN:
            new_state = (state[0] + 1, state[1])
        elif action == LEFT:
            new_state = (state[0], state[1] - 1)
        elif action == RIGHT:
            new_state = (state[0], state[1] + 1)
        elif action == CHANGE:
            position = agent.position
            if position == TOP:
                new_state = (state[0] + 1, state[1])
            if position == MIDDLE:
                new_state = (state[0] + 1, state[1])
            if position == BOTTOM:
                new_state = (state[0] - 2, state[1])
        else:
            raise 'Unknown action'

    @property
    def current(self):
        return self.__current

class Agent:
    def __init__(self, environment, position, learning_rate=0.4, discount_factor=0.5):
        self.__environment = environment
        self.__color = environment.current(position)
        self.__learning_rate = learning_rate
        self.__discount_factor = discount_factor
        self.__qtable = {}
        for s in self.__environment.states:
            self.__qtable[s] = {}
            for a in ACTIONS:
                self.__qtable[s][a] = 0.0

if __name__ == '__main__':
    env = Environment()
    agents = [Agent(env, TOP), Agent(env, MIDDLE), Agent(env, BOTTOM)]
