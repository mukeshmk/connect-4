import argparse
import sys
from bots import *
from board import Board
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

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--p1', help='Player 1 type (default Human)', type=str)
    parser.add_argument('--p2', help='Player 2 type (default Human)', type=str)
    parser.add_argument('--ui', help='turn UI off in case of a bot vs bot match', type=str2bool, nargs='?', const=True, default=True)
    parser.add_argument('--bots', help='Lists the Bots available to play with', type=str2bool, nargs='?', const=True, default=False)
    args = parser.parse_args()

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

    if args.p1 is None:
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

    if args.p2 is None:
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

if __name__ == '__main__':
    main()
