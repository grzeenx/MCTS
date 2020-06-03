
from uct.algorithm.mc_node import MonteCarloNode
from uct.game.base_game_move import BaseGameMove
from uct.game.base_game_state import BaseGameState


class MonteCarloTree:
    """
    Class stores the information of the root of the Monte Carlo tree and about game state, and visualization data.
    """
    def __init__(self, game_state: BaseGameState = None, root: MonteCarloNode = None):
        if game_state is not None:
            self.root = MonteCarloNode.create_root()
            self.game_state = game_state
        else:
            self.game_state = None
            self.root = root

    def retrieve_node_game_state(self, node: MonteCarloNode):
        """
        Returns game state after the move from the given node was executed. This is an optimization to save memory and
        to not keep track of every game state from every possible move.

		Args:
			node:  MonteCarloNode object

		Returns:
			BaseGameState object, deep copy of the state with applied moves from the root to the given node        
		"""
        tmp_node = node
        moves = []
        while tmp_node != self.root:
            moves.append(tmp_node.move)
            tmp_node = tmp_node.parent

        rc = self.game_state.deep_copy()
        rc.apply_moves(moves[::-1])
        return rc

    def perform_move_on_root(self, move: BaseGameMove):
        """
        Moves the root to the node with newly executed move.
        If the node was absent, even though it was chosen by the algorithm, it is artificially added.

		Args:
			move:  BaseGameMove object with move to be performed

		Returns:
			None        
		"""
        next_root = None
        for child in self.root.children:
            if move.move_equal(child.move):
                next_root = child
                break

        if next_root is None:
            self.root.add_child_by_move(move)
            if len(self.root.children) > 1:
                raise RuntimeError("Why wouldn't you find your move?")
            next_root = self.root.children[0]
        self.root = next_root
