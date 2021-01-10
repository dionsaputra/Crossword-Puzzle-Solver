import sys
import copy
import os
import time
from crossword import Crossword
from crossword import Block


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


def get_idx_sol(tts, csol, level, block: Block):
    idx = 0
    found = False
    while idx < len(csol[level]) and not found:
        if tts.is_word_match(csol[level][idx][1], block):
            found = True
        else:
            idx += 1

    if found:
        return idx
    else:
        return -1


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
    crossword = Crossword.read_json("./assets/example.crossword.json")

    start_time = time.time()
    list_tts = []
    list_tts.append(crossword.puzzle)
    classSol = clasify_solusi(crossword.words)
    list_sol = []
    list_sol.append(classSol)

    # print(classSol)
    while not len(list_sol[-1]) <= 0:
        level = get_min_class_idx(list_sol[-1])

        curblocks = crossword.puzzle.get_block(len(list_sol[-1][level][0][1]))
        matchAll = True
        i = 0
        newtts = copy.deepcopy(list_tts[-1])
        newsol = copy.deepcopy(list_sol[-1])
        while i < len(curblocks) and matchAll:
            idxsol = get_idx_sol(newtts, newsol, level, curblocks[i])
            if idxsol != -1:
                newtts.fill(curblocks[i], newsol[level][idxsol][1])
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

        list_tts[-1].display()
        print()
        if len(list_sol[-1]) > 0:
            for i in range(len(list_sol[-1])):
                print(list_sol[-1][i], end=" ")
            print()
            os.system("clear")
        os.system("clear")

    exectime = time.time() - start_time
    print()
    list_tts[-1].display()
    print()
    print("Crossword diselesaikan dalam %s seconds " % exectime)