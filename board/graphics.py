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
                if board.getRowCol(r, c) == 1:
                    pygame.draw.circle(self.screen, self.RED, (int(c*self.SQUARESIZE+self.SQUARESIZE/2),\
                         self.height-int(r*self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
                elif board.getRowCol(r, c) == 2: 
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

    def button(self, label, posx, posy, width, height, action):
        mouse_position = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        textfont = pygame.font.SysFont("inkfree", 25)
        text_surface = textfont.render(label, True, self.WHITE)
        text_position = text_surface.get_rect(topleft = (posx + 5, posy + 5 ))

        if posx + width > mouse_position[0] > posx and posy + height > mouse_position[1] > posy:
            pygame.draw.rect(self.screen, self.WHITE, (posx, posy, width, height), 1)

            if click[0] == 1 and action != None:
               action()

        else:
            pygame.draw.rect(self.screen, self.WHITE, (posx, posy, width, height), 1)

        self.screen.blit(text_surface, text_position)