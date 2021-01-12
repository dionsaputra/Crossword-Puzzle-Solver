class Graph:
    def __init__(self, vertex: int):
        self.vertex = vertex
        self.storage = [[0 for _ in range(vertex + 1)] for _ in range(vertex + 1)]
        self.sum = [0 for _ in range(vertex + 1)]

    def setEdge(self, source: int, destination: int, weight: float):
        self.storage[source][destination] = weight
        self.storage[destination][source] = weight
