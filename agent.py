from game import Game
from model import Model
import numpy as np

#go through and optimize this stuff later
from copy import deepcopy, copy

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

        modelMoves = self.model.forward(boardForModel)

        if self.color == -1:
            #set board back
            boardForModel *= -1

        #create a dummy game to test moves on.
        testGame = Game()

        # check all seven moves for obvious actions to do or avoid, could eventually extend much farther
        possibleMoves = np.array([])
        #boardCopy = np.copy(board)

        for x in range(7):
            testGame.board = np.copy(board)
            if testGame.move(self.color, x):
                if testGame.over() and testGame.winner == self.color:
                    #reward this move, and make it
                    #model.backpropogate() until it is the argmax
                    print(f'Found winning move: {x}')
                    #print(testGame.board)
                    return x
                else:
                    enemyColor = self.color * -1
                    savedState = np.copy(testGame.board)
                    enemyCanWin = False
                    for o in range(7):
                        testGame.board = np.copy(savedState)
                        #print(testGame.board)
                        if testGame.move(enemyColor, o):
                            if testGame.over() and testGame.winner == enemyColor:
                                print(f'Opponent can win if I go to {x} as {self.color}')
                                #punish allowing this move in the model, and prohibit moving here.
                                enemyCanWin = True
                                #model.backpropogate() until it is the argmin
                        else:
                            print('Illegal opponent move')
                    if not enemyCanWin:
                        print(f'Moving to {x} is safe')
                        #the opponent can't win with this move, so we'll allow it.
                        possibleMoves = np.append(possibleMoves, x)
            else:
                #move is illegal, probably adjust the model, but maybe not as aggresively.
                pass
                print(f'Illegal Move: {x}')

        print(possibleMoves)


        if possibleMoves.size == 0:
            #forced loss, very bad
            print('Forced loss or tie')
            testGame.board = board
            while not testGame.move(self.color, np.argmax(modelMoves)):
                modelMoves = np.delete(modelMoves, np.argmax(modelMoves))
            print(f'Moving to {np.argmax(modelMoves)} as {self.color}')
            return np.argmax(modelMoves)
        else:

            move = np.argmax(modelMoves)
            print(move)
            #clean this up
            while move not in possibleMoves:
                move = np.argmax(modelMoves)
                print(move)
                #possibleMoves = np.delete(possibleMoves, np.where(possibleMoves == np.argmax(modelMoves)))
                modelMoves[np.argmax(modelMoves)] = 0
                print(possibleMoves)
            print(f'Moving to {move} as {self.color}')
            return move




