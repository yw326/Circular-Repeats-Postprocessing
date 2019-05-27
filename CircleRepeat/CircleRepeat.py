class CircleRepeatPair(object):
    seq_num = -1                # sequence number
    first_section = ""          # str of first section circle repeat pair
    second_section = ""         # str of second section circle repeat pair
    first_index = -1            # starting index of first section
    second_index = -1           # starting index of section section

    first_s1_len = -1
    first_s2_len = -1
    second_s1_len = -1
    second_s2_len = -1
    mismatch_ratio = -1
    length = -1

    GC_content = -1

    def __init__(self, seq_num, first_section, second_section, first_index, second_index, first_s1_len,
                 first_s2_len, second_s1_len, second_s2_len, mismatch_ratio,length, GC):
        self.seq_num = seq_num
        self.first_section = first_section
        self.second_section = second_section
        self.first_index = first_index
        self.second_index = second_index
        self.first_s1_len = first_s1_len
        self.first_s2_len = first_s2_len
        self.second_s1_len = second_s1_len
        self.second_s2_len = second_s2_len
        self.mismatch_ratio = mismatch_ratio
        self.length = length
        self.GC_content = GC




