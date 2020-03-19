import numpy as np
import pygame
import sys
import math
from board.board import Board
from board.graphics import GBoard

board = Board()
gb = GBoard(board)

board.print_board()
game_over = False
turn = 0

gb.draw_board(board)
gb.update_gboard()

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			gb.draw_rect(gb.BLACK, (0,0, gb.width, gb.SQUARESIZE))
			posx = event.pos[0]
			if turn == 0:
				gb.draw_circle(gb.RED, (posx, int(gb.SQUARESIZE/2)), gb.RADIUS)
			else: 
				gb.draw_circle(gb.YELLOW, (posx, int(gb.SQUARESIZE/2)), gb.RADIUS)
		gb.update_gboard()

		if event.type == pygame.MOUSEBUTTONDOWN:
			gb.draw_rect(gb.BLACK, (0, 0, gb.width, gb.SQUARESIZE))

			# Ask for Player 1 Input
			if turn == 0:
				posx = event.pos[0]
				col = int(math.floor(posx/gb.SQUARESIZE))

				if board.is_valid_location(col):
					row = board.get_next_open_row(col)
					board.drop_piece(row, col, 1)

					if board.winning_move(1):
						label = gb.myfont.render("Player 1 wins!!", 1, gb.RED)
						gb.screen.blit(label, (40, 10))
						game_over = True

			# Ask for Player 2 Input
			else:				
				posx = event.pos[0]
				col = int(math.floor(posx/gb.SQUARESIZE))

				if board.is_valid_location(col):
					row = board.get_next_open_row(col)
					board.drop_piece(row, col, 2)

					if board.winning_move(2):
						label = gb.myfont.render("Player 2 wins!!", 1, gb.YELLOW)
						gb.screen.blit(label, (40, 10))
						game_over = True

			board.print_board()
			gb.draw_board(board)

			turn += 1
			turn = turn % 2

			if game_over:
				pygame.time.wait(3000)
