# from MCTS.uct.algorithm.mc_tree import MonteCarloTree
# from MCTS.uct.algorithm.mc_tree_search import MonteCarloTreeSearch
# from MCTS.uct.game.base_game_move import BaseGameMove
# from MCTS.uct.game.base_game_state import BaseGameState
# from mcts_settings import MonteCarloSettings
#
#
# class MonteCarloGameManager:
#     """
#     CLass is responsible for performing UCT algorithm moves and keeping information about game state and settings.
#     """
#
#     def __init__(self, game_state: BaseGameState, settings: MonteCarloSettings, board):
#         self.current_state = game_state
#         self.tree = MonteCarloTree(self.current_state)
#         self.settings = settings
#         self.first_move = True
#         self.previous_move_calculated = None
#         self.chosen_node = None
#         self.board = board
#
#     # def notify_move_performed(self, move: BaseGameMove):
#     #     """
#     #     Updates tree's nodes after player's move. It this is not the first move, it firstly updates the information
#     #     after last algorithm's move to keep consistency.
#     #
# 	# 	Args:
# 	# 		move:  BaseGameMove object
#     #
# 	# 	Returns:
# 	# 		None
# 	# 	"""
#     #     if self.first_move:
#     #         self.first_move = False
#     #         return
#     #     else:
#     #         self.tree.perform_move_on_root(self.previous_move_calculated)
#     #         self.tree.perform_move_on_root(move)
#     #         self.previous_move_calculated = None
#
#     def calculate_next_move(self):
#         """
#         Calculates algorithm's move with UCT algorithm.
#         Information about chosen move is stored after execution.
#
# 		Returns:
# 			calculated move, BaseGameMove object
# 		"""
#         mcts = MonteCarloTreeSearch(self.tree, self.settings)
#         move, state, best_node = mcts.calculate_next_move()
#         self.chosen_node = best_node
#         self.previous_move_calculated = move
#         return move
#
#     # def perform_algorithm_move(self):
#     #     """
#     #     Calculates next PC's move and performs it. It notifies other methods to update information in window, such as:
#     #     - game status label
#     #     - chosen node info.
#     #     It also informs whether the game is still in progress. If not, player cannot click and needs to start over.
#     #     :return: None
#     #     """
#     #     alg_move = self.calculate_next_move()
#     #     # self.canvas.perform_algorithm_move(alg_move)
#     #     phase = self.board.phase
#     #
#     #     # if phase != GamePhase.IN_PROGRESS:
#     #     #    self.canvas.set_player_can_click(False)
#     #     #    self.canvas.game_ended = True
