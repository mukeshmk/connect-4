import numpy as np
import copy

class Board:
    ROW_COUNT = 6
    COLUMN_COUNT = 7

    EMPTY = 0
    PLAYER1_PIECE = 1
    PLAYER2_PIECE = 2

    WINDOW_LENGTH = 4

    PREV_MOVE = None
    PREV_PLAYER = None
    CURR_PLAYER = None

    def __init__(self, current_player):
        self.board = np.zeros((self.ROW_COUNT, self.COLUMN_COUNT), dtype=int)
        self.num_slots_filled = 0
        self.CURR_PLAYER = current_player
        self.PREV_PLAYER = self.get_opp_player(current_player)

    def copy_board(self):
        c = copy.deepcopy(self)
        return c

    def get_board(self):
        return self.board

    def get_row_col(self, row, col):
        return self.board[row][col]

    def get_opp_player(self, piece):
        if piece == self.PLAYER1_PIECE:
            return self.PLAYER2_PIECE
        else:
            return self.PLAYER1_PIECE

    def drop_piece(self, col, piece):
        row = self.get_next_open_row(col)
        self.board[row][col] = piece
        self.num_slots_filled += 1
        self.PREV_MOVE = col
        self.PREV_PLAYER = piece
        self.CURR_PLAYER = self.get_opp_player(piece)

    def is_valid_location(self, col):
        return self.board[self.ROW_COUNT-1][col] == 0

    def get_next_open_row(self, col):
        for r in range(self.ROW_COUNT):
            if self.board[r][col] == 0:
                return r

    def print_board(self):
        print(np.flip(self.board, 0))

    def winning_move(self, piece):
        # Check horizontal locations for win
        for c in range(self.COLUMN_COUNT-3):
            for r in range(self.ROW_COUNT):
                if self.board[r][c] == piece and self.board[r][c+1] == piece and self.board[r][c+2] == piece and self.board[r][c+3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT-3):
                if self.board[r][c] == piece and self.board[r+1][c] == piece and self.board[r+2][c] == piece and self.board[r+3][c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(self.COLUMN_COUNT-3):
            for r in range(self.ROW_COUNT-3):
                if self.board[r][c] == piece and self.board[r+1][c+1] == piece and self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(self.COLUMN_COUNT-3):
            for r in range(3, self.ROW_COUNT):
                if self.board[r][c] == piece and self.board[r-1][c+1] == piece and self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece:
                    return True

    def get_valid_locations(self):
        valid_locations = []
        for col in range(self.COLUMN_COUNT):
            if self.is_valid_location(col):
                valid_locations.append(col)
        return valid_locations

    def check_draw(self):
        if self.num_slots_filled == self.ROW_COUNT * self.COLUMN_COUNT:
            return True
        return False

    def search_result(self, piece):
        if self.winning_move(piece):
            return 1
        elif self.winning_move(self.get_opp_player(piece)):
            return 0
        elif not self.get_valid_locations():
            return 0.5
