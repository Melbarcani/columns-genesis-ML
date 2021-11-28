import Constants
import numpy as np


def create_board(rows, cols):
    # matrix = np.arange(14 * 8).reshape(rows, cols)
    matrix = np.zeros((rows, cols))
    matrix.astype(int)
    matrix[Constants.ROWS_NB - 1] = Constants.GROUND
    matrix[:, 0] = Constants.BORDER
    matrix[:, cols - 1] = Constants.BORDER
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
    if row_count < 2 and row == Constants.ROWS_NB - 2 and len(array) < 3:
        print()
        # get_cells_when_too_close_to_ground(array, board, col, row)
    elif row_count < 2 and row == Constants.ROWS_NB - 2 and len(array) == 3:
        print()
        # array.append(package_right_and_left_four_cells(board, row, col))
    elif row_count < 2 and row < Constants.ROWS_NB - 2:
        get_nearest_cells_recursive_helper(board, row + 1, col, row_count + 1, array)
        get_regular_cells(array, board, col, row, row_count)
    return array


def get_regular_cells(array, board, col, row, row_count):
    if col > 1 + row_count:
        array.append(board[row + 1][col - 1 - row_count])
    array.append(board[row + 1][col])
    if col < Constants.COLS_NB - 1 - row_count:
        if board[row + 1][col + 1 + row_count] != Constants.BORDER:
            array.append(board[row + 1][col + 1 + row_count])


def get_cells_when_too_close_to_ground(array, board, col, row):
    if col == 1:
        array.append(package_right_six_cells(board, row, col))
    elif col == Constants.COLS_NB - 2:
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
    new_row = state[0][0]
    new_col = state[0][1]
    return {(new_row, new_col): (get_column_agent(board, new_row, new_col), get_nearest_cells(board, new_row, new_col))}


def compute_cells():
    pass


def set_board(board, state, column):
    row = state[0]
    col = state[1]
    for i in range(3):
        board[row - i, col] = column[i]


def update_env_state(env_state, new_state, column):
    row = new_state[0]
    col = new_state[1]
    print(env_state[row, col][1][0])
    print("len", len(env_state[row, col][1]))
    # for i in range(len(env_state[row, col][1])):
    #     env_state[row - i, col][1][i] = column[i]


class Environment:
    def __init__(self):
        self.__board = create_board(Constants.ROWS_NB, Constants.COLS_NB)
        self.__states = {}
        for row in range(self.__board.shape[0]):
            for col in range(0, len(self.__board[row])):
                if col != 0 and col != Constants.COLS_NB and row != Constants.ROWS_NB:
                    self.__states[(row, col)] = [[row, col], get_column_agent(self.__board, row, col),
                                                 get_nearest_cells(self.__board, row, col)]
                    if col == 4 and row == 2:
                        self.__start = (row, col)
                elif row == Constants.ROWS_NB:
                    self.__states[(row, col)] = [[], [Constants.GROUND], []]
                else:
                    self.__states[(row, col)] = [[], [Constants.BORDER], []]

                    # self.__states[(row, col)] = board[row][col]
                # if row == GROUND:
                # elif col == BORDER:
                #    self.__states[(row, col)] = board[row][col]
                # else:
                #   self.__states[(row, col)] = board[row][col]
        print(self.__board)

    def apply(self, agent, action):
        state = agent.state
        column = agent.column
        if action == Constants.DOWN:
            new_state = (state[0] + 1, state[1])
        elif action == Constants.LEFT:
            new_state = (state[0], state[1] - 1)
        elif action == Constants.RIGHT:
            new_state = (state[0], state[1] + 1)
        elif action == Constants.CHANGE:
            column[0], column[1], column[2] = column[1], column[2], column[0]
            new_state = state
        else:
            raise 'Unknown action'

        if new_state in self.__states:
            print("self", self.__states)
            print("new state", new_state)
            state = new_state
            if self.__states[new_state][1][0] == Constants.BORDER:
                reward = Constants.REWARD_BORDER
                state = agent.state
            elif self.__states[new_state][1][0] == Constants.GROUND:
                reward = Constants.REWARD_BORDER
                state = agent.state
                set_board(self.__board, state, column)
                print("board", self.__board)
                print("la", agent.state)
                # self.__board
                compute_cells()
            elif self.__states[new_state][1][0] != Constants.EMPTY:
                reward = Constants.REWARD_BORDER
                state = agent.state
                if action == Constants.DOWN:
                    compute_cells()
            else:
                reward = 0
        else:
            reward = Constants.REWARD_LOSE
        update_env_state(self.__states, state, column)
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

    @property
    def states(self):
        return self.__states.keys()

    @property
    def values(self):
        return self.__states.values()


class Agent:
    def __init__(self, environment, learning_rate=0.4, discount_factor=0.5):
        self.__environment = environment
        self.__learning_rate = learning_rate
        self.__discount_factor = discount_factor
        self.__column = [0, 0, 0]
        self.__state = []
        self.__qtable = {}
        for s in self.__environment.states:
            self.__qtable[s] = {}
            for a in Constants.ACTIONS:
                self.__qtable[s][a] = 0.0
        self.reset()

    def reset(self):
        self.__state = self.__environment.start
        self.__score = 0

    def update(self, state, action, reward):
        # Q(s, a) <- Q(s, a) + learning_rate *
        #                     [reward + discount_factor * max(Q(state)) - Q(s, a)]

        maxQ = max(self.__qtable[state].values())
        self.__qtable[self.__state][action] += self.__learning_rate * (
                reward + self.__discount_factor * maxQ - self.__qtable[self.__state][action])
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
        agent.reset()
        agent.column = [Constants.RED, Constants.YELLOW, Constants.GREEN]
        # action = agent.best_action()
        env.apply(agent, Constants.CHANGE)
        for j in range(15):
            env.apply(agent, Constants.DOWN)

    print(env.values)
