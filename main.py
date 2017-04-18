import sys
from os import system


if __name__ == "__main__":
    if sys.argv[1] == "test":
        system("pytest --cache-clear --durations=10 --cov=tests/")
    else:
        from gui_ import main
        main.main()
