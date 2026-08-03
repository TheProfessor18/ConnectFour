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
        pass
        #make this move an item from the working set into the main database

    def newEntry(self, key, board, winningMoves, losingMoves, otherLegalMoves, colortoMove):
        self.presentWorkingSet[key] = self.Entry(board, winningMoves, losingMoves, otherLegalMoves, colortoMove)

    class Entry:
        def __init__(self, board, winningMoves, losingMoves, otherLegalMoves, colortoMove):
            self.board = board
            self.winningMoves = winningMoves
            self.losingMoves = losingMoves
            self.otherLegalMoves = otherLegalMoves
            self.colortoMove = colortoMove

