from MCTS.uct.game.base_game_move import BaseGameMove


class ConnectNMove(BaseGameMove):
    """
    Class is implementing BaseGameMove class methods in relation to mancala game.
    """
    def __init__(self, move_number, player):
        super().__init__()
        self.move_number = move_number
        self.player = player

    def move_equal(self, move) -> bool:
        # TU NIE WIEM CO MAM POROWNYWAC
        pass
