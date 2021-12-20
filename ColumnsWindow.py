"""
Platformer Game
"""
import arcade

# Constants
from Constants import *

SCREEN_TITLE = "COLUMNS"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5


class ColumnsWindow(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, environment):
        self.__width = COLS_NB * 64
        self.__height = ROWS_NB * 64
        self.__environment = environment

        # Call the parent class and set up the window
        super().__init__(self.__width, self.__height, SCREEN_TITLE)

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.wall_list = None
        self.player_list = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        # Create the ground
        # This shows using a loop to place multiple sprites horizontally
        board = self.__environment.board
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
                else:
                    wall = arcade.Sprite(":resources:images/cards/cardBack_red4.png", TILE_SCALING)
                    wall.center_x = 64 * y + 32
                    wall.center_y = self.height - SPRITE_SIZE * (x + 0.5)
                    self.wall_list.append(wall)

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        arcade.start_render()

        # Draw our sprites
        self.wall_list.draw()
        self.player_list.draw()
