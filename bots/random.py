import random

class RandomBot:
    def __init__(self):
        pass

    def getMove(self, board):
        return random.randint(0, board.COLUMN_COUNT-1)
