class Graph:
    def __init__(self, vertex):
        self.vertex = vertex
        self.storage = [[0 for _ in range(vertex + 1)] for _ in range(vertex + 1)]
        self.sum = [0 for _ in range(vertex + 1)]

    def setEdge(self, source, destination, weight):
        self.storage[source][destination] = weight
        self.storage[destination][source] = weight
