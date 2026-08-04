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
        database.newEntry('', testGame.board, np.array([]), np.array([]), legalMoves, 1)
    try:
        while True:
            #see if there's a new move
            if conn.poll():
                moveSequence, boardState = conn.recv()
                if database.entries[moveSequence].winningMoves.size != 0:
                    move = database.entries[moveSequence].winningMoves[0]
                else:
                    move = database.entries[moveSequence].legalMoves[0]
                conn.send(move)
                database.updatePresentWorkingSet(moveSequence+str(move))

            #print("I'm running!", flush=True)
            #make sure each round doesn't take too long...
            movesToProcess = dict(islice(database.presentWorkingSet.items(), 1000))
            for key, data in movesToProcess.items():
                #print(f'Looking at {key}...', flush=True)
                #testGame.board = np.copy(data.board)
                possibleMoves = np.setdiff1d(data.legalMoves, data.losingMoves) #Exclude losing moves from the check
                for move in possibleMoves:
                    testGame.board = np.copy(data.board)
                    testGame.move(data.colorToMove, move)
                    if testGame.over():
                        if testGame.winner == data.colorToMove: #This means a win, not a tie
                            np.append(data.winningMoves, move)
                            np.append(database.parent(key).losingMoves, database.parentMove(key))
                            database.updateAncestors(key)
                    else:
                        legalMoves = testGame.legalMoves()
                        database.newEntry(key+str(move), testGame.board, np.array([]), np.array([]), legalMoves, data.colorToMove * -1)
                database.demote(key)
    except Exception as e:
        with open('moveDatabase.pkl', 'wb') as file:
            dump(database, file)
        print(e, flush=True)



        conn.send(0)

if __name__ == '__main__':

    newGame = Game()
    color = 1

    mainConn, searchConn = multiprocessing.Pipe()

    background = multiprocessing.Process(target=backgroundSearch, args=(searchConn,))
    background.start()
    background.join()

    while not newGame.over():
        move = int(input('Enter you move'))
        newGame.move(color, move)
        color *= -1
        currentBoardState = np.copy(newGame.board)
        mainConn.send((newGame.moveSequence, currentBoardState))
        print(currentBoardState)
        move = mainConn.recv()
        print(f'Bot moved to {move}')
        newGame.move(color, move)
        print(newGame.board)
        color *= -1

