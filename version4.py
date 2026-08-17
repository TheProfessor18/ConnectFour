from multiprocessing import Process, Pipe
from game import Game
from version3 import backgroundSearch
import numpy as np

def newEntry(key, board, legalMoves, winningMoves, losingMoves, colorToMove):
    return {'key': key, 'board': board, 'legalMoves':legalMoves, 'winningMoves':winningMoves, 'losingMoves':losingMoves, 'colorToMove':colorToMove}

def backgroundSearch(conn, agentColor):
    game = Game()
    testGame = Game()

    entries = {}
    positionsToProcess = [newEntry('', game.board, game.legalMoves(), [], [], 1)]
    newRound = []

    while not game.over():
        if conn.poll():
            message = conn.recv()
            if message == 'Ready':
                conn.send('Ready')
            else:
                newMove = message
                #movelogic


        for position in positionsToProcess:

            #check if the current position is relevant to the current game state
            if game.moveSequence in position['key']:
                for move in position['legalMoves']:
                    testGame.board = np.copy(game.board)
                    testGame.move(position['colorToMove'], move)
                    if testGame.over() and testGame.winner == position['colorToMove']:
                        position['winningMoves'].append(move)
                        entries[position['key'][:-1]]['losingMoves'].append(position['key'][-1])
                        if entries[]

                    else:
                        newKey = position['key']+str(move)
                        newPosition = newEntry(newKey, testGame.board, testGame.legalMoves(), [], [], position['colorToMove'] * -1)
                        entries[newKey] = newPosition
                        newRound.append(newPosition)
        positionsToProcess = np.copy(newRound)


if __name__ == '__main__':
    game = Game()

    agentColor = 1

    mainConn, backgroundConn = Pipe()
    backgroundSearch = Process(target=backgroundSearch(backgroundConn, agentColor))