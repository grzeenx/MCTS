from connect_n.ConnectN import ConnectN
from connect_n.AIPlayer import AIPlayer
from connect_n.HeuristicPlayer import HeuristicPlayer
from connect_n.RandomPlayer import RandomPlayer
from mcts_settings import MonteCarloSettings
from MCTS.uct.algorithm.enums import GamePhase

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 720

SCREEN_TITLE = "Connect Four"

GAMES_NUM = 10

if __name__ == '__main__':
    with open("results.txt", 'a') as file:
        settings = MonteCarloSettings()
        # file.write(f"Heuristic vs AI max_iter:{settings.max_iterations}, variant:{settings.mcts_variant} \n")
        # file.write(f"Heuristic vs Random \n")
        file.write(f"Random vs AI max_iter:{settings.max_iterations}, variant:{settings.mcts_variant} \n")
        ai_scores = []
        for i in range(GAMES_NUM):
            game = ConnectN(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, player_1=RandomPlayer(), player_2=AIPlayer())
            game.setup()
            game.run()

            result = game.board.result
            if result == 0:
                ai_scores.append(0.5)
            elif result == 1:
                ai_scores.append(0)
            else:
                ai_scores.append(1)

        file.write(str(ai_scores) + '\n')
        # file.write(f"AI max_iter:{settings.max_iterations}, variant:{settings.mcts_variant} vs Heuristic \n")
        # file.write(f"Random vs Heuristic\n")
        file.write(f"AI max_iter:{settings.max_iterations}, variant:{settings.mcts_variant} vs Random \n")
        ai_scores=[]
        for i in range(GAMES_NUM):
            game = ConnectN(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, player_1=AIPlayer(), player_2=RandomPlayer())
            game.setup()
            game.run()
            result = game.board.result
            if result == 0:
                ai_scores.append(0.5)
            elif result == 1:
                ai_scores.append(1)
            else:
                ai_scores.append(0)
        file.write(str(ai_scores) +'\n')
