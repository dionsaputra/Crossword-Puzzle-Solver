from typing import List
import json


class Matrix:
    def __init__(self, height: int, width: int, elements: List[str]):
        self.height = height
        self.width = width
        self.elements = elements

    def index(self, row: int, col: int) -> int:
        return self.height * row + col

    def getAt(self, row: int, col: int) -> str:
        return self.elements[self.index(row, col)]

    def setAt(self, row: int, col: int, element: str):
        self.elements[self.index(row, col)] = element


class Block:
    def __init__(self, head: [int, int], length: int, horizontal: bool):
        self.head = head
        self.length = length
        self.horizontal = horizontal


class Crossword:
    def __init__(self, puzzle: Matrix, words: List[str]):
        self.puzzle = puzzle
        self.words = words

    @classmethod
    def read_json(cls, json_file: str) -> "Crossword":
        with open(json_file) as f:
            data = json.load(f)

        height = len(data["puzzle"])
        width = len(data["puzzle"][0])
        puzzle = Matrix(height, width, list("".join(data["puzzle"])))

        return Crossword(puzzle, data["words"])

    @classmethod
    def display(cls, tts: Matrix):
        for i in range(tts.height):
            for j in range(tts.width):
                print(tts.getAt(i, j), end=" ")
            print()

    def get_blocks(self) -> List[Block]:
        ret = []
        # horizontal
        for i in range(self.puzzle.height):
            j = 0
            while j < self.puzzle.width:
                if self.puzzle.getAt(i, j) != "#":
                    head = [i, j]
                    k = 0
                    while (
                        j + k < self.puzzle.width and self.puzzle.getAt(i, j + k) != "#"
                    ):
                        k += 1
                    if k > 1:
                        ret.append(Block(head, k, True))
                    j += k
                else:
                    j += 1

        # vertical
        for j in range(self.puzzle.height):
            i = 0
            while i < self.puzzle.width:
                if self.puzzle.getAt(i, j) != "#":
                    head = [i, j]
                    k = 0
                    while (
                        i + k < self.puzzle.height
                        and self.puzzle.getAt(i + k, j) != "#"
                    ):
                        k += 1
                    if k > 1:
                        ret.append(Block(head, k, False))
                    i += k
                else:
                    i += 1
        return ret

    def get_block(self, length):
        allblocks = self.get_blocks()
        ret = []
        for i in range(len(allblocks)):
            if allblocks[i].length == length:
                ret.append(allblocks[i])
        return ret


if __name__ == "__main__":
    crossword = Crossword.read_json("./assets/example.crossword.json")
    print(crossword.words)
    print(crossword.puzzle)
