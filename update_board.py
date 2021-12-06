from Constants import *
import numpy as np


def update_cells(board, cell):
    row = cell[0]
    col = cell[1]
    update_cell(board, row, col)
    # update_cell(board, row - 1, col)
    # update_cell(board, row - 2, col)


def sort_board(board):
    unsorted = True
    cells = []
    while unsorted:
        unsorted = False
        for i in range(ROWS_NB - 3, -1, -1):
            for j in range(1, COLS_NB - 1):
                if board[i][j] != EMPTY and board[i + 1][j] == EMPTY:
                    board[i + 1][j] = board[i][j]
                    board[i][j] = 0
                    cells.append((i, j))
                    unsorted = True
        for c in cells:
            break_cells(board, c[0], c[1])


def break_cells(board, row, col):
    count1 = check_value(board, row, col, 1, 0, 0) + check_value(board, row, col, -1, 0, 0) + 1
    count2 = check_value(board, row, col, 1, 1, 0) + check_value(board, row, col, -1, -1, 0) + 1
    count3 = check_value(board, row, col, 1, -1, 0) + check_value(board, row, col, -1, 1, 0) + 1
    count4 = check_value(board, row, col, 0, 1, 0) + check_value(board, row, col, 0, -1, 0) + 1
    broken = False
    if count1 > 2:
        set_zeros(board, row, col, -1, 0)
        set_zeros(board, row, col, 1, 0)
        broken = True
    if count2 > 2:
        set_zeros(board, row, col, -1, -1)
        set_zeros(board, row, col, 1, 1)
        broken = True
    if count3 > 2:
        set_zeros(board, row, col, 1, -1)
        set_zeros(board, row, col, -1, 1)
        broken = True
    if count4 > 2:
        set_zeros(board, row, col, 0, 1)
        set_zeros(board, row, col, 0, -1)
        broken = True
    if broken:
        board[row][col] = 0
        print("board", board)
        sort_board(board)


def set_zeros(board, row, col, dx, dy):
    content = board[row][col]
    next_content = board[row + dx][col + dy]
    if content == next_content and content != 0:
        set_zeros(board, row + dx, col + dy, dx, dy)
        board[row + dx][col + dy] = 0


def check_value(board, row, col, dx, dy, count):
    content = board[row][col]
    next_content = board[row + dx][col + dy]
    if content == next_content and content != 0:
        return check_value(board, row + dx, col + dy, dx, dy, count) + 1
    return count


def update_cell(board, row, col):
    break_cells(board, row, col)


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
    matrix[ROWS_NB - 4, 1:3] = 2
    matrix[ROWS_NB - 2, 4:6] = 5
    matrix[ROWS_NB - 3, 4:6] = 5
    matrix[ROWS_NB - 5, 1:4] = 5
    matrix[ROWS_NB - 6, 1:4] = 5
    matrix[ROWS_NB - 7, 1:4] = 5
    matrix[ROWS_NB - 4: ROWS_NB - 2, 3] = 1
    return matrix


def apply():
    board = create_board(ROWS_NB, COLS_NB)
    print(board)
    cell = (ROWS_NB - 2, 3)
    update_cells(board, cell)
    print(board)
