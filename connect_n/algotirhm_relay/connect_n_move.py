from MCTS.uct.game.base_game_move import BaseGameMove


class ConnectNMove(BaseGameMove):
    """
    Class is implementing BaseGameMove class methods in relation to mancala game.
    """
    def __init__(self, move_number, player, level=None):
        super().__init__()
        self.move_number = move_number
        self.player = player
        self.level = level

    def move_equal(self, move) -> bool:
        return self.move_number == move.move_number and self.player == move.player and self.level == move.level

    def __str__(self):
        return f'Col: {self.move_number}, level: {self.level}, player: {self.player}'
