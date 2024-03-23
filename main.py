from Game import Game


game = Game()
game.init()

while not game.is_game_over:
    print ("best move:" + str(game.get_ai_move()))