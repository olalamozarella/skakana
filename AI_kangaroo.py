# kangaroo AI - can move or do any jumps (single, double, triple)
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
    if (orientation == Data.Orientation.WhiteUp and player == Data.Color.White) or (
            orientation == Data.Orientation.BlackUp and player == Data.Color.Black):
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
            score = random.randint(0, 5) + abs(end_row - pawn.row) - 2 * bias
            if score > best_score:
                best_move = Move(pawn.row, pawn.col, [(direction, -1)], score)
                best_score = score
        # check move to the right
        if pawn.col < 7 and (pawn.row + direction, pawn.col + 1) not in occupied_squares:
            score = random.randint(0, 5) + abs(end_row - pawn.row) + 2 * bias
            if score > best_score:
                best_move = Move(pawn.row, pawn.col, [(direction, 1)], score)
                best_score = score
        # check jumps
        base_move = Move(pawn.row, pawn.col, [], 0)
        best_score, best_move = calculate_jumps(direction, occupied_squares, end_row, base_move, best_score, best_move, bias)

    # pick best move
    if best_move is None:
        return [Data.PartialMove(-1, -1, -1, -1)]
    next_position = (best_move.row + best_move.path[0][0], best_move.col + best_move.path[0][1])
    first_part = Data.PartialMove(best_move.row, best_move.col, next_position[0], next_position[1])
    result = [first_part]
    for i in range(1, len(best_move.path)):
        last_position = next_position
        next_position = last_position[0] + best_move.path[i][0], last_position[1] + best_move.path[i][1]
        next_part = Data.PartialMove(last_position[0], last_position[1], next_position[0], next_position[1])
        result.append(next_part)
    return result


def calculate_jumps(direction, occupied_squares, end_row, base_move, best_score, best_move, bias):
    original_square = (base_move.row, base_move.col)
    if base_move.path is not None:
        for path in base_move.path:
            original_square = original_square[0] + path[0], original_square[1] + path[1]

    # check jump to the left
    difference = (2 * direction, -2)
    next_square = (original_square[0] + difference[0], original_square[1] + difference[1])
    middle_square = (original_square[0] + direction, original_square[1] - 1)
    if 0 <= next_square[1] <= 7 \
            and abs(original_square[0] - end_row) > 1 \
            and next_square not in occupied_squares \
            and middle_square in occupied_squares:
        # calculate score, maybe this move is the best one?
        score = base_move.score + 10 + random.randint(0, 5) + abs(end_row - original_square[0]) - 2 * bias
        next_path = base_move.path.copy()
        next_path.append(difference)
        next_base_move = Move(base_move.row, base_move.col, next_path, score)
        if score > best_score:
            best_move = next_base_move
            best_score = score
        # try to jump deeper
        best_score, best_move = calculate_jumps(direction, occupied_squares, end_row, next_base_move, best_score, best_move, bias)

    # check jump to the right
    difference = (2 * direction, 2)
    next_square = (original_square[0] + difference[0], original_square[1] + difference[1])
    middle_square = (original_square[0] + direction, original_square[1] + 1)
    if 0 <= next_square[1] <= 7 \
            and abs(original_square[0] - end_row) > 1 \
            and next_square not in occupied_squares \
            and middle_square in occupied_squares:
        # calculate score, maybe this move is the best one?
        score = base_move.score + 10 + random.randint(0, 5) + abs(end_row - original_square[0]) + 2 * bias
        next_path = base_move.path.copy()
        next_path.append(difference)
        next_base_move = Move(base_move.row, base_move.col, next_path, score)
        if score > best_score:
            best_move = next_base_move
            best_score = score
        # try to jump deeper
        best_score, best_move = calculate_jumps(direction, occupied_squares, end_row, next_base_move, best_score, best_move, bias)
    return best_score, best_move
