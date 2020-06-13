import random

from connect_n.Board import Board
from MCTS.uct.algorithm.enums import GamePhase
from MCTS.uct.game.base_game_state import BaseGameState
from connect_n.algotirhm_relay.connect_n_move import ConnectNMove


class ConnectNState(BaseGameState):
    def __init__(self, board: Board):
        super().__init__()
        self.board = board

    def get_all_possible_moves(self):
        possible_moves = []
        for value in self.board.give_possible_moves():
            possible_moves.append(ConnectNMove(value, self.board.whos_turn_is_now))
        return possible_moves

    def perform_random_move(self):
        # get all possible moves and random

        # all_possible_moves = self.get_all_possible_moves()
        # random_number = RandomUtils.get_random_int(0, len(all_possible_moves))
        # move = all_possible_moves[random_number]
        # self.board.perform_move(move[0])
        # self.switch_current_player()
        # self.phase = self.board.phase
        #
        # possible_moves = self.get_all_possible_moves()
        # eturn possible_moves[random.randint(0, len(possible_moves) - 1)]

        all_possible_moves = self.get_all_possible_moves()
        move = all_possible_moves[random.randint(0, len(all_possible_moves) - 1)]
        self.board.play_human(move.move_number)
        self.switch_current_player()
        self.phase = self.board.phase

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
        # return self.board.players.deepcopy(), self.board.whos_turn_is_now.deepcopy(), self.board.last_move.deepcopy(), self.board.board.deepcopy(), self.board.result.deepcopy()
