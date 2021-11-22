if row == 0:
    print("UN", board[row, col])
    if 1 < col < COLS_NB - 2:
        self.__states[(row, col)] = [(board[row][col]), package_six_cells(board, row, col)]
    elif col == 1:
        self.__states[(row, col)] = [(board[row][col]), package_right_four_cells(board, row, col)]
    elif col == COLS_NB - 2:
        self.__states[(row, col)] = [(board[row][col]), package_right_four_cells(board, row,
                                                                                 col - 2)]  # right four cells from col - 2 is left four cells from right border

elif row == 1:
    if 1 < col < COLS_NB - 2:
        self.__states[(row, col)] = [(board[row - 1][col], board[row][col]),
                                     package_six_cells(board, row, col)]
    elif col == 1:
        self.__states[(row, col)] = [(board[row - 1][col], board[row][col]),
                                     package_right_four_cells(board, row, col)]
    elif col == COLS_NB - 2:
        self.__states[(row, col)] = [(board[row - 1][col], board[row][col]),
                                     package_right_four_cells(board, row, col - 2)]

elif row == ROWS_NB - 2:
    if 1 < col < COLS_NB - 2:
        self.__states[(row, col)] = [(board[row - 2][col], board[row - 1][col], board[row][col]),
                                     package_right_and_left_cells(board, row, col)]
    elif col == 1:
        self.__states[(row, col)] = [(board[row - 2][col], board[row - 1][col], board[row][col]),
                                     package_right_six_cells(board, row, col)]
    elif col == COLS_NB - 2:
        self.__states[(row, col)] = [(board[row - 2][col], board[row - 1][col], board[row][col]),
                                     package_right_six_cells(board, row, col - 3)]

elif row == ROWS_NB - 3:
    if 1 < col < COLS_NB - 2:
        self.__states[(row, col)] = [(board[row - 2][col], board[row - 1][col], board[row][col]),
                                     package_right_and_left_cells(board, row, col)]
    elif col == 1:
        self.__states[(row, col)] = [(board[row - 2][col], board[row - 1][col], board[row][col]),
                                     package_right_six_cells(board, row, col)]
    elif col == COLS_NB - 2:
        self.__states[(row, col)] = [(board[row - 2][col], board[row - 1][col], board[row][col]),
                                     package_right_six_cells(board, row, col - 3)]