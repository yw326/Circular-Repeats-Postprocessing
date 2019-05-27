from helpers.file_helper import first_index, second_index, first_s1_len, first_s2_len, second_s1_len, second_s2_len, \
    mismatch_ratio, length
from helpers.seq_helper import get_seq_GC_content
import matplotlib.pyplot as plt
import numpy as np
from CircleRepeat.CircleRepeat import CircleRepeatPair

# obtain a list of CircleRepeatPair objects from the index file
def setup_circle_repeats_from_index_file(sequence, index_file_name):
    index_file = open(index_file_name, "r")
    result = list()

    for i, line in enumerate(index_file):
        first_idx = first_index(line)
        second_idx = second_index(line)
        first_s1_length = first_s1_len(line)
        first_s2_length = first_s2_len(line)
        second_s1_length = second_s1_len(line)
        second_s2_length = second_s2_len(line)
        mismatch_ratio_val = mismatch_ratio(line)
        repeat_length = length(line)

        first_sec = sequence[first_idx: first_idx + repeat_length]
        second_sec = sequence[second_idx: second_idx + repeat_length]

        GC = (get_seq_GC_content(first_sec) + get_seq_GC_content(second_sec)) / 2

        circle_repeat = CircleRepeatPair(i + 1, first_sec, second_sec, first_idx, second_idx, first_s1_length,
                                         first_s2_length, second_s1_length, second_s2_length, mismatch_ratio_val, repeat_length, GC)
        result.append(circle_repeat)

    return filter_repeats_pairs(result)

# remove duplicates
def filter_repeats_pairs(repeats):
    result = list()
    for pair in repeats:
        in_result = False
        for recorded_pair in result:
            if (recorded_pair.first_index == pair.first_index and recorded_pair.second_index == pair.second_index):
                in_result = True
        if (not in_result):
            result.append(pair)
    return result

# only get circle repeats with length smaller than threshold
def get_pairs_len_smaller_than(repeats, threshold):
    result = list()
    for p in repeats:
        if p.length < threshold:
            result.append(p)
    return result


def averge_GC_content(repeats):
    total = 0.0
    total_len = 0.0
    for repeat in repeats:
        for chr in repeat.first_section:
            total_len += 1
            if (chr == 'G' or chr == 'C'):
                total += 1
        for chr in repeat.second_section:
            total_len += 1
            if (chr == 'G' or chr == 'C'):
                total += 1

    return total / total_len

def plot_distr(repeats):
    print("plotting length and GC distribution")
    l1 = list()
    l2 = list()
    l3 = list()
    for circle_pair in repeats:
        l1.append(circle_pair.length)
        l2.append(circle_pair.GC_content)
        if (not circle_pair.first_index in l3):
            l3.append(circle_pair.first_index)
        if (not circle_pair.second_index in l3):
            l3.append(circle_pair.second_index)

    print("microDNA count: ", len(l3))

    binwidth1 = 10
    f1 = plt.figure(1)
    plt.hist(l1, bins=range(0, 800 + binwidth1, binwidth1))
    f1.show()

    bin_size = 0.01
    min_edge = 0.3
    max_edge = 0.7
    N = (max_edge - min_edge) / bin_size
    Nplus1 = N + 1
    bin_list = np.linspace(min_edge, max_edge, Nplus1)
    f2 = plt.figure(2)
    plt.hist(l2, bins=bin_list)
    f2.show()

    f3 = plt.figure(3)
    plt.hist(l3, bins=range(0, 40000000, 10000))
    f3.show()

    input()

def check_microhomo(repeats, str):
    result = list()
    for repeat_pair in repeats:
        count1 = 0
        for i in range(15):
            if (str[repeat_pair.first_index + repeat_pair.length + i] == repeat_pair.first_section[i]):
                count1 += 1
            else:
                break
        count2 = 0
        for i in range(15):
            if (str[repeat_pair.second_index + repeat_pair.length + i] == repeat_pair.second_section[i]):
                count2 += 1
            else:
                break

        if (count1 or count2 >= 2):
            result.append(repeat_pair)

    print("Number of pairs with at least 1 microhomo is", len(result))
    print("Or", len(result)/len(repeats))