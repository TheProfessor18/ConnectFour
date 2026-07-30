from game import Game
from model import Model

class Agent:

    def __init__(self, model, color):
        self.model = model
        self.color = color

    def action(self, board):

        #get the neural networks moves, and then compare to protective logic.
        boardForModel = board
        if self.color == -1:
            #invert board if playing second
            boardForModel *= -1

        modelMoves = self.model.result(boardForModel)

        #create a dummy game to test moves on.
        testGame = Game()

        # check all seven moves for obvious actions to do or avoid, could eventually extend much farther
        possibleMoves = []
        for x in range(7):
            testGame.board = board
            if testGame.move(self.color, x):
                if testGame.over():
                    #reward this move, and make it
                    #model.backpropogate()...
                    return x
                else:
                    enemyColor = self.color * -1
                    savedState = testGame.board
                    enemyCanWin = False
                    for o in range(7):
                        testGame.board = savedState
                        if testGame.move(enemyColor, o):
                            if testGame.over():
                                #punish allowing this move in the model, and prohibit moving here.
                                enemyCanWin = True
                                #model.backpropogate()
                    if not enemyCanWin:
                        #the opponent can't win with this move, so we'll allow it.
                        possibleMoves.append(x)





