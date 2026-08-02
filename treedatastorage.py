import numpy as np
from pickle import load, dump

class Database:
    def __init__(self):
        try:
            with open('moveDatabase.pkl', 'rb') as file:
                self.movesDatabase = load(file)
        except:
            self.entries = {}
    def save(self):
        with open('moveDatabase.pkl', 'wb') as file:
            dump(self.movesDatabase, file)

    class Entry:
        def __init__(self, key, boardstate):
            self.key = key
            self.board = boardstate
            self.parent = np.array([])

