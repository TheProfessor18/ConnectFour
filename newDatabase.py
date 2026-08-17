import numpy as np
from game import Game

def join(beginning, end):
    return int(str(beginning) + str(end))

class Database:
    def __init__(self):
        self.entries = {}

    def getPositionData(self, moveSequence):
        positionDict = self.entries
        for move in moveSequence:
            positionDict = positionDict[move]
        return positionDict['Data']

    def newEntry(self, moveSequence, board, colorToMove):
        testGame = Game()
        testGame.board = board
        legalMoves = testGame.legalMoves()
        positionDict = self.entries
        for move in str(moveSequence)[:-1]:
            positionDict = positionDict[str(move)]
            #print(positionDict)
        entry = self.Entry(moveSequence ,board, np.array([]), np.array([]), legalMoves, colorToMove)
        positionDict[moveSequence[-1]] = {}
        positionDict[moveSequence[-1]]['Data'] = entry
        return entry

    def getAncestor(self, moveSequence, generationsBack):
        return self.getPositionData(moveSequence[:-generationsBack])

    def updateAncestors(self, moveSequence):
        ancestorData = self.getAncestor(moveSequence, 1)
        if np.array_equal(ancestorData.legalMoves, ancestorData.losingMoves):
            fartherAncestorData = self.getAncestor(moveSequence, 2)
            fartherAncestorData.winningMoves = np.append(fartherAncestorData.winningMoves, ancestorData.moveSequence[-1])
            evenFartherAncestorData = self.getAncestor(moveSequence, 3)
            evenFartherAncestorData.losingMoves = np.append(evenFartherAncestorData.losingMoves, ancestorData.moveSequence[-2])
            self.updateAncestors(moveSequence[:-2])

    class Entry:
        def __init__(self, moveSequence, board, winningMoves, losingMoves, legalMoves, colorToMove):
            self.moveSequence = moveSequence
            self.board = board
            self.winningMoves = winningMoves
            self.losingMoves = losingMoves
            self.legalMoves = legalMoves
            self.colorToMove = colorToMove

        def printData(self):
            print(f'Entry data move sequence: {self.moveSequence}')
            print(f'Entry data board state: {self.board}')
            print(f'Entry data winning: {self.winningMoves}')
            print(f'Entry data losing moves: {self.losingMoves}')
            print(f'Entry data color to move: {self.colorToMove}')

