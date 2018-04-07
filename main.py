import lib
import tests

if __name__ == "__main__":
    ans = input()
    if ans == "test":
        tests.test()
    elif ans == "file":
        lib.file_run()
    else:
        lib.run()
