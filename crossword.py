from typing import List
import json
from puzzle import Puzzle
from block import Block


class Crossword:
    def __init__(self, puzzle: Puzzle, words: List[str]):
        self.puzzle = puzzle
        self.words = words

    @classmethod
    def read_json(cls, json_file: str) -> "Crossword":
        with open(json_file) as f:
            data = json.load(f)

        height = len(data["puzzle"])
        width = len(data["puzzle"][0])
        puzzle = Puzzle(height, width, list("".join(data["puzzle"])))

        return Crossword(puzzle, data["words"])


if __name__ == "__main__":
    crossword = Crossword.read_json("./assets/example.crossword.json")
    print(crossword.words)
    print(crossword.puzzle)
