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
        if args.inputfile is not None:
            sys.stdin = open(args.inputfile, "r")
        height, length, steps = list(map(int, input().split()))
        game = lib.CLifegame(height, length)
        for i in range(height):
            string_of_field = list(input())
            game.full_field(i, string_of_field)
        game.play(steps)
        if args.outputfile is not None:
            sys.stdout = open(args.outputfile, "w")
        for i in range(height):
            for j in range(length):
                print(game.get_cell(i, j), end='')
            print()


if __name__ == "__main__":
    run()
