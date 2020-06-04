import random

from connect_n.Board import Board
from MCTS.uct.algorithm.enums import GamePhase
from MCTS.uct.game.base_game_state import BaseGameState


class ConnectNState(BaseGameState):
    def __init__(self, board: Board):
        super().__init__()
        self.board = board

    def get_all_possible_moves(self):
        return self.board.give_possible_moves()

    def perform_random_move(self):
        # get all possible moves and random
        possible_moves = self.get_all_possible_moves()
        return possible_moves[random.randint(0, len(possible_moves) - 1)]

    def apply_moves(self, moves):
        # for move in moves:
        #     self.board.perform_move(move)
        # self.phase = self.board.phase
        pass

    def get_win_score(self, player):
        pass

    def deep_copy(self):
        return self.board.players.deepcopy(), self.board.whos_turn_is_now.deepcopy(), self.board.last_move.deepcopy(), self.board.board.deepcopy(), self.board.result.deepcopy()
