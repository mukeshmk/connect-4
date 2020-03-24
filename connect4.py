import numpy as np
import pygame
import sys
import math
import random
from board import *
from bots import *

board = Board()
gb = GBoard(board)

PLAYER_COLOUR = [gb.RED, gb.YELLOW]

board.print_board()
gb.draw_gboard(board)
gb.update_gboard()

game_over = False
turn = random.randint(board.PLAYER1_PIECE, board.PLAYER2_PIECE)

def next_turn():
	global turn
	board.print_board()
	gb.draw_gboard(board)

	if turn == board.PLAYER1_PIECE:
		turn = board.PLAYER2_PIECE
	else:
		turn = board.PLAYER1_PIECE

def check_win(piece):
	if board.winning_move(piece):
		gb.write_on_board("Player" + str(piece) + " wins!!", PLAYER_COLOUR[piece-1], (40, 10))
		return True
	if board.check_draw():
		gb.write_on_board("Draw!!", gb.BLUE, (240, 10))
		return True
	return False

def connect4(p1, p2):
	global game_over, board
	while not game_over:
		# Player1's Input
		if turn == board.PLAYER1_PIECE and not game_over:
			col = p1.get_move(board)

			if board.is_valid_location(col):
				board.set_player_column(board.PLAYER1_PIECE, col)
				row = board.get_next_open_row(col)
				board.drop_piece(row, col, board.PLAYER1_PIECE)

				game_over = check_win(board.PLAYER1_PIECE)
				next_turn()

		# Player2's Input
		if turn == board.PLAYER2_PIECE and not game_over:
			col = p2.get_move(board)

			if board.is_valid_location(col):
				board.set_player_column(board.PLAYER2_PIECE, col)
				row = board.get_next_open_row(col)
				board.drop_piece(row, col, board.PLAYER2_PIECE)

				game_over = check_win(board.PLAYER2_PIECE)
				next_turn()

		if game_over:
			pygame.time.wait(3000)

if __name__ == "__main__":
	p1 = MonteCarloBot(board, board.PLAYER1_PIECE)
	p2 = MiniMaxBot(board.PLAYER2_PIECE)
	connect4(p1, p2)
