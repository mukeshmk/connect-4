import numpy as np
import pygame
import sys
import math
import random
from board import *
from bots import *

board = None
gb = None

# dev statement to turn of the UI when having a bot vs bot match
# turning UI off in this case helps improve the performance of the bots.
graphics = True

PLAYER_COLOUR = [GBoard.RED, GBoard.YELLOW]

game_over = False
turn = random.randint(Board.PLAYER1_PIECE, Board.PLAYER2_PIECE)

def next_turn():
	global turn
	print("\nPlayer " + str(turn) + "'s Turn\n")
	board.print_board()
	if graphics:
		gb.draw_gboard(board)

	if turn == board.PLAYER1_PIECE:
		turn = board.PLAYER2_PIECE
	else:
		turn = board.PLAYER1_PIECE

def check_win(piece):
	if board.winning_move(piece):
		if graphics:
			gb.write_on_board("Player" + str(piece) + " wins!!", PLAYER_COLOUR[piece-1], (40, 10))
			gb.update_gboard()
		print("\nPlayer" + str(piece) + " wins!!")
		return True
	if board.check_draw():
		if graphics:
			gb.write_on_board("Draw!!", gb.BLUE, (240, 10))
			gb.update_gboard()
		print("\nDraw!!")
		return True
	return False

def connect4(p1, p2, ui=True):
	global game_over, board, gb, graphics

	graphics=ui

	board = Board(turn)
	board.print_board()

	if graphics:
		gb = GBoard(board)
		gb.draw_gboard(board)
		gb.update_gboard()

	while not game_over:
		# Player1's Input
		if turn == board.PLAYER1_PIECE and not game_over:
			col = p1.get_move(board)

			if board.is_valid_location(col):
				board.drop_piece(col, board.PLAYER1_PIECE)
				next_turn()
				game_over = check_win(board.PLAYER1_PIECE)

		# Player2's Input
		if turn == board.PLAYER2_PIECE and not game_over:
			col = p2.get_move(board)

			if board.is_valid_location(col):
				board.drop_piece(col, board.PLAYER2_PIECE)
				next_turn()
				game_over = check_win(board.PLAYER2_PIECE)

		if game_over:
			pygame.time.wait(3000)

if __name__ == "__main__":
	print()
	print("use the file 'game.py' to start the game!")
