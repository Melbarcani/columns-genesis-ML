"""
Platformer Game
"""
import arcade

# Constants
import numpy as np

from Agent import Agent
from Constant import *
import datetime
import random
import calendar
import time

import os

path = "C:/Users/admin/Documents"
SCREEN_TITLE = "COLUMNS"
CASE_RED = ":resources:images/cards/cardBack_red1.png"
CASE_BLUE = ":resources:images/cards/cardBack_blue1.png"
CASE_GREEN = ":resources:images/cards/cardBack_green1.png"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5


def create_board(row, cols):
    matrix = np.zeros((row, cols))
    matrix.astype(int)
    matrix[:] = 1
    return matrix


class Env:
    def __init__(self):
        self.board = create_board(5, 5)
        print(self.board)

    def reset(self):
        self.board = create_board(5, 5)


class ColumnWindow(arcade.Window):
    def __init__(self, environment, agent):
        self.__width = ROWS_NB * 64
        self.__height = COLS_NB * 64
        self.__environment = environment
        self.__agent = agent
        # Call the parent class and set up the window
        self.wall_list = None
        self.player_list = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        super().__init__(self.__width, self.__height, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

    def on_draw(self):
        """Render the screen."""
        # Clear the screen to the background color
        arcade.start_render()

        # Draw our sprites
        self.wall_list.draw()

    def on_update(self, delta_time: float):
        self.wall_list = None
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.__agent.reset()
        self.__environment.reset()
        self.__agent.score = 0
        env = self.__environment
        seconds = calendar.timegm(time.gmtime())
        while not env.isLost:
            self.__agent.reset()
            env.is_round_ended = False
            self.__agent.column = [random.randint(1, 3), random.randint(1, 3), random.randint(1, 3)]
            while not env.is_round_ended and not env.isLost:
                if seconds + 0.0001 < calendar.timegm(time.gmtime()):
                    seconds = calendar.timegm(time.gmtime())
                    env.apply(self.__agent, DOWN)
                else:
                    action = self.__agent.best_action()
                    env.apply(self.__agent, action)
            board = self.__environment.board
            print(board)
            for x in range(ROWS_NB):
                for y in range(COLS_NB):
                    if board[x][y] == GROUND:
                        wall = arcade.Sprite(":resources:images/tiles/brickTextureWhite.png", TILE_SCALING)
                        wall.center_x = 64 * y + 32
                        wall.center_y = 32
                        self.wall_list.append(wall)
                    elif board[x][y] == BORDER:
                        wall = arcade.Sprite(":resources:images/tiles/brickTextureWhite.png", TILE_SCALING)
                        wall.center_x = 64 * y + 32
                        wall.center_y = self.height - SPRITE_SIZE * (x + 0.5)
                        self.wall_list.append(wall)
                    elif board[x][y] == 1:
                        wall = arcade.Sprite(CASE_RED, TILE_SCALING)
                        wall.center_x = 64 * y + 32
                        wall.center_y = self.height - SPRITE_SIZE * (x + 0.5)
                        self.wall_list.append(wall)
                    elif board[x][y] == 2:
                        wall = arcade.Sprite(CASE_BLUE, TILE_SCALING)
                        wall.center_x = 64 * y + 32
                        wall.center_y = self.height - SPRITE_SIZE * (x + 0.5)
                        self.wall_list.append(wall)
                    elif board[x][y] == 3:
                        wall = arcade.Sprite(CASE_GREEN, TILE_SCALING)
                        wall.center_x = 64 * y + 32
                        wall.center_y = self.height - SPRITE_SIZE * (x + 0.5)
                        self.wall_list.append(wall)


if __name__ == '__main__':
    env = Env()
    window = ColumnWindow(env)
    window.setup()
    arcade.run()
    arcade.schedule(window.on_draw, 1 / 80)
