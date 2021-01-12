graph = {}


def initGraph(vrtx):
    graph["vertex"] = vrtx
    graph["storage"] = []
    for i in range(0, vrtx + 1):
        temp = []
        for j in range(0, vrtx + 1):
            temp.append(0)
        graph["storage"].append(temp)
    graph["sum"] = temp
    return


def addEdgeGraph(src, dest, weight):
    graph["storage"][src][dest] = weight
    graph["storage"][dest][src] = weight
    return


def displayGraph():
    for i in range(graph["vertex"]):
        for j in range(graph["vertex"]):
            print(graph["storage"][i][j], end=" ")
        print(end="\n")


class Graph:
    def __init__(self, vertex):
        self.vertex = vertex
        self.storage = []
        for _ in range(0, vertex + 1):
            temp = []
            for _ in range(0, vertex + 1):
                temp.append(0)
            self.storage.append(temp)
        self.sum = temp