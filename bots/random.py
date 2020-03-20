import random

class RandomBot:
    def __init__(self, piece):
        self.bot_piece = piece

    def getMove(self, board):
        return random.randint(0, board.COLUMN_COUNT-1)
