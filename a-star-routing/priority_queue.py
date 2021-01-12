PriorityQueue = {}


def initPriorityQueue():
    PriorityQueue["arrTuple"] = []
    PriorityQueue["head"] = 0
    PriorityQueue["tail"] = 0
    return


def swap(x, y):
    x[0], y[0] = y[0], x[0]
    x[1], y[1] = y[1], x[1]


def add(tupleInput):
    PriorityQueue["arrTuple"].append(tupleInput)
    PriorityQueue["tail"] += 1
    i = PriorityQueue["tail"] - 1
    while (
        i > PriorityQueue["head"]
        and PriorityQueue["arrTuple"][i][0] < PriorityQueue["arrTuple"][i - 1][0]
    ):
        swap(PriorityQueue["arrTuple"][i], PriorityQueue["arrTuple"][i - 1])
        i -= 1


def delete():
    if PriorityQueue["head"] != PriorityQueue["tail"]:
        PriorityQueue["head"] += 1
        return PriorityQueue["arrTuple"][PriorityQueue["head"] - 1]
