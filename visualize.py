from tkinter import *

class Visualization:
    def __init__(self):
        self.tk = Tk()
        self.canvas = Canvas(self.tk)
        self.scale = 30

    def display(self, board):
        self.canvas.create_rectangle(0, 0, 7*self.scale, 6*self.scale, fill="yellow")
        color = "white"
        for y, row in enumerate(board):
            for x, chip in enumerate(row):
                if chip == 1:
                    color = "blue"
                elif chip == -1:
                    color = "red"
                else:
                    color = "white"
                self.canvas.create_oval(self.scale*x, self.scale*y, self.scale*(x+1), self.scale*(y+1), fill=color)
        self.canvas.pack(fill=BOTH, expand=1)
        self.tk.update()

