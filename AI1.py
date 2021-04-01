from dataclasses import dataclass
import random
import Data


# dataclass representing one possible move
@dataclass
class Move:
    row: int
    col: int
    path: [int]  # list of row/col diffs
    score: int  # len of path + random number (0..9)


# calculates next move
def calculate_move(orientation: Data.Orientation, pieces: Data.Pieces, player: Data.Color) -> Data.Move:
    # pick correct direction
    direction = -1
    end_row = 0
    if (orientation == Data.Orientation.WhiteUp and player == Data.Color.White) or (orientation == Data.Orientation.BlackUp and player == Data.Color.Black):
        direction = 1
        end_row = 7

    # find all my pawns + mark all occupied squares
    # calculate bias (if more pawns are on left or right
    occupied_squares = set()
    my_pawns = []
    bias = 0
    for piece in pieces:
        if piece.color == player:
            my_pawns.append(piece)
            bias += 3.5 - piece.col  # pieces on cols 0-3 create positive bias, cols 4-7 negative bias
        occupied_squares.add((piece.row, piece.col))

    # find all possible moves
    best_score = -999
    best_move = None
    for pawn in my_pawns:
        # is pawn on the end?
        if pawn.row == end_row:
            continue
        # check move to the left
        if pawn.col > 0 and (pawn.row + direction, pawn.col - 1) not in occupied_squares:
            score = random.randint(0, 5) + abs(end_row - pawn.row) - 2*bias
            if score > best_score:
                best_move = Move(pawn.row, pawn.col, [(direction, -1)], score)
                best_score = score
        # check move to the right
        if pawn.col < 7 and (pawn.row + direction, pawn.col + 1) not in occupied_squares:
            score = random.randint(0, 5) + abs(end_row - pawn.row) + 2*bias
            if score > best_score:
                best_move = Move(pawn.row, pawn.col, [(direction, 1)], score)
                best_score = score
        # check jump to the left
        if pawn.col > 1 and abs(pawn.row - end_row) > 1 and (pawn.row + 2*direction, pawn.col - 2) not in occupied_squares and (pawn.row + direction, pawn.col - 1) in occupied_squares:
            score = 10 + random.randint(0, 5) + abs(end_row - pawn.row) - 2*bias
            if score > best_score:
                best_move = Move(pawn.row, pawn.col, [(2 * direction, -2)], score)
                best_score = score
        # check jump to the right
        if pawn.col < 6 and abs(pawn.row - end_row) > 1 and (pawn.row + 2*direction, pawn.col + 2) not in occupied_squares and (pawn.row + direction, pawn.col + 1) in occupied_squares:
            score = 10 + random.randint(0, 5) + abs(end_row - pawn.row) + 2*bias
            if score > best_score:
                best_move = Move(pawn.row, pawn.col, [(2 * direction, 2)], score)
                best_score = score

    # pick best move
    if best_move is None:
        return [Data.PartialMove(0, 1, 2, 3)]
    result = Data.PartialMove(best_move.row, best_move.col, best_move.row + best_move.path[0][0], best_move.col + best_move.path[0][1])
    return [result]
