from game import Game
from model import Model
from agent import Agent

game = Game()
model = Model(4, 20)

player1 = Agent(model, 1)
player2 = Agent(model, -1)

color = 1
while not game.over():
    if color == 1:
        move = player1.action(game.board)
    else:
        move = player2.action(game.board)
    if game.move(color, move):
        color *= -1
    print(game.board)
print(f'Winner: {game.winner}.')
