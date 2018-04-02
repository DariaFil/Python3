import lib
import Tests

ans = input()
if ans == "test":
    Tests.test()
elif ans == "file":
    lib.file_run()
else:
    lib.run()
