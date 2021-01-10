import sys
import copy
import os
import time
from crossword_util import CrosswordUtil


def get_start(tts):
    [i, j] = [0, 0]
    while i < len(tts) and tts[i][j] != "-":
        if j + 1 == len(tts):
            i += 1
            j = 0
        else:
            j += 1

    return [i, j]


def is_solved(solusi):
    return len(solusi) <= 0


def clasify_solusi(solusi):
    tempsol = copy.deepcopy(solusi)
    maxlength = 0
    for i in range(len(tempsol)):
        if len(tempsol[i]) > maxlength:
            maxlength = len(tempsol[i])
    ret = []
    for i in range(maxlength + 1):
        ret.append([])

    for i in range(len(tempsol)):
        ret[len(tempsol[i])].append([len(ret[len(tempsol[i])]), tempsol[i]])

    i = 0
    while i < len(ret):
        if len(ret[i]) == 0:
            del ret[i]
        else:
            i += 1

    return ret


def get_min_class_idx(csol):
    minim = len(csol[0])
    idx = 0
    for i in range(1, len(csol)):
        if len(csol[i]) < minim:
            idx = i
            minim = len(csol[i])
    return idx


def get_all_block(tts):
    ret = []
    # horizontal
    for i in range(len(tts)):
        j = 0
        while j < len(tts):
            if tts[i][j] != "#":
                head = [i, j]
                k = 0
                while j + k < len(tts) and tts[i][j + k] != "#":
                    k += 1
                if k > 1:
                    ret.append((head, k, True))
                j += k
            else:
                j += 1
    # vertical
    for j in range(len(tts)):
        i = 0
        while i < len(tts):
            if tts[i][j] != "#":
                head = [i, j]
                k = 0
                while i + k < len(tts) and tts[i + k][j] != "#":
                    k += 1
                if k > 1:
                    ret.append([head, k, False])
                i += k
            else:
                i += 1
    return ret


def get_block_by_length(allblocks, length):
    ret = []
    for i in range(len(allblocks)):
        if allblocks[i][1] == length:
            ret.append(allblocks[i])
    return ret


def is_str_match(tts, string, head, length, datar):
    if length == len(string):
        match = True
        i = 0
        c1 = "-"
        if datar:
            while i < length and match:
                if (
                    tts[head[0]][head[1] + i] == c1
                    or tts[head[0]][head[1] + i] == string[i]
                ):
                    i += 1
                else:
                    match = False
        else:
            while i < length and match:
                if (
                    tts[head[0] + i][head[1]] == c1
                    or tts[head[0] + i][head[1]] == string[i]
                ):
                    i += 1
                else:
                    match = False
        return match
    else:
        return False


def get_idx_sol(tts, csol, level, head, length, datar):
    idx = 0
    found = False
    while idx < len(csol[level]) and not found:
        if is_str_match(tts, csol[level][idx][1], head, length, datar):
            found = True
        else:
            idx += 1

    if found:
        return idx
    else:
        return -1


def fill_tts(tts, head, length, datar, string):
    if datar:
        for i in range(length):
            tts[head[0]][head[1] + i] = string[i]

    else:
        for i in range(length):
            tts[head[0] + i][head[1]] = string[i]


def permutasi_solusi(solusi, length):

    pos1 = len(solusi[length]) - 1
    while pos1 > 0 and solusi[length][pos1][0] < solusi[length][pos1 - 1][0]:
        pos1 -= 1

    if pos1 > 0:
        pos2 = len(solusi[length]) - 1
        while solusi[length][pos2][0] < solusi[length][pos1 - 1][0]:
            pos2 -= 1
        [solusi[length][pos1 - 1], solusi[length][pos2]] = [
            solusi[length][pos2],
            solusi[length][pos1 - 1],
        ]

        last = solusi[length][pos1:]
        last.reverse()
        solusi[length][pos1:] = last[:]

        return True
    else:
        return False


def top(x):
    return x[len(x) - 1]


tc = input("Nama file testcase: ")
opsi = input("Lihat proses [y/n]: ")
util = CrosswordUtil()
a = util.read_json(tc)

start_time = time.time()
tts = a[0]
sol = a[1]
list_tts = []
list_tts.append(tts)
classSol = clasify_solusi(sol)
list_sol = []
list_sol.append(classSol)
allblocks = get_all_block(tts)

# print(classSol)
while not is_solved(top(list_sol)):
    level = get_min_class_idx(top(list_sol))

    curblocks = get_block_by_length(allblocks, len(top(list_sol)[level][0][1]))
    matchAll = True
    i = 0
    newtts = copy.deepcopy(top(list_tts))
    newsol = copy.deepcopy(top(list_sol))
    while i < len(curblocks) and matchAll:
        idxsol = get_idx_sol(
            newtts, newsol, level, curblocks[i][0], curblocks[i][1], curblocks[i][2]
        )
        if idxsol != -1:
            fill_tts(
                newtts,
                curblocks[i][0],
                curblocks[i][1],
                curblocks[i][2],
                newsol[level][idxsol][1],
            )
            del newsol[level][idxsol]
            i += 1
        else:
            matchAll = False
    if matchAll:
        del newsol[level]
        list_sol.append(newsol)
        list_tts.append(newtts)
    else:
        stillPermute = permutasi_solusi(top(list_sol), get_min_class_idx(top(list_sol)))
        while not stillPermute:
            spam1 = list_sol.pop()
            spam2 = list_tts.pop()
            stillPermute = permutasi_solusi(
                top(list_sol), get_min_class_idx(top(list_sol))
            )

    if opsi == "y":
        util.display(top(list_tts))
        print()
        if len(top(list_sol)) > 0:
            for i in range(len(top(list_sol))):
                print(top(list_sol)[i], end=" ")
            print()
            os.system("clear")
        os.system("clear")

exectime = time.time() - start_time
print()
util.display(top(list_tts))
print()
print("Crossword diselesaikan dalam %s seconds " % exectime)
