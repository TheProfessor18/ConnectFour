from game import Game
from model import Model, Layer
from agent import Agent
from visualize import Visualization

game = Game()
model = Model([
            Layer(16, 42),
            Layer(16,16),
            Layer(16,16),
            Layer(7, 16)
        ])

player1 = Agent(model, 1,  6)
player2 = Agent(model, -1,  6)

color = 1
while not game.over(True):
    if color == 1:
        move = player1.action(game.board)
    else:
        move = player2.action(game.board)
    if game.move(color, move):
        color *= -1
    print(game.board)
print(f'Winner: {game.winner}.')
vis = Visualization()
vis.display(game.board)
vis.tk.mainloop()
