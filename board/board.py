import numpy as np
import copy

class Board:
    ROW_COUNT = 6
    COLUMN_COUNT = 7

    EMPTY = 0
    PLAYER1_PIECE = 1
    PLAYER2_PIECE = 2

    WINDOW_LENGTH = 4
    LAST_COLUMN_POSITION = None
    LAST_PLAYER_PLAYED = 0

    def __init__(self):
        self.board = np.zeros((self.ROW_COUNT, self.COLUMN_COUNT), dtype=int)
        self.num_slots_filled = 0

        #adding additional variables for monte carlo tree search
        self.heights = [(self.ROW_COUNT + 1)*i for i in range(self.COLUMN_COUNT)] # top empty row for each column
        self.lowest_row = [0]*self.COLUMN_COUNT # number of stones in each row
        self.top_row = [(x*(self.ROW_COUNT+1))-1 for x in range(1, self.COLUMN_COUNT+1)] # top row of the board (this will never change)

    def copy_board(self):
        c = copy.deepcopy(self)
        return c

    def get_board(self):
        return self.board

    def get_row_col(self, row, col):
        return self.board[row][col]
    
    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece
        self.num_slots_filled += 1

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

    def set_player_column(self, piece, col):
        self.LAST_COLUMN_POSITION = col
        self.LAST_PLAYER_PLAYED = piece

    def update_move_list(self, col):
        self.heights[col] += 1 # update top empty row for column
        self.lowest_row[col] += 1 # update number of stones in column

    def get_list_moves(self):
        available_moves = []
        for i in range(self.COLUMN_COUNT):
            if self.lowest_row[i] < self.ROW_COUNT:
                available_moves.append(i)
        return available_moves

    def search_result(self, piece):
        if self.winning_move(piece): return 1
        elif self.winning_move(self.get_opponent_piece(piece)): return 0
        elif not self.get_list_moves(): return 0.5
    
    def get_opponent_piece(self, piece):
        if piece == self.PLAYER1_PIECE:
            return self.PLAYER2_PIECE
        else:
            return self.PLAYER1_PIECE