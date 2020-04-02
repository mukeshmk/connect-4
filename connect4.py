import numpy as np

#pygame version number and welcome message hidden.
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import sys
import math
import random
from board import *
from bots import *

board = None
gb = None

PLAYER_COLOUR = [GBoard.RED, GBoard.YELLOW]

game_over = False
turn = random.randint(Board.PLAYER1_PIECE, Board.PLAYER2_PIECE)

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
		gb.write_on_board("PLAYER " + str(piece) + " WINS!", PLAYER_COLOUR[piece - 1], 350, 50, 70, True)
		return True
	if board.check_draw():
		gb.write_on_board("IT'S A TIE!", gb.LIGHTBLUE, 350, 50, 70, True)
		return True
	return False

def connect4(p1, p2):
	global game_over, board, gb

	board = Board()
	gb = GBoard(board)

	board.print_board()
	gb.draw_gboard(board)
	gb.update_gboard()

	while not game_over:
		# Player1's Input
		if turn == board.PLAYER1_PIECE and not game_over:
			col = p1.getMove(board)

			if board.is_valid_location(col):
				row = board.get_next_open_row(col)
				board.drop_piece(row, col, board.PLAYER1_PIECE)

				game_over = check_win(board.PLAYER1_PIECE)
				next_turn()

		# Player2's Input
		if turn == board.PLAYER2_PIECE and not game_over:
			col = p2.getMove(board)

			if board.is_valid_location(col):
				row = board.get_next_open_row(col)
				board.drop_piece(row, col, board.PLAYER2_PIECE)

				game_over = check_win(board.PLAYER2_PIECE)
				next_turn()

		if game_over:
			pygame.time.wait(1000)
			sys.exit()

if __name__ == "__main__":
	print()
	print("use the file 'game.py' to start the game!")
