import numpy as np
import matplotlib.pyplot as plt
import pickle
import sys
from pathlib import Path


class CircleRepeat(object):
    seq_num = -1                # sequence number
    first_section = ""          # str of first section circle repeat
    first_index = -1            # starting index of first section
    second_index = -1           # starting index of section section
    maximal_section_len = 0     # length of maximal part
    microhomology_len_1st = 0   # len of str after 1st section that is same as the prefix
    microhomology_len_2nd = 0   # len of str after 2nd section that is same as the prefix

    def __init__(self, seq_num, first_section, first_index, second_index, maximal_section_len, microhomology_len_1st, microhomology_len_2nd):
        self.seq_num = seq_num
        self.first_section = first_section
        self.first_index = first_index
        self.second_index = second_index
        self.maximal_section_len = maximal_section_len
        self.microhomology_len_1st = microhomology_len_1st
        self.microhomology_len_2nd = microhomology_len_2nd


def is_repeat_line(line):
    return line[0]==">" and ("-" not in line)

def seq_num_from_line(line):
    return line[4:len(line)]

def parse_line_from_index_file(line):
    l = list()
    i = 1

    while(line[i] != ","):
        i += 1
    l.append(line[1:i])

    j = i + 1
    while (line[j] != ","):
        j += 1
    l.append(line[i+1:j])

    k = j + 1
    while (line[k] != ","):
        k += 1
    l.append(line[j+1:k])

    x = k + 1
    while (line[x] != ")"):
        x += 1
    l.append(line[k + 1:x])

    return l

def first_index(line):
    return int(parse_line_from_index_file(line)[0])

def second_index(line):
    return int(parse_line_from_index_file(line)[1])

def total_repeat_len(line):
    return int(parse_line_from_index_file(line)[2])

def maximal_repeat_len(line):
    return int(parse_line_from_index_file(line)[3])

def len_for_microhomo(start, len, str, max_checklen):
    count = 0
    for i in range(max_checklen):
        if (str[start+i]==str[start+len+i]):
            count += 1
        else:
            return count
    return count

def len_for_microhomo(start, length, str, max_checklen):
    count = 0
    for i in range(max_checklen):
        if (start+i+length >= len(str)):
            return count
        if (str[start+i]==str[start+length+i]):
            count += 1
        else:
            return count
    return count

def get_circle_repeats_from_file(filtered_file_name, index_file_name, s, s_masked, tandem_threshold):

    filter_file = open(filtered_file_name, "r")
    index_file = open(index_file_name, "r")
    seq_nums = list()
    seq_sections = list()
    result = list()

    # temp var used for get str
    temp = 0
    temp_set = False
    for i, line in enumerate(filter_file):

        if (is_repeat_line(line)):
            seq_nums.append(int(seq_num_from_line(line))-1)
            temp = i + 1
            temp_set = True

        if (temp_set and i == temp):
            temp_set = False
            seq_sections.append(line[:len(line)-1])


    count = 0
    for i, line in enumerate(index_file):
        if (i in seq_nums):

            first_microhomo = len_for_microhomo(first_index(line), total_repeat_len(line), s, 15)
            second_microhomo = len_for_microhomo(second_index(line), total_repeat_len(line), s, 15)

            circle_repeat = CircleRepeat(i+1, seq_sections[count], first_index(line), second_index(line),
                                               maximal_repeat_len(line), first_microhomo, second_microhomo)
            result.append(circle_repeat)
            count += 1

    a = list()
    for i in range(len(result)):
        fst_idx = result[i].first_index
        if percentage_tandem(s_masked[fst_idx : fst_idx+len(result[i].first_section)]) < tandem_threshold:
            a.append(result[i])
    return a

def percentage_tandem(str):
    count = 0
    for c in str:
        if c == "N":
            count += 1
    return count / len(str)


def get_seq_from_file(seq_file_name):
    s = ""
    file = open(seq_file_name, "r")
    for line in file:
        for ch in line:
            if (ch == "A" or ch == "T" or ch == "C" or ch == "G"):
                s = s + ch
    return s

def get_masked_seq_from_file(seq_file_name):
    s = ""
    file = open(seq_file_name, "r")
    for line in file:
        for ch in line:
            if (ch == "A" or ch == "T" or ch == "C" or ch == "G" or ch == "N"):
                s = s + ch
    return s

def get_GC_content(seq):
    count = 0.0
    for chr in seq:
        if (chr == "G" or chr == "C"):
            count += 1
    return count / len(seq)

def averge_GC_content(repeats):
    total = 0.0
    total_len = 0.0
    for repeat in repeats:
        for chr in repeat.first_section:
            total_len += 1
            if (chr == 'G' or chr == 'C'):
                total += 1

    return total / total_len

def nonzero_first_microhomo(repeats):
    count = 0
    for repeat in repeats:
        if (repeat.microhomology_len_1st > 1):
            count += 1
    return count / len(repeats)

def nonzero_second_microhomo(repeats):
    count = 0
    for repeat in repeats:
        if (repeat.microhomology_len_2nd > 1):
            count += 1
    return count / len(repeats)

def plot_repeats_len_distr(type1_repeats, type2_repeats):
    l1 = list()
    l2 = list()
    for repeat in type1_repeats:
        l1.append(len(repeat.first_section))
    for repeat in type2_repeats:
        l2.append(len(repeat.first_section))

    l = l1 + l2

    f1 = plt.figure(1)
    plt.hist(l1)
    f1.show()

    f2 = plt.figure(2)
    plt.hist(l2)
    f2.show()

    f3 = plt.figure(3)
    plt.hist(l)
    f3.show()

    #plt.show()

    input()

def print_results_both(file_path, seq_name, masked_seq_name, tandem_threshold):
    s = get_seq_from_file(file_path + seq_name)
    s_masked = get_masked_seq_from_file(file_path+masked_seq_name)

    type1_circle_repeats = get_circle_repeats_from_file(file_path + "1st-type cr seq",
                                                        file_path + "1st-type_circle_repeat", s, s_masked, tandem_threshold)
    type2_circle_repeats = get_circle_repeats_from_file(file_path + "2nd-type cr seq",
                                                        file_path + "2nd-type circle repeat", s, s_masked, tandem_threshold)

    print(len(type1_circle_repeats))
    print(len(type2_circle_repeats))

    print("averge GC content for 1st-type repeat: ", averge_GC_content(type1_circle_repeats))
    print("percentage of non-zero microhomology first part for 1st-type repeat",
          nonzero_first_microhomo(type1_circle_repeats))
    print("percentage of non-zero microhomology second part for 1st-type repeat",
          nonzero_second_microhomo(type1_circle_repeats))

    print("averge GC content for 2nd-type repeat: ", averge_GC_content(type2_circle_repeats))
    print("percentage of non-zero microhomology first part for 2nd-type repeat",
          nonzero_first_microhomo(type2_circle_repeats))
    print("percentage of non-zero microhomology second part for 2nd-type repeat",
          nonzero_second_microhomo(type2_circle_repeats))
    plot_repeats_len_distr(type1_circle_repeats, type2_circle_repeats)
    # path_prefix = "data/" + chr_num + "/"
    # s = get_seq_from_file(path_prefix + seq_name)
    # s_masked = get_masked_seq_from_file(path_prefix + masked_seq)
    #
    # type1_circle_repeats = get_circle_repeats_from_file(path_prefix + "1st-type cr seq",
    #                                                     path_prefix + "1st-type_circle_repeat", s, s_masked,
    #                                                     tandem_threshold)
    # type2_circle_repeats = get_circle_repeats_from_file(path_prefix + "2nd-type cr seq",
    #                                                     path_prefix + "2nd-type circle repeat", s, s_masked,
    #                                                     tandem_threshold)
    #
    # return len(type1_circle_repeats), len(type2_circle_repeats)

def write_seq_file_from_circle_repeats(output_file_name, circle_repeats):
    count = 1
    f = open(output_file_name, "w")

    for c in circle_repeats:
        f.write(">seq" + str(count) + "\n")
        f.write(c.first_section)
        f.write("\n")
        count += 1
    f.close()

def write_idx_file_from_circle_repeats(output_file_name, circle_repeats):
    f = open(output_file_name, "w")

    for c in circle_repeats:
        f.write("(" + str(c.first_index) + "," + str(c.second_index) + "," + str(len(c.first_section)) + "," + str(c.maximal_section_len) + ")\n")
    f.close()


def print_results(seq_name, masked_seq_name, tandem_threshold, seq_circle_rep, idx_circle_rep,
                  output_seq_file, output_idx_file):
    s = get_seq_from_file(seq_name)
    s_masked = get_masked_seq_from_file(masked_seq_name)

    circle_repeats = get_circle_repeats_from_file(seq_circle_rep, idx_circle_rep,
                                                  s, s_masked, tandem_threshold)
    print("number of circle repeat found after filtering out tandem repeats", len(circle_repeats))

    print("averge GC content: ", averge_GC_content(circle_repeats))
    print("percentage of non-zero microhomology first part", nonzero_first_microhomo(circle_repeats))
    print("percentage of non-zero microhomology second part", nonzero_second_microhomo(circle_repeats))
    
    write_seq_file_from_circle_repeats(output_seq_file, circle_repeats)
    write_idx_file_from_circle_repeats(output_idx_file, circle_repeats)

    l = list()
    for repeat in circle_repeats:
        l.append(len(repeat.first_section))
    plt.hist(l)
    plt.show()


# tandem_threshold = 0.3
# file_path = "data/chrY/"
# seq_name = file_path+"chrY_prefiltered.txt"
# masked_seq = file_path+"chrY_prefiltered.mask"
# seq_circle_rep = file_path + "1st-type cr seq"
# idx_circle_rep = file_path + "1st-type_circle_repeat"
# output_seq_file = file_path + "output_seq_file.txt"
# output_idx_file = file_path + "output_idx_file.txt"
#
# print_results(seq_name, masked_seq, tandem_threshold, seq_circle_rep, idx_circle_rep,
#               output_seq_file, output_idx_file)

def main():
    args = sys.argv
    if len(args) < 8:
        print("Error: not enough arguments given (need 7)")
        return

    try:
        seq_file = open(args[1], 'r')
    except FileNotFoundError:
        print("Error: invalid sequence file name")
        return

    try:
        masked_seq_file = open(args[2], 'r')
    except FileNotFoundError:
        print("Error: invalid masked sequence file name")
        return

    tandem_threshold = float(args[3])
    if (tandem_threshold > 1 or tandem_threshold < 0):
        print("Error: invalid tandem threshold")
        return

    try:
        seq_circle_rep = open(args[4], 'r')
    except FileNotFoundError:
        print("Error: invalid circle repeats sequence file name")
        return

    try:
        idx_circle_rep = open(args[5], 'r')
    except FileNotFoundError:
        print("Error: invalid circle repeats index file name")
        return

    print_results(args[1], args[2], tandem_threshold, args[4], args[5],
                  args[6], args[7])


if __name__ == "__main__":
   main()