import pygame
import pygame.gfxdraw

pygame.init()

class GBoard:
    BLUE = (0,0,255)
    BLACK = (0,0,0)
    RED = (255,0,0)
    YELLOW = (255,255,0)
    WHITE = (255, 255, 255)
    LIGHTBLUE = (93, 173, 226)

    SQUARESIZE = 100

    RADIUS = int(SQUARESIZE/2 - 5)

    myfont = pygame.font.SysFont("monospace", 75)

    def __init__(self, board):
        self.width = board.COLUMN_COUNT * self.SQUARESIZE
        self.height = (board.ROW_COUNT+1) * self.SQUARESIZE
        self.size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.size)

    def update_gboard(self):
        pygame.display.update()
    
    def draw_gboard(self, board):
        for c in range(board.COLUMN_COUNT):
            for r in range(board.ROW_COUNT):
                pygame.draw.rect(self.screen, self.BLUE, (c*self.SQUARESIZE, r*self.SQUARESIZE+self.SQUARESIZE, \
                    self.SQUARESIZE, self.SQUARESIZE))
                pygame.draw.circle(self.screen, self.BLACK, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), \
                    int(r*self.SQUARESIZE+self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
        
        for c in range(board.COLUMN_COUNT):
            for r in range(board.ROW_COUNT):		
                if board.get_row_col(r, c) == 1:
                    pygame.draw.circle(self.screen, self.RED, (int(c*self.SQUARESIZE+self.SQUARESIZE/2),\
                         self.height-int(r*self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
                elif board.get_row_col(r, c) == 2: 
                    pygame.draw.circle(self.screen, self.YELLOW, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), \
                        self.height-int(r*self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
        self.update_gboard()

    def draw_rect(self, colour, params):
        pygame.draw.rect(self.screen, colour, params)

    def draw_circle(self, colour, params, radius):
        pygame.draw.circle(self.screen, colour, params, radius)

    def write_on_board(self, text, color, posx, posy, fontsize, inCenter = False):
        textfont = pygame.font.SysFont("inkfree", fontsize)
        text_surface = textfont.render(text, True, color)
        if(inCenter):
            text_position = text_surface.get_rect(center = (posx, posy))
        else:
            text_position = text_surface.get_rect(topleft = (posx, posy))
        self.screen.blit(text_surface, text_position)
    
    def draw_button(self, button, screen):
        pygame.draw.rect(screen, button['color'], button['button position'], 1)
        screen.blit(button['text surface'], button['text rectangle'])

    def create_button(self, posx, posy, width, height, label, callback, optional_arguments = None):
        textfont = pygame.font.SysFont("inkfree", 25)
        text_surface = textfont.render(label, True, self.WHITE)

        button_position = pygame.Rect(posx, posy, width, height)
        text_rectangle = text_surface.get_rect(topleft = (posx + 10, posy + 5))
        button = {
            'button position': button_position,
            'text surface': text_surface,
            'text rectangle': text_rectangle,
            'color': self.WHITE,
            'callback': callback,
            'args': optional_arguments,
            }
        return button