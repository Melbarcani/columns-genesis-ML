from Agent import *
import update_board
import numpy as np


def create_board(rows, cols):
    # matrix = np.arange(14 * 8).reshape(rows, cols)
    matrix = np.zeros((rows, cols))
    matrix.astype(int)
    matrix[:, 0] = BORDER
    matrix[:, cols - 1] = BORDER
    matrix[ROWS_NB - 1] = GROUND
    # matrix[1][1] = 9
    # matrix[:, 1] = 1
    # matrix[:, 2] = 2
    # matrix[:, 3] = 3
    # matrix[:, 4] = 4
    # matrix[:, 5] = 5
    # matrix[:, 6] = 6
    return matrix


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
        get_cells_when_too_close_to_ground(array, board, col, row)
    elif row_count < 2 and row == ROWS_NB - 2 and len(array) == 3:
        b = 0
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
    elif col == COLS_NB - 1:
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


def set_board(board, state, column):
    row = state[0]
    col = state[1]
    for i in range(3):
        board[row - i, col] = column[i]


class Environment:
    def __init__(self):
        self.__board = create_board(ROWS_NB, COLS_NB)
        self.__states = {}
        self.update_states(self.__board)
        self.__change_counter = 0
        self.__lost = False
        self.__round_ended = False

    def reset(self):
        self.__board = create_board(ROWS_NB, COLS_NB)
        self.__states = {}
        self.update_states(self.__board)
        self.__change_counter = 0
        self.__lost = False
        self.__round_ended = False

    def update_states(self, board):
        for row in range(board.shape[0]):
            for col in range(0, len(board[row])):
                if col != 0 and col != COLS_NB and row != ROWS_NB:
                    self.__states[(row, col)] = [[row, col], get_column_agent(board, row, col),
                                                 get_nearest_cells(board, row, col)]
                    if col == 4 and row == 0:
                        self.__start = (row, col)
                elif row == ROWS_NB:
                    self.__states[(row, col)] = [[], [GROUND], []]
                else:
                    self.__states[(row, col)] = [[], [BORDER], []]

    def apply(self, agent, action):
        state = agent.state
        column = agent.column
        new_state = self.perform_actions(action, column, state)

        if new_state in self.__states:
            state = new_state
            supposed_current_position = self.__states[state][1][0]
            self.__round_ended = False
            if supposed_current_position == BORDER:
                reward = REWARD_BORDER
                state = agent.state
            elif supposed_current_position == GROUND:
                reward, state = self.perform_ground_reached(agent, column)
            elif supposed_current_position != EMPTY:
                previous_position_cell_down = self.__states[(agent.state[0] + 1, agent.state[1])][1][0]
                current_column_row_position = self.__states[state][0][0]
                if current_column_row_position < 2:
                    reward = REWARD_LOSE
                    self.__lost = True
                    print("Lost")
                # elif previous_position_cell_down == EMPTY:
                #     print("ICI")
                #     state = agent.state
                #     reward = REWARD_BORDER - (REWARD_ROW - state[0])  # state[0] == current row
                else:
                    reward = REWARD_BORDER - (REWARD_ROW - state[0])  # state[0] == current row
                    state = agent.state
                    set_board(self.__board, state, column)
                    self.update_states(self.__board)
                    if action == DOWN:
                        reward += self.perform_round_ended(column, state)
            else:
                reward = REWARD_TIME
        else:
            reward = REWARD_LOSE
        agent.update(state, action, reward)
        return reward

    def perform_actions(self, action, column, state):
        if action == DOWN:
            new_state = (state[0] + 1, state[1])
        elif action == LEFT:
            new_state = (state[0], state[1] - 1)
        elif action == RIGHT:
            new_state = (state[0], state[1] + 1)
        elif action == CHANGE:
            column[0], column[1], column[2] = column[1], column[2], column[0]
            self.__change_counter += 1
            if self.__change_counter == 2:
                self.__change_counter = 0
                new_state = (state[0] + 1, state[1])
            else:
                new_state = state
        else:
            raise 'Unknown action'
        return new_state

    def perform_round_ended(self, column, state):
        set_board(self.__board, state, column)
        count, self.__board = update_board.update_cells(self.__board, state)
        self.__round_ended = True
        self.update_states(self.__board)
        return REWARD_BREAK * count if count > 0 else 0

    def perform_ground_reached(self, agent, column):
        state = agent.state
        reward = self.perform_round_ended(column, state)
        reward += REWARD_GROUND
        return reward, state

    # @property
    # def states(self):
    #     return self.__states.keys()

    @property
    def is_round_ended(self):
        return self.__round_ended

    @is_round_ended.setter
    def is_round_ended(self, ended):
        self.__round_ended = ended

    @property
    def isLost(self):
        return self.__lost

    @isLost.setter
    def isLost(self, lost):
        self.__lost = lost

    @property
    def start(self):
        return self.__start

    @property
    def board(self):
        return self.__board

    @board.setter
    def board(self, board):
        self.__board = board

    @property
    def states(self):
        return self.__states.keys()

    @property
    def values(self):
        return self.__states.values()

    def get(self, state):
        return self.__states[state]



