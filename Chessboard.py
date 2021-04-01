# Simple tkinter checkerboard with pawns only (other pieces are not used for "skakana".
# Inspired by https://stackoverflow.com/questions/4954395/create-board-game-like-grid-in-python
# Images used from public domain.

import tkinter as tk
import Data
import time


class Chessboard(tk.Frame):
    def __init__(self, parent, rows=8, columns=8, size=80, color1="white", color2="sienna"):
        # all internal data
        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2
        canvas_width = columns * size
        canvas_height = rows * size
        self.root_white = tk.PhotoImage(file="pawn_white_mini.png")
        self.root_black = tk.PhotoImage(file="pawn_black_mini.png")
        self.pieces = []

        # init tk canvas
        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        # this binding will cause a refresh if the user interactively changes the window size
        self.canvas.bind("<Configure>", self.draw_board)

        # event handling for manual play
        parent.bind("<Key>", self.key_pressed)
        self.canvas.bind("<Button-1>", self.clicked)
        self.clicked_fields = []
        self.enter_pressed = False

    # redraws all pieces
    def draw_pieces(self, pieces: Data.Pieces):
        self.pieces = pieces
        self.canvas.delete("piece")
        for piece in pieces:
            x = (piece.col * self.size) + int(self.size / 2)
            y = (piece.row * self.size) + int(self.size / 2)
            if piece.color is Data.Color.Black:
                image = self.root_black
            else:
                image = self.root_white
            self.canvas.create_image(x, y, image=image, tags="piece", anchor="c")

    # redraws whole board (including pieces), possibly in response to window resize event
    def draw_board(self, event):
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.size = min(xsize, ysize)
        self.canvas.delete("square")
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                color = self.color1 if color == self.color2 else self.color2
        self.draw_pieces(self.pieces)
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")

    # waits until human clicks his move and presses enter
    def wait_for_move(self, root) -> Data.Move:
        self.enter_pressed = False
        while True:
            root.update_idletasks()
            root.update()
            if self.enter_pressed is True:
                if len(self.clicked_fields) < 2:
                    print("Too few squaress selected!");
                    self.enter_pressed = False
                    continue
                move = []
                starting_pair = self.clicked_fields[0]
                for pair in self.clicked_fields[1:]:
                    move.append(Data.PartialMove(starting_pair[0], starting_pair[1], pair[0], pair[1]))
                    starting_pair = pair
                self.canvas.delete("selected")
                self.clicked_fields.clear()
                return move
            time.sleep(0.1)

    def key_pressed(self, event):
        if event.keysym == 'Return':
            print("Enter pressed - selected squares will be sent to the game")
            self.enter_pressed = True
        if event.keysym == 'Escape':
            print("ESC pressed - selected squares cleared")
            self.canvas.delete("selected")
            self.clicked_fields.clear()

    def clicked(self, event):
        # calculate which square was selected
        row = event.y // self.size
        col = event.x // self.size
        print("Selected row " + str(row) + " col " + str(col))
        self.clicked_fields.append((row, col))

        # highlight selected square
        x1 = (col * self.size)
        y1 = (row * self.size)
        x2 = x1 + self.size
        y2 = y1 + self.size
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="green", stipple='gray50', tags="selected")


if __name__ == "__main__":
    root = tk.Tk()
    board = Chessboard(root)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    pieces = [Data.Piece(1, 1, Data.PieceType.Pawn, Data.Color.Black),
              Data.Piece(1, 2, Data.PieceType.Pawn, Data.Color.Black),
              Data.Piece(2, 1, Data.PieceType.Pawn, Data.Color.White),
              Data.Piece(2, 2, Data.PieceType.Pawn, Data.Color.White)]
    board.draw_pieces(pieces)
    root.mainloop()
