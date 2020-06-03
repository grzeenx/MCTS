import random


class Player:
    def move(self, board, possible_moves):
        return possible_moves[random.randint(0,len(possible_moves)-1)]
