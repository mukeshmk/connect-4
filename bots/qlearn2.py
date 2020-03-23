import random

class QLearn2:
    def __init__(self, piece, depth=3):
        self.bot_piece = piece
        if self.bot_piece == 1:
            self.opp_piece = 2
        else:
            self.opp_piece = 1
        self.depth=depth

    def getMove(self, board):
        potentialMoves = self.getPotentialMoves(board, self.depth)
        # get the best fitness from the potential moves
        best_fitness_score = -1 #min(potentialMoves)
        for col in board.get_valid_locations():
            if potentialMoves[col] > best_fitness_score and board.is_valid_location(col):
                best_fitness_score = potentialMoves[col]
        # find all potential moves that have this best fitness
        best_moves = []
        for col in range(len(potentialMoves)):
            if potentialMoves[col] == best_fitness_score and board.is_valid_location(col):
                best_moves.append(col)

        return random.choice(best_moves)

    def getPotentialMoves(self, board, depth):
        if depth == 0 or board.check_draw():
            return [0] * board.COLUMN_COUNT

        # Figure out the best move to make.
        potentialMoves = [0] * board.COLUMN_COUNT
        no_of_moves = len(board.get_valid_locations())
        for col in board.get_valid_locations():
            b_copy = board.copy_board()
            if not b_copy.is_valid_location(col):
                continue
            row = b_copy.get_next_open_row(col)
            b_copy.drop_piece(row, col, self.bot_piece)
            b_copy.print_board()
            if b_copy.winning_move(self.bot_piece):
                # a winning move automatically gets a perfect fitness
                potentialMoves[col] = 1
                break # don't bother calculating other moves
            else:
                # do other player's counter moves and determine best one
                if b_copy.check_draw():
                    potentialMoves[col] = 0
                else:
                    for counterMove in b_copy.get_valid_locations():
                        b2_copy = b_copy.copy_board()
                        if not b2_copy.is_valid_location(counterMove):
                            continue
                        row = b_copy.get_next_open_row(counterMove)
                        b2_copy.drop_piece(row, counterMove, self.opp_piece)
                        b2_copy.print_board()
                        if b2_copy.winning_move(self.opp_piece):
                            # a losing move automatically gets the worst fitness
                            potentialMoves[counterMove] = 1
                            break
                        else:
                            # do the recursive call to getPotentialMoves()
                            results = self.getPotentialMoves(b2_copy, depth - 1)
                            potentialMoves[counterMove] += (sum(results) / no_of_moves / no_of_moves)
        return potentialMoves