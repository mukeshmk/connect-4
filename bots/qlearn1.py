import random

class QLearn1:
	def __init__(self, piece):
		self.bot_piece = piece
		if self.bot_piece == 1:
			self.opp_piece = 2
		else:
			self.opp_piece = 1

		self.q = {}
		self.epsilon = 0.2 # a greedy chance of random exploration
		self.alpha = 0.3 # learning rate
		self.gamma = 0.9 # discount factor for future rewards

	def check_win(self, board, piece):
		if board.winning_move(piece):
			return True
		if board.check_draw():
			return True
		return False

	def update_params(self, epsilon, alpha, gamma):
		self.epsilon = epsilon
		self.alpha = alpha
		self.gamma = gamma

	def get_state(self, state):
		return tuple(tuple(x) for x in state)

	def getQ(self, state, action):
		# encourage exploration; "optimistic" 1.0 initial values
		if self.q.get((state, action)) is None:
			self.q[(state, action)] = 1.0
		return self.q.get((state, action))

	def choose_action(self, state, actions):
		current_state = state

		if random.random() < self.epsilon: # explore!
			chosen_action = random.choice(actions)
			return chosen_action

		qs = [self.getQ(current_state, a) for a in actions]
		maxQ = max(qs)

		if qs.count(maxQ) > 1:
			# more than 1 best option; choose among them randomly
			best_options = [i for i in range(len(actions)) if qs[i] == maxQ]
			i = random.choice(best_options)
		else:
			i = qs.index(maxQ)

		return actions[i]

	def learn(self, prev_board, board, actions, chosen_action, game_over):
		reward = 0
		if (game_over):
			winner = board.get_winner()
			if winner == 0:
				reward = 0.5
			elif winner == self.bot_piece:
				reward = 2
			else:
				reward = -2

		prev_state = self.get_state(prev_board.getBoard())
		prev = self.getQ(prev_state, chosen_action)
		result_state = self.get_state(board.getBoard())

		maxqnew = max([self.getQ(result_state, a) for a in actions])
		self.q[(prev_state, chosen_action)] = prev + self.alpha * ((reward + self.gamma * maxqnew) - prev)

	def getMove(self, board):
		b_copy = board.copy_board()

		actions = b_copy.get_valid_locations()
		state = self.get_state(b_copy.getBoard())
		chosen_action = self.choose_action(state, actions)

		row = b_copy.get_next_open_row(chosen_action)
		b_copy.drop_piece(row, chosen_action, self.bot_piece)

		game_over = self.check_win(b_copy, self.bot_piece)
		self.learn(board, b_copy, actions, chosen_action, game_over)

		print(self.q.values())

		return chosen_action
