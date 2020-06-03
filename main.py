from connect_n.ConnectN import ConnectN

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 720

if __name__ == '__main__':
    game = ConnectN(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    game.run()
