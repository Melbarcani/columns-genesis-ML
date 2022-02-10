import numpy as np

import Update_board
from Constant import *


def create_board(rows, cols):
    # matrix = np.arange(14 * 8).reshape(rows, cols)
    matrix = np.zeros((rows, cols))
    matrix.astype(int)
    matrix[:, 0] = BORDER
    matrix[:, 1] = BORDER
    matrix[:, cols - 1] = BORDER
    matrix[:, cols - 2] = BORDER
    matrix[ROWS_NB - 1] = GROUND
    matrix[ROWS_NB - 2] = GROUND
    # matrix[1][1] = 9
    # matrix[:, 1] = 1
    # matrix[:, 2] = 2
    # matrix[:, 3] = 3
    # matrix[:, 4] = 4
    # matrix[:, 5] = 5
    # matrix[:, 6] = 6
    return matrix


def get_column_agent(board, row, col):
    array = [board[row][col]]
    array = get_column_helper(board, row, col, array, 0)
    while len(array) < 3:
        array.append(0)
    return array


def get_column_helper(board, row, col, array, counter):
    if counter < 2 and row != 0:
        array.append(board[row - 1][col])
        get_column_helper(board, row - 1, col, array, counter + 1)
    return array


def get_nearest_cells(board, row, col):
    array = []
    if COLS_NB - 2 > col > 1 and row < ROWS_NB - 2:
        for i in range(3):
            array.append(board[row + 1][col + i])
            array.append(board[row + 2][col - i])
    return array


def set_Colunm_in_board(board, position, column):
    row = position[0]
    col = position[1]
    i = 0
    while row > -1 and i < 3:
        board[row, col] = column[i]
        row -= 1
        i += 1


class Environment:

    def __init__(self):
        self.__board = create_board(ROWS_NB, COLS_NB)
        self.__states = {}
        self.update_states(self.__board)
        self.__change_counter = 0
        self.__lost = False
        self.__round_ended = False
        self.__counter = 0
        self.__border = 0
        self.__tracker = []

    def reset(self):
        self.__board = create_board(ROWS_NB, COLS_NB)
        self.__states = {}
        self.update_states(self.__board)
        self.__change_counter = 0
        self.__lost = False
        self.__round_ended = False
        self.__counter = 0

    def update_states(self, board):
        for row in range(ROWS_NB):
            for col in range(COLS_NB):
                self.__states[(row, col)] = [get_column_agent(board, row, col),
                                             get_nearest_cells(board, row, col)]
                if col == 4 and row == 0:
                    self.__start = [get_column_agent(board, row, col),
                                    get_nearest_cells(board, row, col)]

    def update_position_and_column__states(self, board, position, column):
        row = position[0]
        col = position[1]
        self.__states[(row, col)] = [column, get_nearest_cells(board, row, col)]

    def apply(self, agent, action):
        # remove_previous_colunm(self._previous_col)
        position = agent.position
        column = agent.column
        new_position = self.perform_actions(action, column, position)
        old_board = self.__board
        reward = 0

        if new_position in self.__states:
            if old_board[new_position[0]][new_position[1]] == BORDER:
                reward = REWARD_BORDER
            elif old_board[new_position[0]][new_position[1]] == GROUND:
                set_Colunm_in_board(self.__board, position, column)
                count, self.__board = Update_board.update_cells(self.__board, position)
                self.__round_ended = True
                reward = REWARD_BREAK * count if count > 0 else 0
            elif old_board[new_position] != EMPTY:
                current_column_row_position = position[0]
                if current_column_row_position < 2:
                    reward = REWARD_LOSE
                    set_Colunm_in_board(self.__board, position, column)
                    self.__round_ended = True
                    self.__lost = True
                    print("Lost")
                    #return reward
                elif action == RIGHT or action == LEFT:
                    reward = REWARD_BORDER
                else:
                    if action == DOWN:
                        set_Colunm_in_board(self.__board, position, column)
                        count, self.__board = Update_board.update_cells(self.__board, position)
                        self.__round_ended = True
                        reward = REWARD_BREAK * count if count > 0 else -1 # check to set to 0
                        # print("count", count, "BREAK", REWARD_BREAK, "after break", reward)
            else:
                if action == DOWN:
                    reward = 0
                elif self.__change_counter == 1:
                    # reset to first order and move by one step to down in order to force IA to not dot it every time
                    self.__change_counter = -1
                    reward = REWARD_CHANGE
                elif action == RIGHT or action == LEFT:
                    self.__border += 1
                    reward = REWARD_MOVE
                agent.position = new_position
        else:
            reward = REWARD_LOSE

        self.update_position_and_column__states(self.__board, new_position, column)
        state = self.__states.get(new_position)
        agent.update(state, action, reward)
        return reward

    def perform_ground_reached(self, position, column):
        return self.perform_round_ended(column, position)

    def perform_round_ended(self, column, position):
        set_Colunm_in_board(self.__board, position, column)
        count, self.__board = Update_board.update_cells(self.__board, position)
        self.__round_ended = True
        self.update_position_and_column__states(self.__board, position)
        return REWARD_BREAK * count if count > 0 else 0

    def perform_actions(self, action, column, position):
        if action == DOWN:
            new_position = (position[0] + 1, position[1])
        elif action == LEFT:
            new_position = (position[0], position[1] - 1)
        elif action == RIGHT:
            new_position = (position[0], position[1] + 1)
        elif action == CHANGE:
            column[0], column[1], column[2] = column[1], column[2], column[0]
            self.__change_counter += 1
            new_position = position
        else:
            raise 'Unknown action'
        return new_position

    @property
    def borderCount(self):
        return self.__border

    @property
    def tracker(self):
        return self.__tracker

    @property
    def values(self):
        return self.__states.values()

    @property
    def start(self):
        return self.__start

    @property
    def isLost(self):
        return self.__lost

    @isLost.setter
    def isLost(self, lost):
        self.__lost = lost

    @property
    def board(self):
        return self.__board

    @property
    def is_round_ended(self):
        return self.__round_ended

    @is_round_ended.setter
    def is_round_ended(self, ended):
        self.__round_ended = ended
