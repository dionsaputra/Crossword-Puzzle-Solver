import copy
from priority_queue import PriorityQueue


class Graph:
    def __init__(self, input_graph):
        vertex = len(input_graph)
        self.vertex = vertex
        self.storage = [[0 for _ in range(vertex + 1)] for _ in range(vertex + 1)]
        self.sum = [0 for _ in range(vertex + 1)]

        for i in range(vertex):
            for j in range(vertex):
                self.setEdge(i, j, input_graph[i][j])

    def setEdge(self, source: int, destination: int, weight: float):
        self.storage[source][destination] = weight
        self.storage[destination][source] = weight

    def a_star(self, input_graph, heuristic):
        queue = PriorityQueue()

        i = 0
        solution = [i]

        while not self.vertex - 1 in solution:
            candidate = copy.deepcopy(self.storage[i])
            for j in range(len(candidate)):
                if self.storage[i][j] > 0:
                    queue.push([self.sum[i] + self.storage[i][j] + heuristic[j], j])
                    self.sum[j] = self.sum[i] + self.storage[i][j]

            nextNode = queue.pop()

            while self.storage[solution[len(solution) - 1]][nextNode[1]] <= 0:
                solution = solution[:-1]

            solution.append(nextNode[1])
            i = nextNode[1]

        return solution
