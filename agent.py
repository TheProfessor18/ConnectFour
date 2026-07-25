
class Agent:

    def __init__(self, color):
        self.color = color

    def randomize(self):
        pass

    def mutate(self):
        pass

    def move(self, game):
        for x in range (7):
            #code to find best move, using x = 1 for best, x = 2 for second best etc...
            if (game.move(self.color, 7)):
                break

