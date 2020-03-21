import random
import math

class ExpectiMaxBot:
	def __init__(self, piece):
		self.bot_piece = piece
		if self.bot_piece == 1:
			self.opp_piece = 2
		else:
			self.opp_piece = 1

	def evaluate_window(self, board, window):
		score = 0
		if window.count(self.bot_piece) == 4:
			score += 100
		elif window.count(self.bot_piece) == 3 and window.count(board.EMPTY) == 1:
			score += 5
		elif window.count(self.bot_piece) == 2 and window.count(board.EMPTY) == 2:
			score += 2

		if window.count(self.opp_piece) == 3 and window.count(board.EMPTY) == 1:
			score -= 4

		return score

	def score_position(self, board):
		score = 0

		## Score center column
		center_array = [int(i) for i in list(board.getBoard()[:, board.COLUMN_COUNT//2])]
		center_count = center_array.count(self.bot_piece)
		score += center_count * 3

		## Score Horizontal
		for r in range(board.ROW_COUNT):
			row_array = [int(i) for i in list(board.getBoard()[r,:])]
			for c in range(board.COLUMN_COUNT-3):
				window = row_array[c:c+board.WINDOW_LENGTH]
				score += self.evaluate_window(board, window)

		## Score Vertical
		for c in range(board.COLUMN_COUNT):
			col_array = [int(i) for i in list(board.getBoard()[:,c])]
			for r in range(board.ROW_COUNT-3):
				window = col_array[r:r+board.WINDOW_LENGTH]
				score += self.evaluate_window(board, window)

		## Score positive sloped diagonal
		for r in range(board.ROW_COUNT-3):
			for c in range(board.COLUMN_COUNT-3):
				window = [board.getBoard()[r+i][c+i] for i in range(board.WINDOW_LENGTH)]
				score += self.evaluate_window(board, window)

		## Score negative sloped diagonal
		for r in range(board.ROW_COUNT-3):
			for c in range(board.COLUMN_COUNT-3):
				window = [board.getBoard()[r+3-i][c+i] for i in range(board.WINDOW_LENGTH)]
				score += self.evaluate_window(board, window)

		return score

	def is_terminal_node(self, board):
		return board.winning_move(self.bot_piece) or board.winning_move(self.opp_piece) or len(board.get_valid_locations()) == 0

	def expectimax(self, board, depth, alpha, beta, maximizingPlayer):
		valid_locations = board.get_valid_locations()
		is_terminal = self.is_terminal_node(board)

		if depth == 0 or is_terminal:
			if is_terminal:
				if board.winning_move(self.bot_piece):
					return (None, 100000000000000)
				elif board.winning_move(self.opp_piece):
					return (None, -10000000000000)
				else: # Game is over, no more valid moves
					return (None, 0)
			else: # Depth is zero
				return (None, self.score_position(board))

		if maximizingPlayer:
			value = -math.inf
			column = random.choice(valid_locations)
			for col in valid_locations:
				row = board.get_next_open_row(col)
				
				b_copy = board.copy_board()
				b_copy.drop_piece(row, col, self.bot_piece)
				new_score = self.expectimax(b_copy, depth-1, alpha, beta, False)[1]
				
				if new_score > value:
					value = new_score
					column = col
				
				alpha = max(alpha, value)
				if alpha >= beta:
					break
			return column, value
		else: # Expecting player
			value = 0
			column = random.choice(valid_locations)
			for col in valid_locations:
				row = board.get_next_open_row(col)

				b_copy = board.copy_board()
				b_copy.drop_piece(row, col, self.opp_piece)
				new_score = self.expectimax(b_copy, depth-1, alpha, beta, True)[1]
				
				if new_score <= value:
					value = new_score
					column = col
				
				beta = math.floor(value/len(valid_locations))
				if alpha >= beta:
					break
			return column, value

	def getMove(self, board):
		col, expectimax_score = self.expectimax(board, 6, -math.inf, 0, True)
		return col
