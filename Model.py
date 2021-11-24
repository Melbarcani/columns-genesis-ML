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
    # matrix = np.arange(14 * 8).reshape(rows, cols)
    matrix = np.zeros((rows, cols))
    matrix.astype(int)
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


def package_right_and_left_four_cells(board, row, col):
    return board[row - 1][col - 1], board[row - 1][col + 1], \
           board[row - 2][col - 1], board[row - 2][col + 1]


def package_right_and_left_cells(board, row, col):
    return board[row][col - 1], board[row][col + 1], \
           board[row - 1][col - 1], board[row - 1][col + 1], \
           board[row - 2][col - 1], board[row - 2][col + 1]


def package_right_six_cells(board, row, col):
    return board[row][col + 1], board[row][col + 2], board[row - 1][col + 1], board[row - 1][col + 2], board[row - 2][
        col + 1], board[row - 2][col + 2]


def get_nearest_cells(board, row, col):
    array = []
    return get_nearest_cells_recursive_helper(board, row, col, 0, array)


def get_nearest_cells_recursive_helper(board, row, col, row_count, array):
    if row_count < 2 and row == ROWS_NB - 2 and len(array) < 3:
        print()
        # get_cells_when_too_close_to_ground(array, board, col, row)
    elif row_count < 2 and row == ROWS_NB - 2 and len(array) == 3:
        print()
        # array.append(package_right_and_left_four_cells(board, row, col))
    elif row_count < 2 and row < ROWS_NB - 2:
        get_nearest_cells_recursive_helper(board, row + 1, col, row_count + 1, array)
        get_regular_cells(array, board, col, row, row_count)
    return array


def get_regular_cells(array, board, col, row, row_count):
    if col > 1 + row_count:
        array.append(board[row + 1][col - 1 - row_count])
    array.append(board[row + 1][col])
    if col < COLS_NB - 1 - row_count:
        if board[row + 1][col + 1 + row_count] != BORDER:
            array.append(board[row + 1][col + 1 + row_count])


def get_cells_when_too_close_to_ground(array, board, col, row):
    if col == 1:
        array.append(package_right_six_cells(board, row, col))
    elif col == COLS_NB - 2:
        array.append(package_right_six_cells(board, row, col - 3))
    else:
        array.append(package_right_and_left_cells(board, row, col))


def get_column_agent(board, row, col):
    array = [board[row][col]]
    return get_column_helper(board, row, col, array, 0)


def get_column_helper(board, row, col, array, counter):
    if counter < 2 and row != 0:
        array.append(board[row - 1][col])
        get_column_helper(board, row - 1, col, array, counter + 1)
    return array


def get_down(state, board):
    print("ixi", state)
    new_row = state[0][0]
    new_col = state[0][1]
    return {(new_row, new_col): (get_column_agent(board, new_row, new_col), get_nearest_cells(board, new_row, new_col))}


class Environment:
    def __init__(self):
        self.__board = create_board(ROWS_NB, COLS_NB)
        self.__states = {}
        for row in range(self.__board.shape[0]):
            for col in range(0, len(self.__board[row])):
                if col != 0 and col != COLS_NB and row != ROWS_NB:
                    self.__states[(row, col)] = [[row, col], get_column_agent(self.__board, row, col),
                                                 get_nearest_cells(self.__board, row, col)]
                    if col == 4 and row == 2:
                        self.__start = (row, col)
                elif row == ROWS_NB:
                    self.__states[(row, col)] = [[], [GROUND], []]
                else:
                    self.__states[(row, col)] = [[], [BORDER], []]

                    # self.__states[(row, col)] = board[row][col]
                # if row == GROUND:
                # elif col == BORDER:
                #    self.__states[(row, col)] = board[row][col]
                # else:
                #   self.__states[(row, col)] = board[row][col]
        print(self.__states)
        print(self.__board)

    @property
    def states(self):
        return self.__states.keys()

    def apply(self, agent, action):
        state = agent.state
        column = agent.column
        if action == DOWN:
            new_state = (state[0] + 1, state[1])
        elif action == LEFT:
            new_state = (state[0], state[1] - 1)
        elif action == RIGHT:
            new_state = (state[0], state[1] + 1)
        elif action == CHANGE:
            column[0], column[1], column[2] = column[1], column[2], column[0]
            new_state = state
        else:
            raise 'Unknown action'

        if new_state in self.__states:
            state = new_state
            if self.__states[new_state][1][0] == BORDER:
                reward = REWARD_BORDER
                state = agent.state
            elif self.__states[new_state][1][0] == GROUND:
                reward = REWARD_BORDER
                state = agent.state
            else:
                reward = 0
        else:
            print("LOSE")
            reward = REWARD_LOSE

        agent.update(state, action, reward)
        return reward

    # @property
    # def states(self):
    #     return self.__states.keys()

    @property
    def start(self):
        return self.__start

    @property
    def board(self):
        return self.__board


class Agent:
    def __init__(self, environment, learning_rate=0.4, discount_factor=0.5):
        self.__environment = environment
        self.__learning_rate = learning_rate
        self.__discount_factor = discount_factor
        self.__column = [0, 0, 0]
        self.__qtable = {}
        for s in self.__environment.states:
            self.__qtable[s] = {}
            for a in ACTIONS:
                self.__qtable[s][a] = 0.0
        self.reset()

    def reset(self):
        self.__state = self.__environment.start
        self.__score = 0

    def update(self, state, action, reward):
        # Q(s, a) <- Q(s, a) + learning_rate *
        #                     [reward + discount_factor * max(Q(state)) - Q(s, a)]

        print("values", self.__qtable[state])
        maxQ = max(self.__qtable[state].values())
        self.__qtable[self.__state][action] += self.__learning_rate * (
                reward + self.__discount_factor * maxQ - self.__qtable[self.__state][action])
        print("state", state)
        self.__state = state
        self.__score += reward

    def best_action(self):
        best = None
        for a in self.__qtable[self.__state]:
            if not best \
                    or self.__qtable[self.__state][a] > self.__qtable[self.__state][best]:
                best = a
        return best

    @property
    def state(self):
        return self.__state

    @property
    def column(self):
        return self.__column

    @column.setter
    def column(self, column):
        self.__column = column


if __name__ == '__main__':
    env = Environment()
    agent = Agent(env)

    for i in range(2):
        print("ok")
        agent.reset()
        agent.column =[RED, YELLOW, GREEN]
        # action = agent.best_action()
        print(agent.column)
        env.apply(agent, CHANGE)
        print("changeed", agent.column)
