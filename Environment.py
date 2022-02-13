import numpy as np

import Update_board
from Constant import *


def create_board(rows, cols):
    matrix = np.zeros((rows, cols))
    matrix.astype(int)
    matrix[:, 0] = BORDER
    matrix[:, 1] = BORDER
    matrix[:, cols - 1] = BORDER
    matrix[:, cols - 2] = BORDER
    matrix[ROWS_NB - 1] = GROUND
    matrix[ROWS_NB - 2] = GROUND
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
    if COLS_NB - 2 > col > 1 and 1 < row < ROWS_NB - 2:
        for i in range(3):
            if i == 0:
                array.append(board[row + 1][col])
                array.append(board[row + 2][col])
            else:
                array.append(board[row + i][col + i])
                array.append(board[row + i][col - i])
                #array.append(board[row][col + i])
                #array.append(board[row][col - i])
                #array.append(board[row - 1][col + i])
                #array.append(board[row - 1][col - i])
                #array.append(board[row - 2][col + i])
                #array.append(board[row - 2][col - i])

    return array


def set_column_in_board(board, position, column):
    row = position[0]
    col = position[1]
    i = 0
    while row > -1 and i < 3:
        board[row, col] = column[i]
        row -= 1
        i += 1


def clear_old_column_position(board, old_position):
    row = old_position[0]
    col = old_position[1]
    i = 0
    while row > -1 and i < 3:
        board[row, col] = 0
        row -= 1
        i += 1


def set_new_column_in_board(board, position, column, old_position):
    clear_old_column_position(board, old_position)
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
        self.__actionsNumber = 0

    def reset(self):
        self.__board = create_board(ROWS_NB, COLS_NB)
        self.__states = {}
        self.update_states(self.__board)
        self.__change_counter = 0
        self.__lost = False
        self.__round_ended = False
        self.__counter = 0
        self.__actionsNumber = 0

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
        self.__states[(row, col)] = [[row], column, get_nearest_cells(board, row, col)]

    def apply(self, agent, action):
        position = tuple(agent.position)
        old_column = agent.column
        new_position, new_column = self.perform_actions(action, old_column, position)
        old_board = self.__board.copy()
        reward = 0
        is_change_operated = False

        if new_position in self.__states:
            self.__actionsNumber += 1
            if action == CHANGE:
                agent.column = new_column
                reward = REWARD_CHANGE
                is_change_operated = True
            elif old_board[new_position[0]][new_position[1]] == BORDER:
                reward = REWARD_BORDER
                new_position = position
            elif old_board[new_position[0]][new_position[1]] == GROUND:
                set_column_in_board(self.__board, position, old_column)
                count, self.__board = Update_board.update_cells(self.__board, position)
                self.__round_ended = True
                reward = REWARD_BREAK * count if count > 0 else REWARD_GROUND
                agent.score_break += reward if count > 0 else 0
                new_position = position
            elif old_board[new_position] != EMPTY:
                current_column_row_position = position[0]
                if current_column_row_position < 2 and action == DOWN:
                    reward = REWARD_LOSE
                    set_column_in_board(self.__board, position, old_column)
                    self.__round_ended = True
                    self.__lost = True
                elif action == RIGHT or action == LEFT:
                    reward = REWARD_BORDER
                    new_position = position
                else:
                    if action == DOWN:
                        count, self.__board = Update_board.update_cells(self.__board, position)
                        self.__round_ended = True
                        reward = REWARD_BREAK * count if count > 0 else REWARD_ON_TOP
                        agent.score_break += reward if count > 0 else 0
            else:
                set_new_column_in_board(self.__board, new_position, old_column, position)
                if action == DOWN:
                    reward = REWARD_MOVE_DOWN
                else:
                    reward = REWARD_MOVE
                agent.position = new_position
        else:
            reward = REWARD_LOSE

        self.update_position_and_column__states(old_board, position, old_column)
        state = self.__states.get(position)
        agent.update(state, action, reward)
        if is_change_operated:
            set_new_column_in_board(self.__board, new_position, new_column, position)
            old_column = new_column
        self.update_position_and_column__states(self.__board, new_position, old_column)
        agent.set_new_state(self.__states.get(new_position))
        return reward

    def perform_ground_reached(self, position, column, old_board):
        return self.perform_round_ended(column, position, old_board)

    def perform_round_ended(self, column, position, old_board):
        set_column_in_board(self.__board, position, column)
        count, self.__board = Update_board.update_cells(self.__board, position)
        self.__round_ended = True
        self.update_position_and_column__states(old_board, position)
        return REWARD_BREAK * count if count > 0 else 0

    def perform_actions(self, action, column, position):
        new_column = []
        if action == DOWN:
            new_position = (position[0] + 1, position[1])
        elif action == LEFT:
            new_position = (position[0], position[1] - 1)
        elif action == RIGHT:
            new_position = (position[0], position[1] + 1)
        elif action == CHANGE:
            new_column = column[1], column[2], column[0]
            self.__change_counter += 1
            new_position = position
        else:
            raise 'Unknown action'
        return new_position, new_column

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
