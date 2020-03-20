import random

class OneStepLookAheadBot():
    def __init__(self):
        pass

    def getBotMove(self, board):
        valid_moves = board.get_valid_locations()

        win_move_set = set()
        fallback_move_set = set()
        stop_loss_move_set = set()

        for move in valid_moves:
            row = board.get_next_open_row(move)
            bot_copy = board.copy_board()
            player_copy = board.copy_board()

            bot_copy.drop_piece(row, move, bot_copy.BOT_PIECE)
            if bot_copy.winning_move(bot_copy.BOT_PIECE):
                win_move_set.add(move)

            player_copy.drop_piece(row, move, player_copy.PLAYER_PIECE)
            if player_copy.winning_move(player_copy.PLAYER_PIECE):
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
