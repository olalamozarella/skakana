# system includes
import argparse
import tkinter
import time
import sys
# project includes
import Data
import Chessboard
import AI_snake
import AI_frog
import AI_kangaroo

EXIT_CODES = dict(
    HUMAN_WON_WHITE=0,
    HUMAN_WON_BLACK=1,
    AI_1_WON_WHITE=2,
    AI_1_WON_BLACK=3,
    AI_2_WON_WHITE=4,
    AI_2_WON_BLACK=5,
    HUMAN_STUCK=10,
    AI_1_STUCK=11,
    AI_2_STUCK=12,
    OTHER_ERROR=-1)


def win(player, color, confirm_needed):
    print("We have a winner! " + str(player) + "(" + str(color) + ") won")
    if confirm_needed is True:
        input("Press Enter to continue...")
    if color == Data.Color.White:
        if player == Data.Player.Human:
            return EXIT_CODES["HUMAN_WON_WHITE"]
        elif player == Data.Player.AI1:
            return EXIT_CODES["AI_1_WON_WHITE"]
        elif player == Data.Player.AI2:
            return EXIT_CODES["AI_2_WON_WHITE"]
    elif color == Data.Color.Black:
        if player == Data.Player.Human:
            return EXIT_CODES["HUMAN_WON_BLACK"]
        elif player == Data.Player.AI1:
            return EXIT_CODES["AI_1_WON_BLACK"]
        elif player == Data.Player.AI2:
            return EXIT_CODES["AI_2_WON_BLACK"]
    print("Failed to convert exit code")
    return EXIT_CODES["OTHER_ERROR"]


def lose(player, color, confirm_needed):
    print("Too many incorrect moves! " + str(player) + "(" + str(color) + ") lost")
    if confirm_needed is True:
        input("Press Enter to continue...")
    if player == Data.Player.Human:
        return EXIT_CODES["HUMAN_STUCK"]
    elif player == Data.Player.AI1:
        return EXIT_CODES["AI_1_STUCK"]
    elif player == Data.Player.AI2:
        return EXIT_CODES["AI_2_STUCK"]
    else:
        print("Failed to convert exit code")
        return EXIT_CODES["OTHER_ERROR"]


class Skakana:
    root, board, pieces, active_color, incorrect_move_counter = None, None, None, None, None

    def __init__(self, orientation: Data.Orientation, headless: bool, delayed: bool):
        self.orientation = orientation
        upper_player = Data.Color.White if orientation == Data.Orientation.WhiteUp else Data.Color.Black
        lower_player = Data.Color.Black if orientation == Data.Orientation.WhiteUp else Data.Color.White
        self.pieces = [
            Data.Piece(1, 0, Data.PieceType.Pawn, upper_player),
            Data.Piece(0, 1, Data.PieceType.Pawn, upper_player),
            Data.Piece(1, 2, Data.PieceType.Pawn, upper_player),
            Data.Piece(0, 3, Data.PieceType.Pawn, upper_player),
            Data.Piece(1, 4, Data.PieceType.Pawn, upper_player),
            Data.Piece(0, 5, Data.PieceType.Pawn, upper_player),
            Data.Piece(1, 6, Data.PieceType.Pawn, upper_player),
            Data.Piece(0, 7, Data.PieceType.Pawn, upper_player),
            Data.Piece(7, 0, Data.PieceType.Pawn, lower_player),
            Data.Piece(6, 1, Data.PieceType.Pawn, lower_player),
            Data.Piece(7, 2, Data.PieceType.Pawn, lower_player),
            Data.Piece(6, 3, Data.PieceType.Pawn, lower_player),
            Data.Piece(7, 4, Data.PieceType.Pawn, lower_player),
            Data.Piece(6, 5, Data.PieceType.Pawn, lower_player),
            Data.Piece(7, 6, Data.PieceType.Pawn, lower_player),
            Data.Piece(6, 7, Data.PieceType.Pawn, lower_player)]
        self.active_color = Data.Color.White
        self.incorrect_move_counter = 0
        self.headless = headless
        self.delayed = delayed
        if headless is False:
            self.root = tkinter.Tk()
            self.board = Chessboard.Chessboard(self.root)
            self.board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
            self.board.draw_pieces(self.pieces)

    def run(self, players: Data.Players):
        # initialize all internal variables and UI
        active_player = players[0]

        # play the game
        while True:
            if active_player == Data.Player.Snake:
                print("Waiting for snake's turn(" + str(self.active_color) + ")")
                move = AI_snake.calculate_move(self.orientation, self.pieces, self.active_color)
            elif active_player == Data.Player.Frog:
                print("Waiting for frog's turn(" + str(self.active_color) + ")")
                move = AI_frog.calculate_move(self.orientation, self.pieces, self.active_color)
            elif active_player == Data.Player.Kangaroo:
                print("Waiting for kangaroo's turn(" + str(self.active_color) + ")")
                move = AI_kangaroo.calculate_move(self.orientation, self.pieces, self.active_color)
            else:
                print("Waiting for player move in UI")
                move = self.board.wait_for_move(self.root)
            if self.apply_move(move) is False:
                print("Incorrect move! " + str(move))
                self.incorrect_move_counter += 1
                if self.incorrect_move_counter >= 3:
                    return lose(active_player, self.active_color, not self.headless)
            else:
                if self.headless is False:
                    self.board.draw_pieces(self.pieces)
                    self.root.update_idletasks()
                    self.root.update()
                if self.delayed is True and active_player != Data.Player.Human:
                    time.sleep(0.1)
                if self.check_end() is True:
                    return win(active_player, self.active_color, not self.headless)
                self.active_color = Data.Color.White if self.active_color == Data.Color.Black else Data.Color.Black
                active_player = players[0] if active_player == players[1] else players[1]
                self.incorrect_move_counter = 0

    # checks if the calculated move is valid and can be performed
    def apply_move(self, move_array: Data.Move) -> bool:
        selected_piece = None
        jumped = False

        def apply_partial_move(move: Data.PartialMove):
            # check if move is in range
            if move.new_row < 0 or move.new_row > 7:
                print("Incorrect move! " + str(self.active_color) + " " + str(move) + " Target square is out of chessboard")
                return False
            if move.new_col < 0 or move.new_col > 7:
                print("Incorrect move! " + str(self.active_color) + " " + str(move) + " Target square is out of chessboard")
                return False

            # check distance
            difference_row = move.new_row - move.old_row
            difference_col = move.new_col - move.old_col
            if abs(difference_col) > 2 or abs(difference_row) > 2 or abs(difference_row) != abs(difference_col):
                print("Incorrect move! " + str(self.active_color) + " " + str(move) + " Jumping further than allowed")
                return False

            # check direction
            if (self.orientation == Data.Orientation.WhiteUp and self.active_color == Data.Color.White and difference_row < 0) or \
                    (self.orientation == Data.Orientation.WhiteUp and self.active_color == Data.Color.Black and difference_row > 0) or \
                    (self.orientation != Data.Orientation.WhiteUp and self.active_color == Data.Color.White and difference_row > 0) or \
                    (self.orientation != Data.Orientation.WhiteUp and self.active_color == Data.Color.Black and difference_row < 0):
                print("Incorrect move! " + str(self.active_color) + " " + str(move) + " Bad move direction")
                return False

            # detect jumping and calculate middle position
            jumping, jumped_piece, jump_over_row, jump_over_col = False, None, None, None
            if abs(difference_row) == 2:
                jumping = True
                jump_over_row = move.old_row + int(difference_row / 2)
                jump_over_col = move.old_col + int(difference_col / 2)

            nonlocal jumped
            if jumped is True and jumping is False:
                print("Incorrect move! " + str(self.active_color) + " " + str(move) + " Double move without jumping in second part")
                return False

            # loop over all pieces
            nonlocal selected_piece
            for piece in self.pieces:
                # find selected piece
                if piece.row == move.old_row and piece.col == move.old_col:
                    selected_piece = piece
                # check if end square is not full
                if piece.row == move.new_row and piece.col == move.new_col:
                    print("Incorrect move! " + str(self.active_color) + " " + str(move) + " Target square is occupied")
                    return False
                # if jumping, find piece in between
                if jumping is True:
                    if piece.row == jump_over_row and piece.col == jump_over_col:
                        jumped_piece = piece

            if selected_piece is None:
                print("Incorrect move! " + str(self.active_color) + " " + str(move) + " Selected piece does not exist")
                return False

            # check if selected piece has player's color
            if selected_piece.color != self.active_color:
                print("Incorrect move! " + str(self.active_color) + " " + str(move) + " Tried to move with opponent's piece")
                return False

            # if end square is two steps away, check if there is a piece in between
            if jumping is True and jumped_piece is None:
                print("Incorrect move! " + str(self.active_color) + " " + str(move) + " Tried jumping over nothing")
                return False

            # perform move
            selected_piece.row, selected_piece.col = move.new_row, move.new_col
            jumped = jumping  # nonlocal flag used for limiting double moves when not jumping
            print("Move performed: " + str(self.active_color) + " " + str(move))
            return True

        # move can consist of multiple sub-moves in case of double/triple jump - we need to process these partially
        move_performed = False
        for partial_move in move_array:
            if move_performed is True and jumped is False:
                print("Incorrect move! " + str(self.active_color) + " " + str(partial_move) + " Tried second move without jumping")
                selected_piece.row, selected_piece.col = move_array[0].old_row, move_array[0].old_col
                return False
            if apply_partial_move(partial_move) is True:
                move_performed = True
            else:
                if move_performed is True and selected_piece is not None:
                    # revert the selected piece back to its original location
                    selected_piece.row, selected_piece.col = move_array[0].old_row, move_array[0].old_col
                return False
        return True

    # checks if either player won
    def check_end(self) -> bool:
        upper_win, lower_win = True, True
        finishing_up = Data.Color.Black if self.orientation == Data.Orientation.WhiteUp else Data.Color.White
        finishing_down = Data.Color.White if self.orientation == Data.Orientation.WhiteUp else Data.Color.Black
        for piece in self.pieces:
            if upper_win is True and piece.color == finishing_up and piece.row > 1:
                upper_win = False
            if lower_win is True and piece.color == finishing_down and piece.row < 6:
                lower_win = False
        if upper_win:
            print("We have a winner! " + str(finishing_up))
            return True
        elif lower_win:
            print("We have a winner! " + str(finishing_down))
            return True
        else:
            return False


def parse_player_option(option):
    if option == "Human":
        return Data.Player.Human
    if option == "Snake":
        return Data.Player.Snake
    if option == "Frog":
        return Data.Player.Frog
    if option == "Kangaroo":
        return Data.Player.Kangaroo


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("player1", help="specify which player will play as white", choices=["Human", "Snake", "Frog", "Kangaroo"])
    parser.add_argument("player2", help="specify which player will play as black", choices=["Human", "Snake", "Frog", "Kangaroo"])
    parser.add_argument("--headless", help="run in shell only, no graphics", action="store_true")
    parser.add_argument("--delayed", help="waits one second after each AI turn", action="store_true")
    args = parser.parse_args()
    player1 = parse_player_option(args.player1)
    player2 = parse_player_option(args.player2)
    if args.headless and (player1 == Data.Player.Human or player2 == Data.Player.Human):
        print("Humans cannot play on headless mode (how would you make your turn?)")
        sys.exit(EXIT_CODES["OTHER_ERROR"])
    game = Skakana(Data.Orientation.WhiteUp, headless=args.headless, delayed=args.delayed)
    result = game.run((player1, player2))
    sys.exit(result)
