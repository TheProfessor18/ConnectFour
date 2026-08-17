import numpy as np
from pickle import load, dump
from copy import copy, deepcopy

class Database:
    def __init__(self):
        self.entries = {}
        self.presentWorkingSet = {}
        self.focus = {}

    def save(self):
        with open('moveDatabase.pkl', 'wb') as file:
            dump(self.movesDatabase, file)

    def updateFocus(self, key):
        #this can be optimized later
        self.focus = {k: v for k, v in self.presentWorkingSet.items() if k.startswith(key)}

    def demote(self, key):
        self.entries[key] = self.presentWorkingSet.pop(key)
        self.focus.pop(key)

    def parent(self, key, generationsBack = 1):
        #gets the one before
        return self.entries[key[:-generationsBack]]

    def parentMove(self, key, generationsBack = 1):
        return int(key[-generationsBack])

    def updateAncestors(self, key):
        #check for forced loss
        parentdata = self.parent(key)
        if np.array_equal(parentdata.legalMoves, parentdata.losingMoves):
            self.parent(key, 2).winningMoves = np.append(self.parent(key, 2).winningMoves, self.parentMove(key, 2))
            self.parent(key, 3).losingMoves = np.append(self.parent(key, 3).losingMoves, self.parentMove(key, 3))
            self.updateAncestors(key[:-2])

    def newEntry(self, key, board, winningMoves, losingMoves, legalMoves, colorToMove):
        self.presentWorkingSet[key] = self.Entry(board, winningMoves, losingMoves, legalMoves, colorToMove)
        self.focus[key] = self.Entry(board, winningMoves, losingMoves, legalMoves, colorToMove)

    class Entry:
        def __init__(self, board, winningMoves, losingMoves, legalMoves, colorToMove):
            self.board = board
            self.winningMoves = winningMoves
            self.losingMoves = losingMoves
            self.legalMoves = legalMoves
            self.colorToMove = colorToMove

