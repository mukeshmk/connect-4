import random
import math

class MiniMaxBot:
	def __init__(self):
		pass

	def evaluate_window(self, board, window, piece):
		score = 0
		opp_piece = board.PLAYER_PIECE
		if piece == board.PLAYER_PIECE:
			opp_piece = board.BOT_PIECE

		if window.count(piece) == 4:
			score += 100
		elif window.count(piece) == 3 and window.count(board.EMPTY) == 1:
			score += 5
		elif window.count(piece) == 2 and window.count(board.EMPTY) == 2:
			score += 2

		if window.count(opp_piece) == 3 and window.count(board.EMPTY) == 1:
			score -= 4

		return score

	def score_position(self, board, piece):
		score = 0

		## Score center column
		center_array = [int(i) for i in list(board.getBoard()[:, board.COLUMN_COUNT//2])]
		center_count = center_array.count(piece)
		score += center_count * 3

		## Score Horizontal
		for r in range(board.ROW_COUNT):
			row_array = [int(i) for i in list(board.getBoard()[r,:])]
			for c in range(board.COLUMN_COUNT-3):
				window = row_array[c:c+board.WINDOW_LENGTH]
				score += self.evaluate_window(board, window, piece)

		## Score Vertical
		for c in range(board.COLUMN_COUNT):
			col_array = [int(i) for i in list(board.getBoard()[:,c])]
			for r in range(board.ROW_COUNT-3):
				window = col_array[r:r+board.WINDOW_LENGTH]
				score += self.evaluate_window(board, window, piece)

		## Score positive sloped diagonal
		for r in range(board.ROW_COUNT-3):
			for c in range(board.COLUMN_COUNT-3):
				window = [board.getBoard()[r+i][c+i] for i in range(board.WINDOW_LENGTH)]
				score += self.evaluate_window(board, window, piece)

		## Score negative sloped diagonal
		for r in range(board.ROW_COUNT-3):
			for c in range(board.COLUMN_COUNT-3):
				window = [board.getBoard()[r+3-i][c+i] for i in range(board.WINDOW_LENGTH)]
				score += self.evaluate_window(board, window, piece)

		return score

	def is_terminal_node(self, board):
		return board.winning_move(board.PLAYER_PIECE) or board.winning_move(board.BOT_PIECE) or len(board.get_valid_locations()) == 0

	def minimax(self, board, depth, alpha, beta, maximizingPlayer):
		valid_locations = board.get_valid_locations()
		is_terminal = self.is_terminal_node(board)

		if depth == 0 or is_terminal:
			if is_terminal:
				if board.winning_move(board.BOT_PIECE):
					return (None, 100000000000000)
				elif board.winning_move(board.PLAYER_PIECE):
					return (None, -10000000000000)
				else: # Game is over, no more valid moves
					return (None, 0)
			else: # Depth is zero
				return (None, self.score_position(board, board.BOT_PIECE))

		if maximizingPlayer:
			value = -math.inf
			column = random.choice(valid_locations)
			for col in valid_locations:
				row = board.get_next_open_row(col)
				
				b_copy = board.copy_board()
				b_copy.drop_piece(row, col, board.BOT_PIECE)
				new_score = self.minimax(b_copy, depth-1, alpha, beta, False)[1]
				
				if new_score > value:
					value = new_score
					column = col
				
				alpha = max(alpha, value)
				if alpha >= beta:
					break
			return column, value
		else: # Minimizing player
			value = math.inf
			column = random.choice(valid_locations)
			for col in valid_locations:
				row = board.get_next_open_row(col)

				b_copy = board.copy_board()
				b_copy.drop_piece(row, col, board.PLAYER_PIECE)
				new_score = self.minimax(b_copy, depth-1, alpha, beta, True)[1]
				
				if new_score < value:
					value = new_score
					column = col
				
				beta = min(beta, value)
				if alpha >= beta:
					break
			return column, value

	def getMove(self, board):
		col, minimax_score = self.minimax(board, 5, -math.inf, math.inf, True)
		return col
