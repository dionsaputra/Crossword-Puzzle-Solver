import sys
import copy
import os
import time
from crossword.crossword import Crossword


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


def is_str_match(tts, string, head, length, datar):
    if length == len(string):
        match = True
        i = 0
        c1 = "-"
        if datar:
            while i < length and match:
                if (
                    tts.getAt(head[0], head[1] + i) == c1
                    or tts.getAt(head[0], head[1] + i) == string[i]
                ):
                    i += 1
                else:
                    match = False
        else:
            while i < length and match:
                if (
                    tts.getAt(head[0] + i, head[1]) == c1
                    or tts.getAt(head[0] + i, head[1]) == string[i]
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
            tts.setAt(head[0], head[1] + i, string[i])

    else:
        for i in range(length):
            tts.setAt(head[0] + i, head[1], string[i])


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


if __name__ == "__main__":
    # tc = input("Nama file testcase: ")
    tc = "./assets/example.crossword.json"
    # opsi = input("Lihat proses [y/n]: ")
    opsi = "y"
    crossword = Crossword.read_json(tc)

    start_time = time.time()
    list_tts = []
    list_tts.append(crossword.puzzle)
    classSol = clasify_solusi(crossword.words)
    list_sol = []
    list_sol.append(classSol)
    allblocks = crossword.get_blocks()

    # print(classSol)
    while not len(list_sol[-1]) <= 0:
        level = get_min_class_idx(list_sol[-1])

        curblocks = crossword.get_block(len(list_sol[-1][level][0][1]))
        matchAll = True
        i = 0
        newtts = copy.deepcopy(list_tts[-1])
        newsol = copy.deepcopy(list_sol[-1])
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
            stillPermute = permutasi_solusi(
                list_sol[-1], get_min_class_idx(list_sol[-1])
            )
            while not stillPermute:
                spam1 = list_sol.pop()
                spam2 = list_tts.pop()
                stillPermute = permutasi_solusi(
                    list_sol[-1], get_min_class_idx(list_sol[-1])
                )

        if opsi == "y":
            Crossword.display(list_tts[-1])
            print()
            if len(list_sol[-1]) > 0:
                for i in range(len(list_sol[-1])):
                    print(list_sol[-1][i], end=" ")
                print()
                os.system("clear")
            os.system("clear")

    exectime = time.time() - start_time
    print()
    Crossword.display(list_tts[-1])
    print()
    print("Crossword diselesaikan dalam %s seconds " % exectime)
