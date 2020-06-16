import random

from connect_n.Board import Board
from MCTS.uct.game.base_game_state import BaseGameState
from connect_n.algotirhm_relay.connect_n_move import ConnectNMove


class ConnectNState(BaseGameState):
    def __init__(self, board: Board):
        super().__init__()
        self.board = board
        self.current_player = board.whos_turn_is_now

    def get_all_possible_moves(self):
        possible_moves = []
        for value in self.board.give_possible_moves():
            possible_moves.append(ConnectNMove(value, self.board.whos_turn_is_now, self.board.find_row(value)))
        return possible_moves

    def perform_random_move(self):
        all_possible_moves = self.get_all_possible_moves()
        move = all_possible_moves[random.randint(0, len(all_possible_moves) - 1)]
        self.board.play_human(move.move_number)
        self.switch_current_player()
        self.phase = self.board.phase
        return move

    def apply_moves(self, moves):
        for move in moves:
            self.board.play_human(move.move_number)
        self.phase = self.board.phase
        pass

    def get_win_score(self, player):
        pass

    def deep_copy(self):
        new_board = self.board.deep_copy()
        rc = ConnectNState(new_board)
        rc.phase = self.phase
        rc.current_player = self.board.whos_turn_is_now
        return rc
