import os
import arcade
import pyglet

import MCTS
from connect_n.Board import Board
from connect_n.Player import Player


class ConnectN(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title, player_1=None, player_2=None):
        super().__init__(width, height, title)
        self.center_window()
        self.board = Board(8, 8, 4, player_1, player_2)


        arcade.set_background_color(arcade.color.BLUE_BELL)

        self.image_paths = [os.path.join("connect_n", "graphics", "field.jpg"),
                            os.path.join("connect_n", "graphics", "elisabeth2-coingreen.jpg"),
                            os.path.join("connect_n", "graphics", "elisabeth2-coin-pink.jpg")]

        field = arcade.Sprite(self.image_paths[0], 1)

        self.field_width = float(self.width / max(self.board.n_cols, self.board.n_rows))
        self.field_height = float((self.height - 20) / max(self.board.n_cols, self.board.n_rows))

        self.SPRITE_SCALING_COIN = self.field_width / field.width
        self.game_over = False
        self.move = None
        self.chosen_col_id = 0

    def center_window(self):
        """
        Taken from arcade docs to center the window
        Center the window on the screen.
        """
        # Get the display screen using pyglet
        screen_width, screen_height = self.get_display_size()

        window_width, window_height = self.get_size()
        # Center the window
        self.set_location((screen_width - window_width) // 2, (screen_height - window_height) // 2)

    def get_display_size(self):
        """
        Taken from arcade docs to get_display_size
         Return the resolution of the monitor
         """
        display = pyglet.canvas.Display()
        screen = display.get_default_screen()
        return screen.width, screen.height

    def setup(self):

        self.help_coin = arcade.Sprite(self.image_paths[1], self.SPRITE_SCALING_COIN)
        self.help_coin.alpha = 100
        self.help_coin.center_y = self.board.n_rows * self.field_height
        self.help_coin.center_x = self.field_width / 2

        self.field_list = arcade.SpriteList()
        for i in range(self.board.n_rows):
            for j in range(self.board.n_cols):
                field = arcade.Sprite(self.image_paths[0], self.SPRITE_SCALING_COIN)
                field.center_x = field.width / 2 + j * field.width
                field.center_y = field.height / 2 + i * field.height
                self.field_list.append(field)

        self.token_list = arcade.SpriteList()

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        self.field_list.draw()
        self.token_list.draw()
        self.help_coin.draw()
        # print score
        self.output = f"PLAYER {self.board.result} WON!" if self.game_over else ""
        arcade.draw_text(self.output, (self.board.n_cols / 2 - 0.5) * self.field_width,
                         (self.board.n_rows) * self.field_height, arcade.color.RED, 14, bold=True)

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        # help coin
        self.help_coin.center_x = self.field_width * (self.chosen_col_id + 0.5)
        self.help_coin.center_y = self.board.find_row(
            self.chosen_col_id) * self.field_height + self.field_height / 2 if self.board.find_row(
            self.chosen_col_id) < self.board.n_rows else -10000

        if self.game_over:
            self.help_coin.alpha = 0

        if not self.game_over:
            if self.board.active_player() is not None:
                # AI
                self.game_over = self.board.play()
                token = arcade.Sprite(self.image_paths[self.board.opposite_player(self.board.whos_turn_is_now)],
                                      self.SPRITE_SCALING_COIN)
                token.center_x = self.board.last_move[1] * self.field_width + self.field_width / 2
                token.center_y = self.board.last_move[0] * self.field_height + self.field_height / 2
                self.token_list.append(token)
            elif self.move is not None:

                # HUMAN
                self.game_over = self.board.play_human(self.move)
                token = arcade.Sprite(self.image_paths[self.board.opposite_player(self.board.whos_turn_is_now)],
                                      self.SPRITE_SCALING_COIN)
                token.center_x = self.board.last_move[1] * self.field_width + self.field_width / 2
                token.center_y = self.board.last_move[0] * self.field_height + self.field_height / 2
                self.token_list.append(token)
                self.move = None

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if self.board.active_player() is None:
            if key == arcade.key.ENTER:
                if self.chosen_col_id in self.board.give_possible_moves():
                    self.move = self.chosen_col_id
            elif key == arcade.key.LEFT:
                self.chosen_col_id = max(0, self.chosen_col_id - 1)
            elif key == arcade.key.RIGHT:
                self.chosen_col_id = min(self.chosen_col_id + 1, self.board.n_cols - 1)

    def run(self):
        arcade.run()
