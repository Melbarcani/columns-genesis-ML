# import Constants
#
#
# def get_column_agent(board, row, col):
#     array = [board[row][col]]
#     return get_column_helper(board, row, col, array, 0)
#
#
# def get_column_helper(board, row, col, array, counter):
#     if counter < 2 and row != 0:
#         array.append(board[row - 1][col])
#         get_column_helper(board, row - 1, col, array, counter + 1)
#         return array
#
#
# def get_nearest_cells(board, row, col):
#     array = []
#     return get_nearest_cells_recursive_helper(board, row, col, 0, array)
#
#
# def get_nearest_cells_recursive_helper(board, row, col, row_count, array):
#     if row_count < 2 and row == Constants.ROWS_NB - 2 and len(array) < 3:
#         print()
#         # get_cells_when_too_close_to_ground(array, board, col, row)
#     elif row_count < 2 and row == Constants.ROWS_NB - 2 and len(array) == 3:
#         print()
#         # array.append(package_right_and_left_four_cells(board, row, col))
#     elif row_count < 2 and row < Constants.ROWS_NB - 2:
#         get_nearest_cells_recursive_helper(board, row + 1, col, row_count + 1, array)
#         get_regular_cells(array, board, col, row, row_count)
#     return array
#
#
# def get_regular_cells(array, board, col, row, row_count):
#     if col > 1 + row_count:
#         array.append(board[row + 1][col - 1 - row_count])
#     array.append(board[row + 1][col])
#     if col < Constants.COLS_NB - 1 - row_count:
#         if board[row + 1][col + 1 + row_count] != Constants.BORDER:
#             array.append(board[row + 1][col + 1 + row_count])
#
#
# class EnvState:
#     def __init__(self, board, row, col):
#         self.__board = board
#         self.__position = [row, col]
#         self.__column_agent = get_column_agent(board, row, col)
#         self.__nearest_cells = get_nearest_cells(board, row, col)
#
#     @property
#     def column_agent(self):
#         return self.__column_agent
#
#     @column_agent.setter
#     def column_agent(self, ):
