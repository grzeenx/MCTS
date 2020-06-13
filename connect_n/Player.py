import random
from MCTS.uct.algorithm.mc_tree import MonteCarloTree
from MCTS.uct.algorithm.mc_tree_search import MonteCarloTreeSearch
from connect_n.algotirhm_relay.connect_n_state import ConnectNState
from mcts_settings import MonteCarloSettings

class Player:
    def move(self, board, possible_moves):
        # !!! TUTAJ ZA POMOCA BOARDA POWINNISMY JAKOS POBRAC CONNECT_N_STATE
        # w boardzie jest caly stan a go przekazujemy tutaj

        current_state = ConnectNState(board)
        mcts = MonteCarloTreeSearch(MonteCarloTree(current_state), MonteCarloSettings())
        move, state, best_node = mcts.calculate_next_move()
        return move.move_number

        # return possible_moves[random.randint(0,len(possible_moves)-1)]
