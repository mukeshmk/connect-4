import pygame

pygame.init()

class GBoard:
    BLUE = (0,0,255)
    BLACK = (0,0,0)
    RED = (255,0,0)
    YELLOW = (255,255,0)

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

    def write_on_board(self, text, colour, pos):
        label = self.myfont.render(text, 1, colour)
        self.screen.blit(label, pos)

    def draw_rect(self, colour, params):
        pygame.draw.rect(self.screen, colour, params)

    def draw_circle(self, colour, params, radius):
        pygame.draw.circle(self.screen, colour, params, radius)

