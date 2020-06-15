from MCTS.uct.algorithm.mc_node_details import MonteCarloNodeDetails


class MonteCarloNode:
    """
    Class is responsible for storing information about a single node in Monte Carlo tree.
    """
    _node_counter = 0

    def __init__(self):
        """
        Public constructor shouldn't ever be called, use create_root instead
        """
        self.id = -1
        self.move = None
        self.details = MonteCarloNodeDetails()
        self.children = []
        self.parent = None

    def add_child_by_move(self, move, state_desc=""):
        """
        Adds child node to the node. New node represents given move.

		Args:
			move:  BaseGameMove object

		Returns:
			None        
		"""
        child = MonteCarloNode._create_instance(move)
        if state_desc != "":
            child.details.state_name = state_desc
        child.parent = self
        self.children.append(child)
        child.number = len(self.children)

    def add_child_by_node(self, child):
        """
        Adds child node to the node.

		Args:
			child:  MonteCarloNode object

		Returns:
			None        
		"""
        child.parent = self
        # child.vis_details.y = self.vis_details.y + 1
        self.children.append(child)
        child.number = len(self.children)

    def has_children(self):
        """
		Returns:
			bool informing if node has any children nodes        
		"""
        return len(self.children) > 0

    @staticmethod
    def create_root():
        """
		Returns:
			MonteCarloNode object representing root node (has no move assigned)        
		"""
        return MonteCarloNode._create_instance(None)

    @staticmethod
    def _create_instance(move):
        node = MonteCarloNode()
        node.id = MonteCarloNode.generate_next_id()
        node.move = move
        node.details = MonteCarloNodeDetails()
        node.children = []
        node.parent = None
        # if move:
        #     node.details.move_name = move.description
        return node

    @staticmethod
    def generate_next_id():
        """
		Returns:
			int, unique id for a node (starts from 1)        
		"""
        MonteCarloNode._node_counter = MonteCarloNode._node_counter + 1
        return MonteCarloNode._node_counter

    def get_siblings_with_itself(self):
        return self.parent.children if self.parent else []
