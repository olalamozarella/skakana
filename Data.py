from dataclasses import dataclass
from enum import Enum

# type of chess piece
PieceType = Enum('PieceType', 'Pawn Queen')

# color enum
Color = Enum('Color', 'Black White')

# enum for game orientation - white starts either up or down
Orientation = Enum('Orientation', 'WhiteUp BlackUp')

# enum for all supported players
Player = Enum('Player', 'Human AI1 AI2')
Players = (Player, Player)


# dataclass representing one chess piece
@dataclass
class Piece:
    row: int
    col: int
    type: PieceType
    color: Color


# dataclass representing one game move
@dataclass
class PartialMove:
    old_row: int
    old_col: int
    new_row: int
    new_col: int


# alias for list of moves
Move = [PartialMove]


# alias for list of pieces
Pieces = [Piece]


# simple test
if __name__ == "__main__":
    p = Piece(1, 2, PieceType.Pawn, Color.Black)
    print(p)
