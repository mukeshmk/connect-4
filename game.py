import argparse
import sys

#pygame version number and welcome message hidden.
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
from bots import *
from board import *
from connect4 import connect4

bot_map = {
    'human': Human,
    'random': RandomBot,
    'onestep': OneStepLookAheadBot,
    'minimax': MiniMaxBot,
    'expectimax': ExpectiMaxBot
}

name_map = {
    'human': 'Human',
    'random': 'Random Bot',
    'onestep': 'One Step Look Ahead Bot',
    'minimax': 'MiniMax Bot',
    'expectimax': 'ExpectiMax Bot'
}

class Players:
    def human_minimax(self):
        main("human", "minimax")

    def human_expectimax(self):
        main("human", "expectimax")

def main(first_player = None, second_player = None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--p1', help='Player 1 type (default Human)', type=str)
    parser.add_argument('--p2', help='Player 2 type (default Human)', type=str)
    parser.add_argument('--bots', help='Lists the Bots available to play with', type=bool)
    args = parser.parse_args()

    print("\n")
    if not args.bots is None:
        print('The available bots to play with are:')
        print('Random Int Bot (random)')
        print('One Step Look Ahead Bot (onestep)')
        print('MiniMax Bot (minimax)')
        print('ExpectiMax Bot (expectimax)')
        print()
        print('Use the string in the brackets to pass as argument to p1 and p2')
        exit(1)

    p1 = p2 = None
    
    args.p1 = first_player
    args.p2 = second_player

    if args.p1 is None or args.p1 == "human":
        print("Player 1 is set as a Human")
        p1 = Human(Board.PLAYER1_PIECE)
    else:
        for bot in bot_map:
            if bot == args.p1:
                p1 = bot_map[args.p1](Board.PLAYER1_PIECE)
        if p1 is None:
            print("oops! you have entered a wrong bot name for p1")
            exit(1)
        print("Player 1 is set as a " + name_map[args.p1])

    if args.p2 is None or args.p2 == "human":
        print("Player 2 is set as a Human")
        p2 = Human(Board.PLAYER2_PIECE)
    else:
        for bot in bot_map:
            if bot == args.p2:
                p2 = bot_map[args.p2](Board.PLAYER2_PIECE)
        if p2 is None:
            print("oops! you have entered a wrong bot name for p2")
            exit(1)
        print("Player 2 is set as a " + name_map[args.p2])

    print("\n")

    connect4(p1, p2)

def first_screen():
    global game_over, board, graphics_board
    pygame.init()
    pygame.display.set_caption("Connect Four | AI Project")
    board = Board()
    graphics_board = GBoard(board)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        graphics_board.write_on_board("CONNECT 4 GAME", graphics_board.RED , 350 , 100, 60, True)
        graphics_board.write_on_board("CHOOSE ONE OF THE OPTIONS TO PLAY", graphics_board.YELLOW , 350 , 175, 30, True)

        graphics_board.button("1. PLAYER VS PLAYER", 60, 220, 300, 40, main)
        graphics_board.button("2. PLAYER VS BOT", 60, 280, 300, 40, bot_vs_human)
        graphics_board.button("3. BOT VS BOT", 60, 340, 300, 40, bot_vs_bot)
        graphics_board.button("EXIT", 60, 600, 80, 40, sys.exit)
      
        pygame.display.update()

def bot_vs_human():
    pygame.init()
    board = Board()
    graphics_board = GBoard(board)

    players = Players()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        graphics_board.write_on_board("CONNECT 4 GAME", graphics_board.RED , 350 , 100, 60, True)
        graphics_board.write_on_board("CHOOSE THE BOT TO PLAY AGAINST", graphics_board.YELLOW , 350 , 175, 30, True)

        graphics_board.button("1. MINIMAX BOT", 60, 220, 400, 40, players.human_minimax)
        graphics_board.button("2. EXPECTIMAX BOT", 60, 280, 400, 40, players.human_expectimax)
        graphics_board.button("3. MONTECARLO SEARCH BOT", 60, 340, 400, 40, None)
        
        graphics_board.button("BACK", 60, 600, 80, 40,first_screen)
        graphics_board.button("EXIT", 180, 600, 80, 40, sys.exit)

        pygame.display.update()

def bot_vs_bot():
    pygame.init()
    board = Board()
    graphics_board = GBoard(board)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        graphics_board.write_on_board("CONNECT 4 GAME", graphics_board.RED , 350 , 100, 60, True)
        graphics_board.write_on_board("CHOOSE THE BOT(S) TO PLAY", graphics_board.YELLOW , 350 , 175, 30, True)

        graphics_board.button("1. MINIMAX BOT", 60, 220, 400, 40, None)
        graphics_board.button("2. EXPECTIMAX BOT", 60, 280, 400, 40, None)
        graphics_board.button("3. MONTECARLO SEARCH BOT", 60, 340, 400, 40, None)
        
        graphics_board.button("BACK", 60, 600, 80, 40,first_screen)
        graphics_board.button("EXIT", 180, 600, 80, 40, sys.exit)

        pygame.display.update()

if __name__ == '__main__':
    first_screen()