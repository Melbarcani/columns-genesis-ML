from Constants import *
import numpy as np


def update_cells(board, cell):
    row = cell[0]
    col = cell[1]
    cells_to_empty = [(row, col), (row - 1, col), (row - 2, col)]
    count = empty_cells(board, cells_to_empty, 0)
    return count


def empty_cells(board, cells, count):
    cells_to_empty = []
    for c in cells:
        get_cells_to_empty(board, c[0], c[1], cells_to_empty)

    for c in cells_to_empty:
        print("cells to empty", c, board[c[0]][c[1]])
        board[c[0]][c[1]] = 0
        count += 1

    if len(cells_to_empty) > 0:
        sort_board(board, count)
    return count


def sort_board(board, count):
    dirty = True
    cells = []
    while dirty:
        dirty = False
        for i in range(ROWS_NB - 3, -1, -1):
            for j in range(1, COLS_NB - 1):
                if board[i][j] != EMPTY and board[i + 1][j] == EMPTY:
                    board[i + 1][j] = board[i][j]
                    board[i][j] = 0
                    cells.append((i + 1, j))
                    dirty = True
    print("cells sorted", cells)
    empty_cells(board, cells, count)


def get_cells_to_empty(board, row, col, cells_to_empty):
    count1 = check_value(board, row, col, 1, 0, 0) + check_value(board, row, col, -1, 0, 0) + 1
    count2 = check_value(board, row, col, 1, 1, 0) + check_value(board, row, col, -1, -1, 0) + 1
    count3 = check_value(board, row, col, 1, -1, 0) + check_value(board, row, col, -1, 1, 0) + 1
    count4 = check_value(board, row, col, 0, 1, 0) + check_value(board, row, col, 0, -1, 0) + 1
    if count1 > 2:
        append_cells_to_empty(board, row, col, -1, 0, cells_to_empty)
        append_cells_to_empty(board, row, col, 1, 0, cells_to_empty)
    if count2 > 2:
        append_cells_to_empty(board, row, col, -1, -1, cells_to_empty)
        append_cells_to_empty(board, row, col, 1, 1, cells_to_empty)
    if count3 > 2:
        append_cells_to_empty(board, row, col, 1, -1, cells_to_empty)
        append_cells_to_empty(board, row, col, -1, 1, cells_to_empty)
    if count4 > 2:
        append_cells_to_empty(board, row, col, 0, 1, cells_to_empty)
        append_cells_to_empty(board, row, col, 0, -1, cells_to_empty)
    if count1 or count2 or count3 or count4:
        cells_to_empty.append((row, col))


def append_cells_to_empty(board, row, col, dx, dy, cells_to_empty):
    content = board[row][col]
    next_content = board[row + dx][col + dy]
    if content == next_content and content != 0:
        append_cells_to_empty(board, row + dx, col + dy, dx, dy, cells_to_empty)
        cells_to_empty.append((row + dx, col + dy))


def check_value(board, row, col, dx, dy, count):
    content = board[row][col]
    if row + dx < 14:
        next_content = board[row + dx][col + dy]
        if content == next_content and content != 0:
            return check_value(board, row + dx, col + dy, dx, dy, count) + 1
    return count


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
    matrix[ROWS_NB - 8, 3:4] = 1
    matrix[ROWS_NB - 4, 4:6] = 1
    matrix[ROWS_NB - 4: ROWS_NB - 2, 3] = 1
    return matrix


def apply():
    board = create_board(ROWS_NB, COLS_NB)
    cell = (ROWS_NB - 5, 3)

    update_cells(board, cell)
