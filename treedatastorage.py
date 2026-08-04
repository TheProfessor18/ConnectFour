import numpy as np
from pickle import load, dump

class Database:
    def __init__(self):
        self.entries = {}
        self.presentWorkingSet = self.entries

    def save(self):
        with open('moveDatabase.pkl', 'wb') as file:
            dump(self.movesDatabase, file)

    def updatePresentWorkingSet(self, key):
        #this can be optimized later
        self.presentWorkingSet = {k: v for k, v in self.presentWorkingSet.items() if k.startswith(key)}

    def demote(self, key):
        self.entries[key] = self.presentWorkingSet[key]
        self.presentWorkingSet.pop(key)

    def parent(self, key, generationsBack = 1):
        #gets the one before
        return self.entries[key[:-generationsBack]]

    def parentMove(self, key, generationsBack = 1):
        return key[-generationsBack]

    def updateAncestors(self, key):
        #check for forced loss
        parentdata = self.parent(key)
        if parentdata.legalMoves == parentdata.losingMoves:
            np.append(self.parent(key, 2).winningMoves, self.parentMove(key, 2))
            np.append(self.parent(key, 3).losingMoves, self.parentMove(key, 3))
            self.updateAncestors(key[:-2])

    def newEntry(self, key, board, winningMoves, losingMoves, legalMoves, colortoMove):
        self.presentWorkingSet[key] = self.Entry(board, winningMoves, losingMoves, legalMoves, colortoMove)

    class Entry:
        def __init__(self, board, winningMoves, losingMoves, legalMoves, colortoMove):
            self.board = board
            self.winningMoves = winningMoves
            self.losingMoves = losingMoves
            self.legalMoves = legalMoves
            self.colortoMove = colortoMove

