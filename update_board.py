from Constants import *
import numpy as np


def update_cells(board, cell):
    row = cell[0]
    col = cell[1]
    print("inside\n", board)
    cells_to_check = [(row, col), (row - 1, col), (row - 2, col)]
    count = empty_cells(board, cells_to_check, 0)
    return count, board


def empty_cells(board, cells, count):
    cells_to_empty = []
    for c in cells:
        get_cells_to_empty(board, c[0], c[1], cells_to_empty)
    for c in cells_to_empty:
        board[c[0]][c[1]] = 0
        count += 1

    if len(cells_to_empty) > 0:
        sort_board(board, count)
    return count


def get_cells_to_empty(board, row, col, cells_to_empty):
    vertical_count = check_value(board, row, col, 1, 0, 0) + check_value(board, row, col, -1, 0, 0) + 1
    diagonal_count = check_value(board, row, col, 1, 1, 0) + check_value(board, row, col, -1, -1, 0) + 1
    diagonal2_count = check_value(board, row, col, 1, -1, 0) + check_value(board, row, col, -1, 1, 0) + 1
    horizontal_count = check_value(board, row, col, 0, 1, 0) + check_value(board, row, col, 0, -1, 0) + 1
    if vertical_count > 2:
        append_cells_to_empty(board, row, col, -1, 0, cells_to_empty)
        append_cells_to_empty(board, row, col, 1, 0, cells_to_empty)
    if diagonal_count > 2:
        append_cells_to_empty(board, row, col, -1, -1, cells_to_empty)
        append_cells_to_empty(board, row, col, 1, 1, cells_to_empty)
    if diagonal2_count > 2:
        append_cells_to_empty(board, row, col, 1, -1, cells_to_empty)
        append_cells_to_empty(board, row, col, -1, 1, cells_to_empty)
    if horizontal_count > 2:
        append_cells_to_empty(board, row, col, 0, 1, cells_to_empty)
        append_cells_to_empty(board, row, col, 0, -1, cells_to_empty)
    if vertical_count > 2 or diagonal_count > 2 or diagonal2_count > 2 or horizontal_count > 2:
        if not cells_to_empty.__contains__((row, col)):
            cells_to_empty.append((row, col))


def append_cells_to_empty(board, row, col, dx, dy, cells_to_empty):
    content = board[row][col]
    if row + dx < ROWS_NB:
        next_content = board[row + dx][col + dy]
        if content == next_content and content != 0:
            append_cells_to_empty(board, row + dx, col + dy, dx, dy, cells_to_empty)
            if not cells_to_empty.__contains__((row + dx, col + dy)):
                cells_to_empty.append((row + dx, col + dy))


def check_value(board, row, col, dx, dy, count):
    content = board[row][col]
    if row + dx < 14:
        next_content = board[row + dx][col + dy]
        if content == next_content and content != 0:
            return check_value(board, row + dx, col + dy, dx, dy, count) + 1
    return count


def sort_board(board, count):
    dirty = True
    cells = []
    while dirty:
        dirty = False
        for i in range(ROWS_NB - 2, -1, -1):
            for j in range(1, COLS_NB - 1):
                if board[i][j] != EMPTY and board[i + 1][j] == EMPTY:
                    board[i + 1][j] = board[i][j]
                    board[i][j] = 0
                    cells.append((i + 1, j))
                    dirty = True
    empty_cells(board, cells, count)


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
    matrix[ROWS_NB - 2, 4:6] = 3
    matrix[ROWS_NB - 3, 4:6] = 4
    # matrix[ROWS_NB - 5, 1:4] = 6
    # matrix[ROWS_NB - 6, 1:4] = 7
    # matrix[ROWS_NB - 7, 1:4] = 8
    # matrix[ROWS_NB - 8, 3:4] = 1
    matrix[ROWS_NB - 4, 4:6] = 1
    matrix[ROWS_NB - 4: ROWS_NB - 2, 3] = 1
    matrix[ROWS_NB - 5, 3] = 3
    return matrix


def apply():
    board = create_board(ROWS_NB, COLS_NB)
    cell = (ROWS_NB - 2, 3)
    print(board)
    update_cells(board, cell)
    print(board)
