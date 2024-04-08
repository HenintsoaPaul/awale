from Game import Game
from GameGUI import GameGUI

def main():
    game = Game()
    game.init()
    gui = GameGUI(game)
    gui.run()

if __name__ == "__main__":
    main()