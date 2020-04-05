import numpy as np
import os
import pygame
import sys
import math
import random
import time
from board import *
from bots import *

#pygame version number and welcome message hidden.
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

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
			gb.write_on_board("PLAYER " + str(piece) + " WINS!", PLAYER_COLOUR[piece - 1], 350, 50, 70, True)
			gb.update_gboard()
		print("\nPLAYER " + str(piece) + " WINS!")
		return True
	
	if board.check_draw():
		if graphics:
			gb.write_on_board("IT'S A TIE!", gb.LIGHTBLUE, 350, 50, 70, True)
			gb.update_gboard()
		print("\n IT'S A TIE!")
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

	time_p1 = time_p2 = 0
	moves_count_p1 = moves_count_p2 = 0

	while not game_over:
		# Player1's Input
		start = time.perf_counter()
		if turn == board.PLAYER1_PIECE and not game_over:
			col = p1.get_move(board)

			if board.is_valid_location(col):
				board.drop_piece(col, board.PLAYER1_PIECE)
				moves_count_p1 += 1
				next_turn()
				game_over = check_win(board.PLAYER1_PIECE)
		end = time.perf_counter()

		time_p1 += (end - start)

		# Player2's Input
		start = time.perf_counter()
		if turn == board.PLAYER2_PIECE and not game_over:
			col = p2.get_move(board)

			if board.is_valid_location(col):
				board.drop_piece(col, board.PLAYER2_PIECE)
				moves_count_p2 += 1
				next_turn()
				game_over = check_win(board.PLAYER2_PIECE)
		end = time.perf_counter()

		time_p2 += (end - start)

		if game_over:
			pygame.time.wait(1000)

			print("\nPlayer 1")
			print("TIME: " + "{:.2f}".format(round(time_p1, 2)) + " seconds")
			print("MOVES: "+ str(moves_count_p1))
			print("\nPlayer 2")
			print("TIME: " + "{:.2f}".format(round(time_p2, 2)) + " seconds")
			print("MOVES: "+ str(moves_count_p2))

			sys.exit()

if __name__ == "__main__":
	print()
	print("use the file 'game.py' to start the game!")
