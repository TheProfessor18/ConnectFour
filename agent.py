from game import Game
from model import Model
import numpy as np
from math import log, floor
from pickle import load

class Agent:

    def __init__(self, model, color, startingforsight):
        self.model = model
        self.color = color
        tempGame = Game()
        self.normalMoveCount = len(tempGame.legalMoves())
        self.startingforsight = startingforsight



    def lookAhead(self, movesAhead, board, color):
        #if (board in self.movesDatabase):
        testGame = Game()
        testGame.board = np.copy(board)
        possibleMoves = testGame.legalMoves()
        canWin = False
        forcedLoss = False
        winningMoves = np.array([])
        losingMoves = np.array([])
        if movesAhead == 0:
            return False, False, np.array([]), np.array([])
        else:
            for move in possibleMoves:
                testGame.board = np.copy(board)
                testGame.move(color, move)
                if testGame.over() and testGame.winner == color:
                    canWin = True
                    winningMoves = np.append(winningMoves, move)
                else:
                    opponentCanWin, opponentForcedLoss, opponentWinningMoves, opponentLosingMoves = self.lookAhead(movesAhead - 1, testGame.board, color * -1)
                    if opponentCanWin:
                        losingMoves = np.append(losingMoves, move)
                    if opponentForcedLoss:
                        winningMoves = np.append(winningMoves, move)
                        canWin = True
            if np.array_equal(possibleMoves, losingMoves):
                forcedLoss = True
            return canWin, forcedLoss, winningMoves, losingMoves

    def action(self, board):
        #get the neural networks moves, and then compare to protective logic.
        if self.color == 1:
            boardForModel = board
        else:
            #invert board if playing second
            boardForModel = board * -1

        modelMoves = self.model.forward(boardForModel)

        testGame = Game()
        testGame.board = board
        legalMoves = testGame.legalMoves()

        #adjusts forsight depending on how many legal moves are left
        try:
            forsightMultiplier = log(self.normalMoveCount)/log(len(legalMoves))
        except:
            #eliminate the division by zero problem.
            forsightMultiplier = 1
        forsight = floor(self.startingforsight * (forsightMultiplier))

        lineToWin, doomed, winningMoves, losingMoves = self.lookAhead(forsight, board, self.color)

        if lineToWin:
            print(f'Winning line found at {int(winningMoves[0])}')
            #backpropogate to strengthen this move in the model
            return int(winningMoves[0])
        elif doomed:
            print('Game is lost, making random moves until end')
            return legalMoves[0]
        else:
            possibleMoves = legalMoves
            possibleMoves = np.setdiff1d(possibleMoves, losingMoves)
            for move in modelMoves:
                if np.argmax(modelMoves) in possibleMoves:
                    return np.argmax(modelMoves)
                else:
                    modelMoves[np.argmax(modelMoves)] = 0







