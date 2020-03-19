import numpy as np
import pygame
import sys
import math
import random
from board.board import Board
from board.graphics import GBoard
from bots.random import RandomBot

PLAYER = 0
BOT = 1

EMPTY = 0
PLAYER_PIECE = 1
BOT_PIECE = 2

board = Board()
gb = GBoard(board)

PLAYER_COLOUR = [gb.RED, gb.YELLOW]

board.print_board()
game_over = False

turn = random.randint(PLAYER, BOT)

gb.draw_gboard(board)
gb.update_gboard()

def next_turn():
	global turn
	board.print_board()
	gb.draw_gboard(board)

	turn += 1
	turn = turn % 2

def check_win(piece):
	if board.winning_move(piece):
		gb.write_on_board("Player" + str(piece) + " wins!!", PLAYER_COLOUR[piece-1], (40, 10))
		return True
	return False

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			gb.draw_rect(gb.BLACK, (0, 0, gb.width, gb.SQUARESIZE))
			posx = event.pos[0]
			if turn == PLAYER:
				gb.draw_circle(gb.RED, (posx, int(gb.SQUARESIZE/2)), gb.RADIUS)

		gb.update_gboard()

		if event.type == pygame.MOUSEBUTTONDOWN:
			gb.draw_rect(gb.BLACK, (0, 0, gb.width, gb.SQUARESIZE))
			# Player 1's Input
			if turn == PLAYER:
				posx = event.pos[0]
				col = int(math.floor(posx/gb.SQUARESIZE))

				if board.is_valid_location(col):
					row = board.get_next_open_row(col)
					board.drop_piece(row, col, PLAYER_PIECE)

					game_over = check_win(PLAYER_PIECE)
					next_turn()


	# Bot's Input
	if turn == BOT and not game_over:

		bot = RandomBot()
		col = bot.getBotMove(board)

		if board.is_valid_location(col):
			row = board.get_next_open_row(col)
			board.drop_piece(row, col, BOT_PIECE)

			game_over = check_win(BOT_PIECE)
			next_turn()

	if game_over:
		pygame.time.wait(3000)
