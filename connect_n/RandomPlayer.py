import random
from connect_n.Player import Player


class RandomPlayer(Player):

    def move(self, board, possible_moves):
        return possible_moves[random.randint(0,len(possible_moves)-1)]
