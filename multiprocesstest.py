import multiprocessing
from treedatastorage import Database
from game import Game
from time import sleep
import numpy as np
from pickle import load, dump
from itertools import islice
import traceback

def backgroundSearch(conn):
    print('Background search starting...', flush=True)
    testGame = Game()

    try:
        with open('moveDatabase.pkl', 'rb') as file:
            database = load(file)
        print('Found database. Successfully loaded.')
    except FileNotFoundError:
        print('Making new database', flush=True)
        database = Database()

    if len(database.presentWorkingSet) == 0:
        # start off empty database
        legalMoves = testGame.legalMoves()
        database.newEntry('', testGame.board, np.array([]), np.array([]), legalMoves, 1)
    try:
        while True:
            #see if there's a new move
            if conn.poll():
                print(f'Message received')
                moveSequence, boardState = conn.recv()
                print('Actually recieved')
                try:
                    if database.entries[moveSequence].winningMoves.size != 0:
                        move = database.entries[moveSequence].winningMoves[0]
                    else:
                        move = database.entries[moveSequence].legalMoves[0]
                except:
                    traceback.print_exc()
                print(f'Moving to {move}')
                conn.send(move)
                database.updateFocus(moveSequence+str(move))

            #print("I'm running!", flush=True)
            #make sure each round doesn't take too long...
            movesToProcess = dict(islice(database.focus.items(), 1000))
            for key, data in movesToProcess.items():
                #print(f'Looking at {key}...', flush=True)
                testGame.board = np.copy(data.board)
                possibleMoves = np.setdiff1d(data.legalMoves, data.losingMoves) #Exclude losing moves from the check
                for move in possibleMoves:
                    testGame.board = np.copy(data.board)
                    testGame.move(data.colorToMove, move)
                    if testGame.over():
                        if testGame.winner == data.colorToMove: #This means a win, not a tie
                            np.append(database.presentWorkingSet[key].winningMoves, move)
                            np.append(database.parent(key).losingMoves, database.parentMove(key))
                            database.updateAncestors(key)
                    else:
                        legalMoves = testGame.legalMoves()
                        database.newEntry(key+str(move), np.copy(testGame.board), np.array([]), np.array([]), legalMoves, data.colorToMove * -1)
                database.demote(key)
    except:
        traceback.print_exc()
        with open('moveDatabase.pkl', 'wb') as file:
            dump(database, file)

if __name__ == '__main__':

    newGame = Game()
    color = 1

    mainConn, searchConn = multiprocessing.Pipe()

    background = multiprocessing.Process(target=backgroundSearch, args=(searchConn,))
    background.start()
    sleep(4)

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
    print(f'Game Over, winner: {newGame.winner}')

