import numpy as np
import sys
import copy
import time
import random

class MonteCarloBot():
    def __init__(self, board, piece, initialNode = None, max_iterations = 20000 , timeout = 2):
        self.piece = piece
        self.max_iterations = max_iterations
        self.timeout = timeout
        self.currentNode = None

    def montecarlo_tree_search(self, board, max_iterations, currentNode = None, timeout = 100):
        rootnode = currentNode

        start = time.perf_counter()
        for i in range(max_iterations):
            node = rootnode
            state = board.copy_board()

            # selection
            # keep going down the tree based on best UCT values until terminal or unexpanded node
            while node.available_moves == [] and node.children != []:
                node = node.selection()
                state.update_move_list(node.move)

            # expand
            if node.available_moves != []:
                m = random.choice(node.available_moves)
                state.update_move_list(m)
                node = node.expand(m, state)

            # rollout
            while state.get_list_moves():
                state.update_move_list(random.choice(state.get_list_moves()))

            # backpropagate
            while node is not None:
                node.update(state.search_result(node.piece))
                node = node.parent

            duration = time.perf_counter() - start
            if duration > timeout: break

        foo = lambda x: x.wins/x.visits
        sorted_children = sorted(rootnode.children, key = foo)[::-1]
        for node in sorted_children:
            print('Move: %s Win Rate: %.2f%%' % (node.move + 1, 100 * node.wins / node.visits))
        print('Simulations performed: %s\n' % i)
        return rootnode, sorted_children[0].move

    def get_move(self, board):
        if self.currentNode is None:
            self.currentNode = Node(piece=self.piece, board=board)
        
        if board.LAST_COLUMN_POSITION is not None:
            last_column, last_piece = board.LAST_COLUMN_POSITION, board.LAST_PLAYER_PLAYED
            print(last_column, last_piece)
            self.currentNode = self.get_child_node(self.currentNode, board, last_column, last_piece)
            board.update_move_list(last_column)

        self.currentNode, col = self.montecarlo_tree_search(board, 10000, self.currentNode, 3)
        board.update_move_list(col)
        self.currentNode = self.get_child_node(self.currentNode, board, col, board.LAST_PLAYER_PLAYED)
        return col

    def get_child_node(self, node, board, move, piece):
        for child in node.children:
            if child.move == move:
                return child
        return Node(piece = piece, board = board)

class Node:
    def __init__(self, piece, move = None, parent = None, board = None):
        self.board = board.copy_board()
        self.parent = parent
        self.move = move
        self.available_moves = board.get_list_moves()
        self.children = []
        self.wins = 0
        self.visits = 0
        self.piece = piece

    def selection(self):
        # return child with largest UCT value
        foo = lambda x: x.wins / x.visits + np.sqrt(2 * np.log(self.visits) / x.visits)
        return sorted(self.children, key = foo)[-1]

    def expand(self, move, board):
        # return child when move is taken
        # remove move from current node
        child = Node(piece = board.LAST_PLAYER_PLAYED, move = move, parent = self, board=board)
        self.available_moves.remove(move)
        self.children.append(child)
        return child

    def update(self, result):
        self.wins += result
        self.visits += 1