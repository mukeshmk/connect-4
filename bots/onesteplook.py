import random

class OneStepLookAheadBot():
    def __init__(self, bot_piece):
        self.bot_piece = bot_piece
        if bot_piece == 1:
            self.opp_piece = 2
        else:
            self.opp_piece = 1

    def get_move(self, board):
        valid_moves = board.get_valid_locations()

        win_move_set = set()
        fallback_move_set = set()
        stop_loss_move_set = set()

        for move in valid_moves:
            bot_copy = board.copy_board()
            player_copy = board.copy_board()

            bot_copy.drop_piece(move, self.bot_piece)
            if bot_copy.winning_move(self.bot_piece):
                win_move_set.add(move)

            player_copy.drop_piece(move, self.opp_piece)
            if player_copy.winning_move(self.opp_piece):
                stop_loss_move_set.add(move)
            else:
                fallback_move_set.add(move)

        if len(win_move_set) > 0:
            ret_move = random.choice(list(win_move_set))
        elif len(stop_loss_move_set) > 0:
            ret_move = random.choice(list(stop_loss_move_set))
        elif len(fallback_move_set) > 0:
            ret_move = random.choice(list(fallback_move_set))

        return ret_move
