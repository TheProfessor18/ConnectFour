from multiprocessing import Process, Pipe
from game import Game
import numpy as np

class Database:
    def __init__(self):
        self.entries = {}
        self.focus = []

    def newEntry(self, rawboardState, parentBoardState, lastMove, colorToMove):
        boardState = str(rawboardState)
        if boardState not in self.entries:
            testGame = Game()
            testGame.board = np.copy(boardState)
            self.entries[boardState] = {'parent': [np.copy(parentBoardState)], 'lastMove': [lastMove], 'legalMoves': testGame.legalMoves(), 'winningMoves': [], 'losingMoves': [], 'forcedLoss': False, 'colorToMove': colorToMove}
        else:
            #if the entry already exists, add another parent to it
            self.entries[boardState]['parent'].append(np.copy(parentBoardState))
            self.entries[boardState]['lastMove'].append(lastMove)
        self.focus.append(self.entries[boardState])

    def checkForWinsandCreateChildren(self, rawboard):
        board = str(rawboard)
        if board not in self.entries:
            return False
        else:
            testGame = Game()
            positionToProcess = self.entries[np.copy(board)]
            for move in positionToProcess['legalMoves']:
                testGame.board = np.copy(board)
                testGame.move(positionToProcess['colorToMove'], move)
                if testGame.over() and testGame.winner == positionToProcess['colorToMove']:
                    positionToProcess['winningMoves'].append(move)

                    for lastMoveIndex, parent in enumerate(self.entries[positionToProcess['parent']]):
                        parent['losingMoves'].append(positionToProcess['lastMove'][lastMoveIndex])
                else:
                    self.newEntry(testGame.board, board, move, positionToProcess['colorToMove'] * -1)

            #check for a forced loss
            processing = True
            positionToCheckBack = positionToProcess
            while processing:
                for lastMoveIndex, parent in enumerate(self.entries[positionToCheckBack['parent']]):
                    parent['losingMoves'].sort()
                    parent['legalMoves'].sort()
                    if parent['losingMoves'] == parent['legalMoves']:
                        #add the last move to the grandparent's winning moves
                        grandparent = self.entries[parent['parent']]
                        grandparent['winningMoves'].append(parent['lastMove'])
                        self.entries[grandparent['parent']]['losingMoves'].append(self.entries[grandparent]['lastMove'])
                    else:
                        processing = False
                    positionToCheckBack = grandparent



            self.focus = self.focus[self.focus != positionToProcess]

if __name__ == '__main__':
    game = Game()
    database = Database()
    database.newEntry(game.board, None, None, 1)
    while True:
        for position in database.focus:
            database.checkForWinsandCreateChildren(position['board'])