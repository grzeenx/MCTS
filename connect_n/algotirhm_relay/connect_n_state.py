from connect_n.Board import Board
from MCTS.uct.algorithm.enums import GamePhase
from MCTS.uct.game.base_game_state import BaseGameState


class ConnectNState(BaseGameState):
    def __init__(self, board: Board):
        super().__init__()
        self.board = board

    def get_all_possible_moves(self):
        pass

    def perform_random_move(self):
        # get all possible moves and random
        pass

    def apply_moves(self, moves):
        # for move in moves:
        #     self.board.perform_move(move)
        # self.phase = self.board.phase
        pass

    def get_win_score(self, player):
        pass

    def deep_copy(self):
        pass
