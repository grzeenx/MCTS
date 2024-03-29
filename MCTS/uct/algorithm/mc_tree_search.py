from math import sqrt, log
import numpy as np

import MCTS.uct.algorithm.enums as Enums
import MCTS.uct.algorithm.mc_node_utils as NodeUtils
from MCTS.uct.algorithm.mc_simulation_result import MonteCarloSimulationResult
from MCTS.uct.algorithm.mc_tree import MonteCarloTree
from MCTS.uct.game.base_game_move import BaseGameMove
from MCTS.uct.game.base_game_state import BaseGameState
from mcts_settings import MonteCarloSettings


class MonteCarloTreeSearch:
    """
    Class responsible for executing four steps of the Monte Carlo Tree Search method in an iterative way.
    """

    def __init__(self, tree: MonteCarloTree, settings: MonteCarloSettings):
        self.tree = tree
        self.settings = settings
        self.iterations = 0
        self.moves_in_iteration = []

    def calculate_next_move(self) -> (BaseGameMove, BaseGameState):
        """
        Depending on the user settings, function calculates the best move for a computer using UCT algorithm.\
        It is calculated by limiting maximum iterations number or by the given time limit.
        The calculation process covers 4 phases: selection, expansion, simulation and backpropagation.

		Returns:
			tuple of (BaseGameMove, BaseGameState, MonteCarloNode) of the chosen move        
		"""
        while self.iterations < self.settings.max_iterations:
            self._perform_iteration()
        return self._select_result_node()

    def _perform_iteration(self):
        """
        Performs single UCT algorithm iteration.
        Execution consists of four steps: selection, expansion, simulation and backpropagation.

		Returns:
			None        
		"""
        promising_node = self._selection(self.tree.root)
        expansion_possible, state = self._expansion(promising_node)
        if not expansion_possible:
            simulation_result = MonteCarloSimulationResult(state)
            self._backpropagation(promising_node, simulation_result)
            self.iterations += 1
            return

        if promising_node.has_children():
            leaf_to_explore = NodeUtils.get_random_child(promising_node)
        else:
            leaf_to_explore = promising_node

        simulation_result = self._simulation(leaf_to_explore)
        self._backpropagation(leaf_to_explore, simulation_result)

        self.iterations += 1

    def _select_result_node(self):
        """
        Selects the best UCT node and retrieves game state of that node. The turn is switched afterwards in the
        resulting game state.

		Returns:
			tuple of (BaseGameMove, BaseGameState, MonteCarloNode) of the chosen move        
		"""
        best_child = NodeUtils.get_child_with_max_score(self.tree.root)

        result_game_state = self.tree.retrieve_node_game_state(best_child)
        result_game_state.switch_current_player()
        result_move = best_child.move
        return result_move, result_game_state, best_child

    def _selection(self, node):
        """
        Executes 1st stage of MCTS.
        Starts from root R and selects successive child nodes until a leaf node L is reached.

		Args:
			node:  node from which to start selection

		Returns:
			UCT-best leaf node        
		"""
        tmp_node = node
        while tmp_node.has_children() != 0:
            tmp_node = self._find_best_child_with_uct(tmp_node)
        return tmp_node

    def _expansion(self, node):
        """
        Executes 2nd stage of MCTS.
        Unless L ends the game, creates one (or more) child nodes and chooses node C from one of them.

		Args:
			node:  node from which to start expanding

		Returns:
			None        
		"""
        node_state = self.tree.retrieve_node_game_state(node)
        possible_moves = node_state.get_all_possible_moves()

        if node_state.board.phase != Enums.GamePhase.IN_PROGRESS:
            return False, node_state
        for move in possible_moves:
            node.add_child_by_move(move)

        return True, node_state

    def _simulation(self, leaf) -> MonteCarloSimulationResult:
        """
        Executes 3rd stage of MCTS.
        Complete a random playout from node C.

		Args:
			leaf:  leaf from which to process a random playout

		Returns:
			None        
		"""
        leaf_state = self.tree.retrieve_node_game_state(leaf)
        tmp_state = leaf_state.deep_copy()
        tmp_phase = leaf_state.phase

        moves_counter = 0
        self.moves_in_iteration = []
        while tmp_phase == Enums.GamePhase.IN_PROGRESS:
            move = tmp_state.perform_random_move()
            tmp_phase = tmp_state.phase
            moves_counter += 1
            self.moves_in_iteration.append(move)
        return MonteCarloSimulationResult(tmp_state)

    def _backpropagation(self, leaf, simulation_result: MonteCarloSimulationResult):
        """
        Executes 4th stage of MCTS.
        Uses the result of the playout to update information in the nodes on the path from C to R.

		Args:
			leaf:  leaf from which to start backpropagating
			simulation_result:  result of random simulation simulated from 

		Returns:
			None        
		"""
        leaf_state = self.tree.retrieve_node_game_state(leaf)
        leaf_player = leaf_state.current_player
        if simulation_result.phase == Enums.get_player_win(leaf_player):
            reward = 1
        elif simulation_result.phase == Enums.GamePhase.DRAW:
            reward = 0.5
        else:
            reward = 0

        tmp_node = leaf
        while tmp_node != self.tree.root:
            self.moves_in_iteration.insert(0, tmp_node.move)
            tmp_node.details.mark_visit()

            if self.settings.mcts_variant == Enums.MCTSVariant.RAVE:
                for sibling in tmp_node.get_siblings_with_itself():
                    for move_in_iteration in self.moves_in_iteration:
                        if sibling.move.move_equal(move_in_iteration):
                            sibling.details.mark_rave_visit()
                            break

            tmp_current_player = tmp_node.move.player
            if leaf_player == tmp_current_player:
                tmp_node.details.add_score(reward)

                if self.settings.mcts_variant == Enums.MCTSVariant.RAVE:
                    for sibling in tmp_node.get_siblings_with_itself():
                        for move_in_iteration in self.moves_in_iteration:
                            if sibling.move.move_equal(move_in_iteration):
                                sibling.details.add_rave_score(reward)
                                break

            tmp_node = tmp_node.parent
        self.tree.root.details.mark_visit()

    def _find_best_child_with_uct(self, node):
        """
        Calculates UCT value for children of a given node, with the formula:
        uct_value = (win_score / visits) + 1.41 * sqrt(log(parent_visit) / visits)
        and returns the most profitable one.

		Args:
			node:  MonteCarloNode object

		Returns:
			MonteCarloNode node with the best UCT calculated value        
		"""

        def uct_value(n, p_visit, exp_par):
            visits = n.details.visits_count
            win_score = n.details.win_score
            average_prize = n.details.average_prize if self.tree.game_state.current_player == \
                                                       n.move.player else -n.details.average_prize
            if visits == 0:
                return 10000000
            else:
                uct_val = average_prize + exp_par * sqrt(log(p_visit) / visits)
                return uct_val

        def ucb_tuned_value(n, p_visit):
            visits = n.details.visits_count
            win_score = n.details.win_score
            if visits == 0:
                return 10000000
            else:
                variance = np.var(n.details.scores)
                factor = variance + sqrt(2 * log(p_visit) / visits)
                ucb_factor = sqrt(min(0.25, factor))
                uct_val = ucb_factor * sqrt(log(p_visit) / visits)
                return uct_val

        def rave_value(n, p_visit, exp_par, rave_factor):
            visits = n.details.visits_count
            if visits == 0:
                return 10000000
            win_score = n.details.win_score
            rave_visits = n.details.rave_visits_count if n.details.rave_visits_count > 0 else 10000000
            rave_score = n.details.rave_win_score
            beta = rave_visits / (visits + rave_visits + 4 * rave_factor ** 2 * visits * rave_visits)
            rave_val = (1 - beta) * (win_score / visits) + beta * (rave_score / rave_visits) + exp_par * sqrt(
                log(p_visit) / visits)
            return rave_val

        parent_visit = node.details.visits_count
        if self.settings.mcts_variant == Enums.MCTSVariant.UCT:
            best_child_node = max(node.children,
                                  key=lambda n: uct_value(n, parent_visit, self.settings.exploration_factor))
        elif self.settings.mcts_variant == Enums.MCTSVariant.UCB1_Tuned:
            best_child_node = max(node.children,
                                  key=lambda n: ucb_tuned_value(n, parent_visit))
        elif self.settings.mcts_variant == Enums.MCTSVariant.RAVE:
            best_child_node = max(node.children,
                                  key=lambda n: rave_value(n, parent_visit, self.settings.exploration_factor,
                                                           self.settings.rave_factor))
        else:
            raise Exception('Undefined node selection method')
        return best_child_node
