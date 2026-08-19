from game import Game
from agent import Agent

agent1 = Agent(1)
agent2 = Agent(-1)

for x in range(1000):
    game = Game()

    currentAgent = agent2
    while not game.over():
        #alternate agents
        if currentAgent == agent2:
            currentAgent = agent1
        else:
            currentAgent = agent2

        game.move(currentAgent.color, currentAgent.getMove(game.board))
        print(game.board)
    if game.winner == currentAgent.color:
        currentAgent.trainWin(game.board)

agent1.saveModel()

