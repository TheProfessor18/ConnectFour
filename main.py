from game import Game
from visualize import Visualization

newGame = Game()
vis = Visualization()

color = -1
while not newGame.over():
    vis.display(newGame.board)
    move = int(input(f"{color}, enter your move: "))
    if newGame.move(color, move):
        if color == -1:
            color = 1
        else:
            color = -1
print(f"The winner is {newGame.winner}")
