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
    matrix = np.arange(14 * 8).reshape(rows, cols)
    # matrix = np.zeros((rows, cols))
    matrix[ROWS_NB - 1] = GROUND
    matrix[:, 0] = BORDER
    matrix[:, cols - 1] = BORDER
    # matrix[1][1] = 9
    # matrix[:, 1] = 1
    # matrix[:, 2] = 2
    # matrix[:, 3] = 3
    # matrix[:, 4] = 4
    # matrix[:, 5] = 5
    # matrix[:, 6] = 6
    return matrix


def check_clear_color():
    pass


def package_six_cells(board, row, col):
    return board[row + 1][col - 1], board[row + 1][col], board[row + 1][col + 1], \
           board[row + 2][col - 1], board[row + 2][col], board[row + 2][col + 1]


def package_right_four_cells(board, row, col):
    return board[row + 1][col], board[row + 1][col + 1], \
           board[row + 2][col], board[row + 2][col + 1]


def package_right_and_left_cells(board, row, col):
    return board[row][col - 1], board[row][col + 1], \
           board[row - 1][col - 1], board[row - 1][col + 1], \
           board[row - 2][col - 1], board[row - 2][col + 1]


def package_right_six_cells(board, row, col):
    return board[row][col + 1], board[row][col + 2], board[row - 1][col + 1], board[row - 1][col + 2], board[row - 2][
        col + 1], board[row - 2][col + 2]


def recursive(board, row, col):
    array = []
    return recursive_helper(board, row, col, 0, array)


def recursive_helper(board, row, col, row_count, array):
    if row_count < 2 and row == ROWS_NB - 2:
        if col == 1:
            array.append(package_right_six_cells(board, row, col))
        elif col == 6:
            array.append(package_right_six_cells(board, row, col - 3))
        else:
            array.append(package_right_and_left_cells(board, row, col))
    elif row_count < 2 and row < ROWS_NB - 2:
        if col > 1 + row_count:
            array.append(board[row + 1][col - 1 - row_count])
        array.append(board[row + 1][col])
        if col < COLS_NB - 1 - row_count:
            if board[row + 1][col + 1 + row_count] != BORDER:
                array.append(board[row + 1][col + 1 + row_count])
        recursive_helper(board, row + 1, col, row_count + 1, array)

    return array


def get_column(board, row, col):
    array = [board[row][col]]
    return get_column_helper(board, row, col, array, 0)


def get_column_helper(board, row, col, array, counter):
    if counter < 2 and row != 0:
        array.append(board[row - 1][col])
        get_column_helper(board, row - 1, col, array, counter + 1)
    return array


class Environment:
    def __init__(self):
        board = create_board(ROWS_NB, COLS_NB)
        self.__states = {}
        for row in range(board.shape[0] - 1):
            for col in range(1, len(board[row]) - 1):
                self.__states[(row, col)] = (get_column(board, row, col), recursive(board, row, col))

                # self.__states[(row, col)] = board[row][col]
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
        self.__states = None
        self.__column = None
        self.__environment = environment
        self.__learning_rate = learning_rate
        self.__discount_factor = discount_factor
        self.__qtable = {}
        for s in self.__environment.states:
            self.__qtable[s] = {}
            for a in ACTIONS:
                self.__qtable[s][a] = 0.0

    def update(self, column):
        self.__states[(3, ROWS_NB - 3)] = column[2]
        self.__states[(2, ROWS_NB - 2)] = column[1]
        self.__states[(1, ROWS_NB - 1)] = column[0]

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

    for i in range(2):
        env.update([RED, RED, GREEN])
        # while True:
        #   agent.column = [GREEN, GREEN, RED]
