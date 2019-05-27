def get_seq_GC_content(seq):
    count = 0.0
    for chr in seq:
        if (chr == "G" or chr == "C"):
            count += 1
    return count / len(seq)