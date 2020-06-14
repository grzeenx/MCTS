from connect_n.ConnectN import ConnectN
from connect_n.Player import Player

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 720

SCREEN_TITLE = "Connect4"

if __name__ == '__main__':
    game = ConnectN(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, player_1=None, player_2=Player())
    game.setup()
    game.run()
