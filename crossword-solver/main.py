import sys
import copy
import os
import time
from crossword import Crossword
from crossword import Block


if __name__ == "__main__":
    crossword = Crossword("./crossword-solver/example.crossword.json")
    crossword.solve()