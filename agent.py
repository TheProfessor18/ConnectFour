from game import Game
from model import Model, Layer
import numpy as np
from pickle import dump, load


class Agent:

    def __init__(self, color, exploration = 0):
        self.color = color

        try:
            with open('modelData.pkl', 'rb') as file:
                self.model = load(file)
        except FileNotFoundError:
            self.model = Model([
                Layer(24, 42),
                Layer(24, 24),
                Layer(24, 24),
                Layer(24, 24),
                Layer(1, 24)
            ])
        self.exploration = exploration

    def getMove(self, board):
        testGame = Game()
        testGame.board = np.copy(board)

        #decide whether to explore to exploit
        if np.random.uniform(0,1) > self.exploration:
            possibleMoves = {}
            for move in testGame.legalMoves():
                testGame.board = np.copy(board)
                testGame.move(self.color, move)
                #add the best move, times own color so that the max will be the losest if playing as -1
                possibleMoves[move] = self.model.forward(np.reshape(testGame.board, 42)) * self.color
            bestMove = max(possibleMoves, key=possibleMoves.get)
            return bestMove
        else:
            return np.random.choice(testGame.legalMoves)

    def trainWin(self, board):
        #backpropogation
        self.model.backPropagate(np.reshape(board, 42), self.color)



    def saveModel(self):
        with open('modelData.pkl', 'wb') as file:
            dump(self.model, file)