from connect_n.ConnectN import ConnectN
from connect_n.AIPlayer import AIPlayer
from connect_n.HeuristicPlayer import HeuristicPlayer
from connect_n.RandomPlayer import RandomPlayer

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 720

SCREEN_TITLE = "Connect Four"

if __name__ == '__main__':
    game = ConnectN(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, player_1=None, player_2=AIPlayer())
    game.setup()
    game.run()
