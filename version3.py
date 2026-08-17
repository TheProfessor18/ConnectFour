import multiprocessing
from game import Game
from newDatabase import Database, join
import numpy as np
import traceback
from time import sleep

def backgroundSearch(conn, myColor):

    game = Game()
    testGame = Game()
    moveSequence = ''
    movesToProcess = np.array([])

    database = Database()

    #Populate intial possible moves
    for move in game.legalMoves():
        testGame.board = np.copy(game.board)
        testGame.move(1, move)
        movesToProcess = np.append(movesToProcess, database.newEntry(str(move), testGame.board, -1))
    database.entries['Data'] = Database.Entry(moveSequence, game.board, np.array([]), np.array([]), game.legalMoves(), 1)

    while True:
        if True:
            if conn.poll():
                print(moveSequence)
                message = conn.recv()
                if message == 'Main program ready.':
                    conn.send('Sub process ready.')
                else:
                    newMove = message
                    game.move(myColor * -1, int(newMove))
                    moveSequence = game.moveSequence

                    positionData = database.getPositionData(moveSequence)
                    print(f'Gotten with {moveSequence}')
                    positionData.printData()
                    if len(positionData.winningMoves) != 0:
                        agentMove = positionData.winningMoves[0]
                    else:
                        possibleMoves = np.setdiff1d(positionData.legalMoves, positionData.losingMoves)
                        agentMove = possibleMoves[0]

                    game.move(myColor, agentMove)
                    conn.send(agentMove)

                    moveSequence += str(agentMove)

            for position in movesToProcess[:200]:
                movesToProcess = movesToProcess[movesToProcess != position]

                #skip any irrelevant positions
                if moveSequence not in position.moveSequence:
                    continue

                testGame.board = np.copy(position.board)
                colorToMove = position.colorToMove
                for move in testGame.legalMoves():
                    testGame.board = np.copy(position.board)
                    testGame.move(colorToMove, move)
                    if testGame.over() and testGame.winner == colorToMove:
                        #print(f'Win found at {testGame.moveSequence}')
                        position.winningMoves = np.append(position.winningMoves, int(move))
                        opponentData = database.getAncestor(position.moveSequence, 1)
                        opponentData.losingMoves = np.append(opponentData.losingMoves, int(opponentData.moveSequence[-1]))
                    else:
                        try:
                            movesToProcess = np.append(movesToProcess, database.newEntry((position.moveSequence + str(move)), testGame.board, colorToMove * -1))
                            #print(f'Found {(position.moveSequence + str(move))}')
                        except KeyError:
                            print(f"Couldn't find {(position.moveSequence + str(move))}")
                            traceback.print_exc()
                    testGame.undoLastMoveinSequence()
                database.updateAncestors(position.moveSequence)





if __name__ == '__main__':

    game = Game()

    agentColor = -1

    mainConn, searchConn = multiprocessing.Pipe()

    backgroundprocess = multiprocessing.Process(target=backgroundSearch, args=(searchConn, agentColor))
    backgroundprocess.start()

    mainConn.send('Main program ready.')

    ready = False
    while not ready:
        if mainConn.poll():
            if mainConn.recv() == 'Sub process ready.':
                ready = True

    color = 1
    playerMove = ''
    while not game.over():
        print(game.board)
        if color == agentColor:
            sleep(6)
            mainConn.send(playerMove)
            agentMove = mainConn.recv()
            game.move(color, int(agentMove))
        else:
            playerMove = str(input('Please enter a move: '))
            game.move(color, int(playerMove))
        color *= -1
    print(f'Game Over, winner: {game.winner}')