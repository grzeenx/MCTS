from time import sleep
from MCTS.uct.algorithm.enums import GamePhase
from connect_n.Player import Player
from connect_n.Board import Board

WIN_REWARD = 10000000
DRAW_REWARD = 0
LOSS_REWARD = -WIN_REWARD
CENTER_FACTOR = 10
BAD_SEQ_FACTOR = -100
GOOD_SEQ_FACTOR = 20


class HeuristicPlayer(Player):

    def move(self, board, possible_moves):
        who_plays = board.whos_turn_is_now
        max_score_move = (self.evaluate(board, possible_moves[0], who_plays), possible_moves[0])
        for move in possible_moves:
            score = self.evaluate(board, move, who_plays)
            if score > max_score_move[0]:
                max_score_move = (score, move)
        # sleep(1)
        return max_score_move[1]

    def evaluate(self, board, move, who_plays):
        new_board = board.deep_copy()
        is_game_over = new_board.play_human(move)
        if is_game_over:
            if new_board.result == who_plays:
                return WIN_REWARD
            else:
                return DRAW_REWARD
        # globally - maybe try locally
        max_seq_good, max_free_good = new_board.count_the_longest_line(who_plays)

        possible_opponent_moves = new_board.give_possible_moves()
        max_seq_bad = 0
        max_free_bad =0
        for opponent_move in possible_opponent_moves:
            seq_bad, free_bad = self.longest_line_for_move(new_board, opponent_move, new_board.opposite_player(who_plays))
            if seq_bad == board.n_to_win:
                return LOSS_REWARD
            elif max_seq_bad< seq_bad:
                max_seq_bad=seq_bad
            elif free_bad==2 and max_seq_bad== seq_bad:
                max_seq_bad=seq_bad
                max_free_bad=free_bad
        # when is --oo-- putting a piece doesnt change the bad_seq_reward -> you have to give a positive or few steps ahead
        bad_seq_reward = LOSS_REWARD/4*max_free_bad if max_seq_bad == board.n_to_win-1 else BAD_SEQ_FACTOR*max_seq_bad*max_free_bad
        good_seq_reward = WIN_REWARD/8*max_free_good if max_seq_good == board.n_to_win-1 else GOOD_SEQ_FACTOR*max_seq_good*max_free_good
        return good_seq_reward+bad_seq_reward + self.center_reward(move, board.n_rows)

    def longest_line_for_move(self, board, move, player):
        new_board = board.deep_copy()
        new_board.play_human(move)
        return new_board.count_the_longest_line(player)

    def center_reward(self, move, n_rows):
        return - CENTER_FACTOR* abs((move+1) - (n_rows+1)/2)
