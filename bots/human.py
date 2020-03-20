import pygame
import math
import sys
from board.graphics import GBoard

class Human:
    def __init__(self, player, colour):
        self.player = player
        self.colour = colour

    def getBotMove(self, board):
        gb = GBoard(board)
        gb.draw_gboard(board)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    gb.draw_rect(gb.BLACK, (0, 0, gb.width, gb.SQUARESIZE))
                    posx = event.pos[0]
                    gb.draw_circle(self.colour, (posx, int(gb.SQUARESIZE/2)), gb.RADIUS)

                gb.update_gboard()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    gb.draw_rect(gb.BLACK, (0, 0, gb.width, gb.SQUARESIZE))
                    posx = event.pos[0]
                    col = int(math.floor(posx/gb.SQUARESIZE))
                    return col