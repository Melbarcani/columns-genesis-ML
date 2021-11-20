import numpy as np

COLS_NB = 8
ROWS_NB = 14
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

REWARD_CELL = 20
REWARD_ROW_THREE = -25
REWARD_ROW_SIX = -50
REWARD_NINE = -75
REWARD_TWELVE = -100
REWARD_LOSE = -1000
REWARD_BORDER = -10
REWARD_FILLED_CELL = -10


def create_board(rows, cols):
    matrix = np.zeros((rows, cols))
    matrix[0] = GROUND
    matrix[:, 0] = BORDER
    matrix[:, cols - 1] = BORDER
    return matrix


def check_clear_color():
    pass


class Environment:
    def __init__(self):
        board = create_board(ROWS_NB, COLS_NB)
        self.__states = {}
        for row in range(board.shape[0]):
            for col in range(len(board[row]) - 1):
                self.__states[(row, col)] = board[row][col]
            # if row == GROUND:
            # elif col == BORDER:
            #    self.__states[(row, col)] = board[row][col]
            # else:
            #   self.__states[(row, col)] = board[row][col]
        print(self.__states)
        print(board)

    def apply(self, agent, action):
        state = agent.state
        if action == DOWN:
            new_state = (state[0] + 1, state[1])
        elif action == LEFT:
            new_state = (state[0], state[1] - 1)
        elif action == RIGHT:
            new_state = (state[0], state[1] + 1)
        elif action == CHANGE:
            agent.column[0], agent.column[1], agent.column[2] = agent.column[2], agent.column[0], agent.column[1]
            new_state = ((state[0], state[1]), agent.column)
        else:
            raise 'Unknown action'
        if new_state in self.__states:
            state = new_state
            if self.__states[new_state] == BORDER:
                reward = REWARD_BORDER
            elif self.__states[new_state] == GROUND:
                reward = check_clear_color()

    @property
    def states(self):
        return self.__states.keys()


class Agent:
    def __init__(self, environment, learning_rate=0.4, discount_factor=0.5):
        self.__column = None
        self.__environment = environment
        self.__learning_rate = learning_rate
        self.__discount_factor = discount_factor
        self.__qtable = {}
        for s in self.__environment.states:
            self.__qtable[s] = {}
            for a in ACTIONS:
                self.__qtable[s][a] = 0.0

    def reset(self):
        self.__score = 0

    @property
    def column(self):
        return self.__column

    @column.setter
    def column(self, column):
        self._column = column


if __name__ == '__main__':
    env = Environment()
    agent = Agent(env)
