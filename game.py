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
    'expectimax': ExpectiMaxBot,
    'montecarlo': MonteCarloBot
}

name_map = {
    'human': 'Human',
    'random': 'Random Bot',
    'onestep': 'One Step Look Ahead Bot',
    'minimax': 'MiniMax Bot',
    'expectimax': 'ExpectiMax Bot',
    'montecarlo': 'Monte Carlo Tree Search Bot'
}

board = Board(1)

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def main(first_player = None, second_player = None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--p1', help='Player 1 type (default Human)', type=str)
    parser.add_argument('--p2', help='Player 2 type (default Human)', type=str)
    parser.add_argument('--ui', help='turn UI off in case of a bot vs bot match', type=str2bool, nargs='?', const=True, default=True)
    parser.add_argument('--bots', help='Lists the Bots available to play with', type=str2bool, nargs='?', const=True, default=False)
    args = parser.parse_args()

    if args.p1 is None and args.p2 is None and args.ui and first_player is None:
        main_screen()

    print("\n")
    if args.bots:
        print('The available bots to play with are:')
        print('Random Int Bot (random)')
        print('One Step Look Ahead Bot (onestep)')
        print('MiniMax Bot (minimax)')
        print('ExpectiMax Bot (expectimax)')
        print('Monte Carlo Tree Search Bot (montecarlo)')
        print()
        print('Use the string in the brackets to pass as argument to p1 and p2')
        exit(1)

    p1 = p2 = None
    
    if first_player != None:
        args.p1 = first_player
        args.p2 = second_player

    if args.p1 is None or args.p2 is None:
        print('Set both p1 and p2 args')
        sys.exit()

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

    if args.ui == False and (Human == type(p1) or Human == type(p2)):
        print("Can not play game as Human without UI!")
        exit(1)

    connect4(p1, p2, args.ui)

def main_screen():
    pygame.init()
    pygame.display.set_caption("Connect Four | AI Project")
    # board = Board(1)
    graphics_board = GBoard(board)

    def human_vs_human():
        main("human", "human")

    player_vs_player_button = graphics_board.create_button(60, 220, 300, 40, '1. PLAYER VS PLAYER', human_vs_human)
    player_vs_bot_button = graphics_board.create_button(60, 280, 300, 40, '2. PLAYER VS BOT', bot_vs_human_screen)
    bot_vs_bot_button = graphics_board.create_button(60, 340, 300, 40, '3. BOT VS BOT', bot_vs_bot_screen)
    quit_button = graphics_board.create_button(60, 600, 100, 40, 'QUIT', sys.exit)

    button_list = [player_vs_player_button, player_vs_bot_button, bot_vs_bot_button, quit_button]

    while True:
        graphics_board.write_on_board("CONNECT 4 GAME", graphics_board.RED , 350 , 100, 60, True)
        graphics_board.write_on_board("CHOOSE ONE OF THE OPTIONS TO PLAY", graphics_board.YELLOW , 350 , 175, 30, True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in button_list:
                        if button['button position'].collidepoint(event.pos):
                            button['callback']()
            
            elif event.type == pygame.MOUSEMOTION:
                for button in button_list:
                    if button['button position'].collidepoint(event.pos):
                        button['color'] = graphics_board.RED
                    else:
                        button['color'] = graphics_board.WHITE

        for button in button_list:
            graphics_board.draw_button(button, graphics_board.screen)

        pygame.display.update()

def bot_vs_human_screen():
    pygame.init()
    # board = Board(1)
    graphics_board = GBoard(board)

    def human_vs_minimax():
        main("human", "minimax")

    def human_vs_expectimax():
        main("human", "expectimax")
    
    def human_vs_montecarlo():
        main("human", "montecarlo")

    minimax_button = graphics_board.create_button(60, 220, 400, 40, '1. MINIMAX BOT', human_vs_minimax)
    expectimax_button = graphics_board.create_button(60, 280, 400, 40, '2. EXPECTIMAX BOT', human_vs_expectimax)
    montecarlo_button = graphics_board.create_button(60, 340, 400, 40, '3. MONTECARLO SEARCH BOT', human_vs_montecarlo)
    
    back_button = graphics_board.create_button(60, 600, 100, 40, 'BACK', main_screen)
    quit_button = graphics_board.create_button(180, 600, 100, 40, 'QUIT', sys.exit)

    button_list = [minimax_button, expectimax_button, montecarlo_button, back_button, quit_button]

    while True:
        graphics_board.write_on_board("CONNECT 4 GAME", graphics_board.RED , 350 , 100, 60, True)
        graphics_board.write_on_board("CHOOSE THE BOT TO PLAY AGAINST", graphics_board.YELLOW , 350 , 175, 30, True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in button_list:
                        if button['button position'].collidepoint(event.pos):
                            button['callback']()
            
            elif event.type == pygame.MOUSEMOTION:
                for button in button_list:
                    if button['button position'].collidepoint(event.pos):
                        button['color'] = graphics_board.RED
                    else:
                        button['color'] = graphics_board.WHITE

        for button in button_list:
            graphics_board.draw_button(button, graphics_board.screen)

        pygame.display.update()

def bot_vs_bot_screen():
    pygame.init()
    # board = Board(1)
    graphics_board = GBoard(board)

    first_bot = second_bot = None

    def bots_to_play_against(bot_to_play):
        nonlocal first_bot, second_bot

        if first_bot == None:
            first_bot = bot_to_play
        elif second_bot == None and first_bot != None:
            second_bot= bot_to_play

        if first_bot != None and second_bot != None:
            main(first_bot, second_bot)

    minimax_button = graphics_board.create_button(60, 220, 400, 40, '1. MINIMAX BOT',  bots_to_play_against, ("minimax"))
    expectimax_button = graphics_board.create_button(60, 280, 400, 40, '2. EXPECTIMAX BOT', bots_to_play_against, ("expectimax"))
    montecarlo_button = graphics_board.create_button(60, 340, 400, 40, '3. MONTECARLO SEARCH BOT', bots_to_play_against, ("montecarlo"))
    
    back_button = graphics_board.create_button(60, 600, 100, 40, 'BACK', main_screen)
    quit_button = graphics_board.create_button(180, 600, 100, 40, 'QUIT', sys.exit)

    button_list = [minimax_button, expectimax_button, montecarlo_button, back_button, quit_button]

    while True:
        graphics_board.write_on_board("CONNECT 4 GAME", graphics_board.RED , 350 , 100, 60, True)
        graphics_board.write_on_board("CHOOSE ANY TWO BOT(S) TO PLAY", graphics_board.YELLOW , 350 , 175, 30, True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in button_list:
                        if button['button position'].collidepoint(event.pos):
                            if(button['args'] != None):
                                button['callback'](button['args'])
                            else:
                                button['callback']()
            
            elif event.type == pygame.MOUSEMOTION:
                for button in button_list:
                    if button['button position'].collidepoint(event.pos):
                        button['color'] = graphics_board.RED
                    else:
                        button['color'] = graphics_board.WHITE                
        
        for button in button_list:
            graphics_board.draw_button(button, graphics_board.screen)

        pygame.display.update()

if __name__ == '__main__':
    main()
