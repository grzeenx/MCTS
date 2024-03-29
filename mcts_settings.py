from MCTS.uct.algorithm.enums import MCTSVariant


class MonteCarloSettings:
    """
    Class is responsible for Monte Carlo algorithm settings.
    """
    def __init__(self):
        self.max_iterations = 150
        self.mcts_variant = MCTSVariant.UCB1_Tuned
        self.exploration_factor = 1.41
        self.rave_factor = 1
