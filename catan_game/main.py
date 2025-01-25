from game import *

# Create the game and check that the board is set up correctly
game = Game(10)
game.board.display_board()
for i in range(9):
    print(game.step())
    print(game.board.display_board())