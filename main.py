import lib
import tests

if __name__ == "__main__":
    ans = input()
    if ans == "test":
        tests.test()
    else:
        lib.run(ans)
