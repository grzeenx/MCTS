import os
import arcade
import MCTS
from connect_n.Board import Board
from connect_n.Player import Player


class ConnectN(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.board = Board(8, 8, 4, None, Player())
        arcade.set_background_color(arcade.color.BLUE_BELL)

        self.image_paths = [os.path.join("connect_n", "graphics", "field.jpg"),
                            os.path.join("connect_n", "graphics", "elisabeth2-coingreen.jpg"),
                            os.path.join("connect_n", "graphics", "elisabeth2-coin-pink.jpg"),
                            os.path.join("connect_n", "graphics", "arrow.jpg")]

        field = arcade.Sprite(os.path.join("connect_n", "graphics", "elisabeth2-coin-pink.jpg"), 1)

        self.field_width = float(self.width / max(self.board.n_cols, self.board.n_rows))
        self.field_height = float((self.height - 20) / max(self.board.n_cols, self.board.n_rows))

        self.SPRITE_SCALING_COIN = self.field_width / field.width
        self.game_over = False
        self.move = None
        self.chosen_col_id = 0

    def setup(self):
        self.arrow = arcade.Sprite(self.image_paths[3], self.SPRITE_SCALING_COIN)
        self.arrow.center_y = self.board.n_rows * self.field_height
        self.arrow.center_x = self.field_width / 2


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
        self.arrow.draw()
        self.output = f"Player {self.board.result} won" if self.game_over else ""
        arcade.draw_text(self.output, (self.board.n_rows/2-1) * self.field_height, (self.board.n_cols) * self.field_width, arcade.color.BLACK, 24)

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """

        # arrow
        self.arrow.center_x = self.field_width * (self.chosen_col_id + 0.5)

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
