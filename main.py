from random import random
import time


class Trace:
    def __init__(self, v, p, i, j):
        self.i = i
        self.j = j
        self.value = v
        self.parent = p


def recursiveTimber(i, j, log):
    if i == j:
        return log[i]
    if i + 1 == j:
        return max(log[i], log[j])

    left = log[i] + min(recursiveTimber(i + 2, j, log), recursiveTimber(i + 1, j - 1, log))
    right = log[j] + min(recursiveTimber(i + 1, j - 1, log), recursiveTimber(i, j - 2, log))
    return max(left, right)


def dpTimber(log):
    log_size = len(log)
    tr_table = [[(Trace(None, None, None, None)) for _ in range(log_size)] for _ in range(log_size)]

    for x, segment in enumerate(log):
        j = x
        i = 0

        while j < log_size:
            if i == j:
                tr_table[i][j].value = log[i]
                tr_table[i][j] = Trace(log[i], None, i + 1, j + 1)
            elif i == j - 1:
                tr_table[i][j].value = curr_value = max(log[i], log[j])
                if log[i] >= log[j]:
                    parent = tr_table[i + 1][j]
                else:
                    parent = tr_table[i][j - 1]
                tr_table[i][j] = Trace(curr_value, parent, i + 1, j + 1)

            else:
                length_i = tr_table[i][j - (j - i)].value
                left_min = min(tr_table[i + 2][j].value, tr_table[i + 1][j - 1].value)
                length_j = tr_table[i + (j - i)][j].value
                right_min = min(tr_table[i + 1][j - 1].value, tr_table[i][j - 2].value)
                tr_table[i][j].value = curr_value = max(length_i + left_min, length_j + right_min)

                if length_i + left_min >= length_j + right_min:
                    if left_min == tr_table[i + 2][j].value:
                        parent = tr_table[i + 1][j]
                    else:
                        if tr_table[i + 1][j].value <= tr_table[i][j - 1].value:
                            parent = tr_table[i + 1][j]
                        else:
                            parent = tr_table[i][j - 1]

                else:
                    if right_min == tr_table[i][j - 2].value:
                        parent = tr_table[i][j - 1]
                    else:
                        if tr_table[i + 1][j].value <= tr_table[i][j - 1].value:
                            parent = tr_table[i + 1][j]
                        else:
                            parent = tr_table[i][j - 1]

                tr_table[i][j] = Trace(curr_value, parent, i + 1, j + 1)
            i += 1
            j += 1

    printTable(tr_table, log_size)
    printTraceback(tr_table[0][log_size - 1], tr_table[0][log_size - 1])
    return tr_table[0][log_size - 1].value, tr_table


def printTraceback(curr, length):
    print(length.value)
    while curr.parent is not None:
        if curr.i == curr.parent.i:
            print(curr.j, end="")
        else:
            print(curr.i, end="")
        print(" ", end="")
        curr = curr.parent
    print(curr.i)


def growTrees(max_size):
    log = []
    for _ in range(max_size):
        log.append(int(random() * 100))
    return log


def printTable(table, size):
    for i in range(size):
        for j in range(size):
            entry = table[i][j].value
            if not entry:
                entry = 0
            print("{:3d}".format(entry) + " ", end="")
        print()


if __name__ == '__main__':
    recursive_log = [33, 28, 35, 25, 29, 34, 28, 32]
    traceback_log = [33, 28, 35, 23, 23, 25, 37, 40, 42, 24, 38, 29, 22, 40, 36, 42, 39, 37, 45, 32]
    brian = [5, 3, 6, 6, 4, 7]
    log_to_split = growTrees(18)
    total = 0

    for _ in range(3):
        start = time.perf_counter()
        # answer = recursiveTimber(0, len(recursive_log) - 1, recursive_log)
        # answer = recursiveTimber(0, len(log_to_split) - 1, log_to_split)
        # answer, dp_traceback = dpTimber(log_to_split)
        answer, dp_traceback = dpTimber(brian)
        end = time.perf_counter()
        run_time = end - start
        total += run_time
    # print(total/3)
