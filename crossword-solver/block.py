class Block:
    def __init__(self, row: int, col: int, length: int, horizontal: bool):
        self.row = row
        self.col = col
        self.length = length
        self.horizontal = horizontal