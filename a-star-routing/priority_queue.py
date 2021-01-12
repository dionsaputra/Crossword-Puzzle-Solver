class PriorityQueue:
    def __init__(self):
        self.tuples = []
        self.head = 0
        self.tail = 0

    def push(self, element):
        self.tuples.append(element)
        self.tail += 1
        i = self.tail - 1
        while i > self.head and self.tuples[i][0] < self.tuples[i - 1][0]:
            self.swap(self.tuples[i], self.tuples[i - 1])
            i -= 1

    def pop(self):
        if self.head != self.tail:
            self.head += 1
            return self.tuples[self.head - 1]

    @staticmethod
    def swap(x, y):
        x[0], y[0] = y[0], x[0]
        x[1], y[1] = y[1], x[1]