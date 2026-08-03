import multiprocessing
from treedatastorage import Database
from game import Game
from time import sleep
import numpy as np
from pickle import load, dump
from itertools import islice

def backgroundSearch(conn):

    testGame = Game()

    try:
        with open('moveDatabase.pkl', 'rb') as file:
            database = load(file)
    except FileNotFoundError:
        database = Database()
    if len(database.presentWorkingSet) == 0:
        # start off empty database
        legalMoves = testGame.legalMoves()
        database.newEntry('', np.array([]), np.array([]), legalMoves, 1)

    while True:
        #see if there's a new move
        if conn.poll():
            moveSequence, boardState = conn.recv()
            database.updatePresentWorkingSet(moveSequence)
            testGame.board = np.copy(boardState)

        #make sure each round doesn't take too long...
        movesToProcess = dict(islice(database.presentWorkingSet.items(), 1000))

        for key, data in movesToProcess.values():
            #testGame.board = np.copy(data.board)
            for move in data.otherLegalMoves:
                testGame.board = np.copy(data.board)
                testGame.move(data.colorToMove, move)
                if testGame.over():
                    match testGame.winner:
                        case 0:
                            #tie
                            pass
                        case 1:
                            #win
                            pass
                        case -1:
                            #loss
                            pass




        conn.send(0)

if __name__ == '__main__':

    newGame = Game()

    mainConn, searchConn = multiprocessing.Pipe()

    background = multiprocessing.Process(target=backgroundSearch, args=(searchConn,))
    background.start()

    while not newGame.over():
        currentBoardState = np.copy(newGame.board)
        mainConn.send((newGame.moveSequence, currentBoardState))
        print('Move was made')
        print(currentBoardState)
        while np.array_equal(newGame.board, currentBoardState):
            sleep(4)
            move = mainConn.recv()
            newGame.move(-1, move)

