import lib
import tests
import argparse
import sys


def set_parser_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputfile', action='store') #Имя входного файла
    parser.add_argument('--outputfile', action='store') #Имя выходного поля
    parser.add_argument('--tests', action='store_true') #Флаг для запуска тестов
    return parser.parse_args()


def run():
    args = set_parser_args()
    if args.tests:
        tests.test()
    else:
        if args.inputfile is not None:
            sys.stdin = open(args.inputfile, "r")
        height, length, steps = list(map(int, input().split())) #Высота, длина игрового поля и количество итераций игры
        game = lib.CLifegame(height, length) #Непосрадственоо игра
        for i in range(height):
            string_of_field = list(input()) #Строка игрового поля
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
