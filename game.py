import numpy as np

class Game:

    def __init__(self):
        self.emptyValue = 0
        self.winner = 0

        #Create the board
        self.board = np.full((6,7), self.emptyValue)

    def move(self, color, position):
        column = self.board[:,position]
        for y, chip in enumerate(column):

            #error handling required for the first one since it will reference past the end of the array
            try:
                if chip == self.emptyValue and column[y+1] != self.emptyValue:
                    column[y] = color
                    break
            except IndexError:
                if chip == self.emptyValue:
                    column[y] = color
                    break
        else:
            #Invalid move, try again
            return False

        #Return true if move was accepted
        return True

    def over(self):
        board = self.board

        if 0 not in board:
            return True

        for y, row in enumerate(board):
            for x, chip in enumerate(row):
                if chip != self.emptyValue:
                    #check all around the chip for matching ones
                    #Only have to check one direction because other direction will be checked by other chips

                    #horizontal
                    try:
                        if chip == row[x+1] == row[x+2] == row[x+3]:
                            self.winner = chip
                            return True
                    except IndexError:
                        pass

                    #vertical
                    try:
                        if chip == board[y+1][x] == board[y+2][x] == board[y+3][x]:
                            self.winner = chip
                            return True
                    except IndexError:
                        pass

                    #diagonal 1
                    try:
                        if chip == board[y+1][x+1] == board[y+2][x+2] == board[y+3][x+3]:
                            self.winner = chip
                            return True
                    except IndexError:
                        pass

                    #diagonal 2
                    try:
                        if chip == board[y-1][x+1] == board[y-2][x+2] == board[y-3][x+3]:
                            self.winner = chip
                            return True
                    except IndexError:
                        pass
        #Return False if no wins detected
        return False



#Two player game if run directly (for testing)
if __name__ == "__main__":
    game = Game()
    color = -1
    while not game.over():
        print(game.board)
        move = int(input(f"{color}, enter your move: "))
        if game.move(color, move):
            if color == -1:
                color = 1
            else:
                color = -1
    print(f"The winner is {game.winner}")


