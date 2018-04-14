import lib
import tests
import argparse
import sys


def set_parser_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputfile', action='store')
    parser.add_argument('--outputfile', action='store')
    parser.add_argument('--tests', action='store_true')
    return parser.parse_args()


def run():
    args = set_parser_args()
    if args.tests:
        tests.test()
    else:
        if not(args.inputfile is None):
            sys.stdin = open(args.inputfile, "r")
        height, length, steps = input().split()
        height = int(height)
        length = int(length)
        steps = int(steps)
        game = lib.CLifegame(height, length)
        for i in range(height):
            string_of_field = list(input())
            game.full_field(i, string_of_field)
        game.play(steps)
        if not(args.outputfile is None):
            sys.stdout = open(args.outputfile, "w")
        for i in range(height):
            for j in range(length):
                print(game.get_cell(i, j), end='')
            print()


if __name__ == "__main__":
    run()
