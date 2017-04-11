import sys
import pytest
from os import system


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        system("pytest .")
    else:
        from gui_ import main
        main.main()
