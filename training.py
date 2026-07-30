from game import Game
from agent import Agent

game = Game()
agent = Agent()

color = 1
while not game.over():

    move = agent.action(game.board)
    if game.move(color, move):
        color *= -1
