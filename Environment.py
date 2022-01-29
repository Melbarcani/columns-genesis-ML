import math

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
    if col < COLS_NB - 2 and col > 1 and row < ROWS_NB - 2:
        for i in range(3):
            array.append(board[row + 1][col + i])
            array.append(board[row + 2][col - i])
    return array


def set_Colunm_in_board(board, position, column):
    row = position[0]
    col = position[1]
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
        for row in range(ROWS_NB):
            for col in range(COLS_NB):
                self.__states[(row, col)] = [get_column_agent(board, row, col),
                                             get_nearest_cells(board, row, col)]
                if col == 4 and row == 0:
                    self.__start = [get_column_agent(board, row, col),
                                    get_nearest_cells(board, row, col)]

    def update_position_states(self, board, position):
        row = position[0]
        col = position[1]
        self.__states[(row, col)] = [get_column_agent(board, row, col),
                                     get_nearest_cells(board, row, col)]

    def apply(self, agent, action):
        #remove_previous_colunm(self._previous_col)
        position = agent.position
        column = agent.column
        new_position = self.perform_actions(action, column, position)

        if new_position in self.__states:
            self.__round_ended = False
            reward = 0
            if self.__board[new_position] == BORDER:
                reward += REWARD_BORDER
                new_position = position
            elif self.__board[new_position] == GROUND:
                reward, new_position = self.perform_ground_reached(agent, column)
            elif self.__board[new_position] != EMPTY:
                # previous_position_cell_down = self.__states[(agent.state[0] + 1, agent.state[1])][1][0]
                current_column_row_position = agent.position[0]
                if current_column_row_position < 2:
                    new_position = agent.position
                    reward = REWARD_LOSE
                    self.__lost = True
                    print("Lost")
                elif action == RIGHT or action == LEFT:
                    new_position = agent.position
                    reward = REWARD_BORDER
                else:
                    new_position = agent.position
                    if action == DOWN:
                        reward += self.perform_round_ended(column, new_position)
            else:
                if self.__change_counter == 3:  # reset to first order and move by one step to down in order to force IA to not dot it every time
                    self.__change_counter = 0
                    reward += REWARD_CHANGE
        else:
            reward = REWARD_LOSE
        #set_Colunm_in_board(self.__board, position, column)
        #self.__previous_pos = position
        self.update_position_states(self.__board, new_position)
        agent.position = new_position
        agent.update(self.__states.get(new_position), action, reward)
        return reward

    def perform_ground_reached(self, agent, column):
        position = agent.position
        reward = self.perform_round_ended(column, position)
        return reward, position

    def perform_round_ended(self, column, position):
        set_Colunm_in_board(self.__board, position, column)
        count, self.__board = Update_board.update_cells(self.__board, position)
        self.__round_ended = True
        self.update_position_states(self.__board, position)
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
