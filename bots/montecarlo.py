import numpy as np
import sys
import copy
import time
import random

class MonteCarloBot():
    def __init__(self, piece, max_iterations = 20000 , timeout = 2):
        self.piece = piece
        self.max_iterations = max_iterations
        self.timeout = timeout
        self.currentNode = None

    def montecarlo_tree_search(self, board, max_iterations, currentNode, timeout = 100):
        rootnode = Node(piece=board.PREV_PLAYER, board=board)

        if currentNode is not None:
            rootnode = currentNode

        start = time.perf_counter()
        for i in range(max_iterations):
            node = rootnode
            state = board.copy_board()

            # selection
            # keep going down the tree based on best UCT values until terminal or unexpanded node
            while node.available_moves == [] and node.children != []:
                node = node.selection()
                state.drop_piece(node.move, state.CURR_PLAYER)

            # expand
            if node.available_moves != []:
                col = random.choice(node.available_moves)
                state.drop_piece(col, state.CURR_PLAYER)
                node = node.expand(col, state)

            # rollout
            while state.get_valid_locations():
                col = random.choice(state.get_valid_locations())
                state.drop_piece(col, state.CURR_PLAYER)
                if state.winning_move(state.PREV_PLAYER):
                    break

            # backpropagate
            while node is not None:
                node.update(state.search_result(node.piece))
                node = node.parent

            duration = time.perf_counter() - start
            if duration > timeout:
                break

        win_ratio = lambda x: x.wins/x.visits
        sorted_children = sorted(rootnode.children, key = win_ratio)[::-1]

        #for node in sorted_children:
        #    print('Move: %s Win Rate: %.2f%%' % (node.move + 1, 100 * node.wins / node.visits))
        #print('Simulations performed: %s\n' % i)

        return rootnode, sorted_children[0].move

    def get_child_node(self, node, board, move, piece):
        for child in node.children:
            if child.move == move:
                return child
        return Node(piece = piece, board = board)

    def get_move(self, board):
        if self.currentNode is None:
            self.currentNode = Node(piece=self.piece, board=board)
        
        if board.PREV_MOVE is not None:
            self.currentNode = self.get_child_node(self.currentNode, board, board.PREV_MOVE, board.CURR_PLAYER)

        self.currentNode, col = self.montecarlo_tree_search(board, self.max_iterations, self.currentNode, self.timeout)
        self.currentNode = self.get_child_node(self.currentNode, board, col, board.PREV_PLAYER)
        return col

class Node:
    def __init__(self, piece, board, parent=None, move=None):
        self.board = board.copy_board()
        self.parent = parent
        self.move = move
        self.available_moves = board.get_valid_locations()
        self.children = []
        self.wins = 0
        self.visits = 0
        self.piece = piece

    def selection(self):
        # return child with largest UCT value
        uct_val = lambda x: x.wins / x.visits + np.sqrt(2 * np.log(self.visits) / x.visits)
        return sorted(self.children, key = uct_val)[-1]

    def expand(self, move, board):
        # return child when move is taken
        # remove move from current node
        child = Node(piece = board.PREV_PLAYER, board = board, parent = self, move = move)
        self.available_moves.remove(move)
        self.children.append(child)
        return child

    def update(self, result):
        self.wins += result
        self.visits += 1
