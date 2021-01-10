from typing import List
from block import Block


class Puzzle:
    def __init__(self, height: int, width: int, elements: List[str]):
        self.height = height
        self.width = width
        self.elements = elements
        self.blocks = self._get_blocks()

    def index(self, row: int, col: int) -> int:
        return self.height * row + col

    def getAt(self, row: int, col: int) -> str:
        return self.elements[self.index(row, col)]

    def setAt(self, row: int, col: int, element: str):
        self.elements[self.index(row, col)] = element

    def display(self):
        for i in range(self.height):
            for j in range(self.width):
                print(self.getAt(i, j), end=" ")
            print()

    def fill(self, block: Block, elements: List[str]):
        if block.horizontal:
            for i in range(block.length):
                self.setAt(block.row, block.col + i, elements[i])
        else:
            for i in range(block.length):
                self.setAt(block.row + i, block.col, elements[i])

    def get_block(self, length) -> List[Block]:
        return list(filter(lambda block: block.length == length, self.blocks))

    def is_word_match(self, word: str, block: Block) -> bool:
        if block.length != len(word):
            return False

        i, j = 0, 0
        while i + j < block.length:
            block_char = self.getAt(block.row + i, block.col + j)
            if block_char != "-" and block_char != word[i + j]:
                return False

            i += 0 if block.horizontal else 1
            j += 1 if block.horizontal else 0

        return True

    def _get_blocks(self) -> List[Block]:
        blocks = []
        # horizontal
        for i in range(self.height):
            j = 0
            while j < self.width:
                if self.getAt(i, j) != "#":
                    k = 0
                    while j + k < self.width and self.getAt(i, j + k) != "#":
                        k += 1
                    if k > 1:
                        blocks.append(Block(i, j, k, True))
                    j += k
                else:
                    j += 1

        # vertical
        for j in range(self.height):
            i = 0
            while i < self.width:
                if self.getAt(i, j) != "#":
                    k = 0
                    while i + k < self.height and self.getAt(i + k, j) != "#":
                        k += 1
                    if k > 1:
                        blocks.append(Block(i, j, k, False))
                    i += k
                else:
                    i += 1
        return blocks
