from game import Game
from visualize import Visualization
from agent import Agent
from model import Model

newGame = Game()
vis = Visualization()
model = Model(4, 20)
agent = Agent(model, -1, 6)

color = 1
while not newGame.over():
    vis.display(newGame.board)
    if color == 1:
        move = int(input(f"{color}, enter your move: "))
    else:
        move = agent.action(newGame.board)
    #make the inputted move, but only change the player if the move is accepted.
    if newGame.move(color, move):
        color *= -1
    else:
        print('Invalid move, try again')
print(f"The winner is {newGame.winner}")
