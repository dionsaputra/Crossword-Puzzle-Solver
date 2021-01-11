import json
import copy
import time
import os
from typing import List
from puzzle import Puzzle
from block import Block


class Crossword:
    def __init__(self, json_file: str):
        with open(json_file) as f:
            data = json.load(f)

        height = len(data["puzzle"])
        width = len(data["puzzle"][0])

        self.puzzle = Puzzle(height, width, list("".join(data["puzzle"])))
        self.words = data["words"]

    def classify_solution(self):
        longest_word = max(self.words, key=lambda word: len(word))
        result = [[] for x in range(len(longest_word) + 1)]

        for word in self.words:
            result[len(word)].append(word)

        i = 0
        while i < len(result):
            if len(result[i]) == 0:
                del result[i]
            else:
                i += 1
        return result

    def get_min_class_idx(self, csol):
        minim = len(csol[0])
        idx = 0
        for i in range(1, len(csol)):
            if len(csol[i]) < minim:
                idx = i
                minim = len(csol[i])
        return idx

    def get_idx_sol(self, tts, csol, level, block: Block):
        idx = 0
        found = False
        while idx < len(csol[level]) and not found:
            if tts.is_word_match(csol[level][idx], block):
                found = True
            else:
                idx += 1

        if found:
            return idx
        else:
            return -1

    def permutate_solution(self, solution, length):
        pos1 = len(solution[length]) - 1
        while pos1 > 0 and solution[length][pos1][0] < solution[length][pos1 - 1][0]:
            pos1 -= 1

        if pos1 > 0:
            pos2 = len(solution[length]) - 1
            while solution[length][pos2][0] < solution[length][pos1 - 1][0]:
                pos2 -= 1
            [solution[length][pos1 - 1], solution[length][pos2]] = [
                solution[length][pos2],
                solution[length][pos1 - 1],
            ]

            last = solution[length][pos1:]
            last.reverse()
            solution[length][pos1:] = last[:]

            return True
        else:
            return False

    def solve(self):
        start_time = time.time()
        list_tts = [self.puzzle]
        list_sol = [self.classify_solution()]

        while not len(list_sol[-1]) <= 0:
            level = self.get_min_class_idx(list_sol[-1])

            curblocks = self.puzzle.get_block(len(list_sol[-1][level][0]))

            matchAll = True
            i = 0
            newtts = copy.deepcopy(list_tts[-1])
            newsol = copy.deepcopy(list_sol[-1])
            while i < len(curblocks) and matchAll:
                idxsol = self.get_idx_sol(newtts, newsol, level, curblocks[i])
                if idxsol != -1:
                    newtts.fill(curblocks[i], newsol[level][idxsol])
                    del newsol[level][idxsol]
                    i += 1
                else:
                    matchAll = False
            if matchAll:
                del newsol[level]
                list_sol.append(newsol)
                list_tts.append(newtts)
            else:
                stillPermute = self.permutate_solution(
                    list_sol[-1], self.get_min_class_idx(list_sol[-1])
                )
                while not stillPermute:
                    list_sol.pop()
                    list_tts.pop()
                    stillPermute = self.permutate_solution(
                        list_sol[-1], self.get_min_class_idx(list_sol[-1])
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
        print("Crossword solved in %s seconds " % exectime)
