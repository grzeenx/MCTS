from MCTS.uct.algorithm.mc_tree import MonteCarloTree
from MCTS.uct.algorithm.mc_tree_search import MonteCarloTreeSearch
from connect_n.Player import Player
from connect_n.algotirhm_relay.connect_n_state import ConnectNState
from mcts_settings import MonteCarloSettings


class AIPlayer(Player):
    def move(self, board, possible_moves):
        current_state = ConnectNState(board)
        monte_carlo_tree = MonteCarloTree(current_state)
        mcts = MonteCarloTreeSearch(monte_carlo_tree, MonteCarloSettings())
        move, state, best_node = mcts.calculate_next_move()
        return move.move_number
