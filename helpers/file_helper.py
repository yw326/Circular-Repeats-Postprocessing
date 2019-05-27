def get_seq_from_file(seq_file_name):
    s = ""
    file = open(seq_file_name, "r")
    for line in file:
        for ch in line:
            if (ch == "A" or ch == "T" or ch == "C" or ch == "G"):
                s = s + ch
    return s

def parse_line_from_index_file(line):
    return line[1:len(line)-2].split(",")

def first_index(line):
    return int(parse_line_from_index_file(line)[0])

def second_index(line):
    return int(parse_line_from_index_file(line)[1])

def first_s1_len(line):
    return int(parse_line_from_index_file(line)[2])

def first_s2_len(line):
    return int(parse_line_from_index_file(line)[3])

def second_s1_len(line):
    return int(parse_line_from_index_file(line)[4])

def second_s2_len(line):
    return int(parse_line_from_index_file(line)[5])

def mismatch_ratio(line):
    return float(parse_line_from_index_file(line)[6])

def length(line):
    return int(parse_line_from_index_file(line)[7])



