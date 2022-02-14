"""
Platformer Game
"""
from time import sleep

import arcade
from matplotlib import pyplot as plt

from Agent import Agent
from Constant import *
import random

from Environment import Environment

path = "C:/Users/admin/Documents"
SCREEN_TITLE = "COLUMNS"
CASE_RED = ":resources:images/cards/cardBack_red1.png"
CASE_BLUE = ":resources:images/cards/cardBack_blue1.png"
CASE_GREEN = ":resources:images/cards/cardBack_green1.png"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5

PIXEL = 32


class ColumnWindow(arcade.Window):
    def __init__(self, environment, agent):
        self.__height = ROWS_NB * 64
        self.__width = COLS_NB * 64
        self.__environment = environment
        self.__agent = agent
        self.__iteration = 1
        # Call the parent class and set up the window
        self.wall_list = None
        super().__init__(self.__width, self.__height, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        # Create the Sprite lists
        env.reset()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

    def on_draw(self):
        """Render the screen."""
        # Clear the screen to the background color
        arcade.start_render()
        # arcade.draw_text(f"#{self.__iteration} Score : {self.__agent.score_break}",10, 10, arcade.csscolor.WHITE, 20)
        # Draw our sprites
        self.wall_list.draw()
        arcade.draw_text(f"#{self.__iteration} Score : {self.__agent.score_break}",
                         10, 10, arcade.csscolor.BLACK, 20)

    def on_update(self, delta_time: float):
        if env.isLost:
            agent.update_history()
            self.__agent.reset()
            self.reset_env()
        agent.resetPosition()
        env.is_round_ended = False
        agent.column = [random.randint(1, 3), random.randint(1, 3), random.randint(1, 3)]
        counter = 0
        old_action = DOWN
        while not env.is_round_ended:
            self.wall_list = arcade.SpriteList(use_spatial_hash=True)
            if counter > 3 and old_action != DOWN:  # every 3 actions column must get down
                env.apply(agent, DOWN)
                old_action = DOWN
                counter = 0
            else:
                action = agent.best_action()
                counter = (counter + 1) if action != DOWN else 0
                old_action = action
                env.apply(agent, action)
            self.draw_board(env.board)


    def draw_board(self, board):

        # "score break", agent.score_break afficher score agent
        for x in range(ROWS_NB - 1):
            for y in range(COLS_NB):
                if board[x][y] == GROUND:
                    wall = arcade.Sprite(":resources:images/tiles/brickTextureWhite.png", TILE_SCALING)
                    wall.center_x = 64 * y + 32
                    wall.center_y = self.height - SPRITE_SIZE * (x + 0.5)
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

    def reset_env(self):
        env.reset()
        self.__iteration += 1

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            plt.plot(agent.history)
            plt.show()

if __name__ == '__main__':
    env = Environment()
    agent = Agent(env)
    window = ColumnWindow(env, agent)
    window.setup()
    arcade.run()
    arcade.schedule(window.on_draw, 1 / 80)
