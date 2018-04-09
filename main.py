import lib
import tests

if __name__ == "__main__":
    ans = input()
    '''При вводе флага test исполняется файл с тестами;
        флага file - производится вывод и ввод из файла;
        иного флага(например, go) - консольный вывод и ввод'''
    if ans == "test":
        tests.test()
    else:
        lib.run(ans)
