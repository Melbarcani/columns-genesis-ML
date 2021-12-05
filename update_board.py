from Constants import *
import numpy as np


def update_cells(board):
    pass


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
    matrix[ROWS_NB - 2, 1:4] = 1
    matrix[ROWS_NB - 3, 1:3] = 2
    return matrix


if __name__ == '__main__':
    board = create_board(ROWS_NB, COLS_NB)
    print(board)
    board = update_cells(board)
