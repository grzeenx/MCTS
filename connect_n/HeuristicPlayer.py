from connect_n.Player import Player


class HeuristicPlayer(Player):

    def move(self, board, possible_moves):
        max_score_move = (self.evaluate(board, possible_moves[0]), possible_moves[0])
        for move in possible_moves:
            score = self.evaluate(board,move)
            if score> max_score_move[0]:
                max_score_move= (score, move)
        return max_score_move[1]

    def evaluate(self, board, move):
        return 10
        # if wins:
        #     return 1000000
        # if loses:
        #     return -1000000
        # # new(!) or globally?
        # h = count_how_many_inline_after_move()
        # c = how_close_to _centre()
        # return h + c
