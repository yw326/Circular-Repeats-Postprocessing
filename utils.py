
def get_seq_from_file(seq_file_name):
    s = ""
    file = open(seq_file_name, "r")
    for line in file:
        for ch in line:
            if (ch == "A" or ch == "T" or ch == "C" or ch == "G"):
                s = s + ch

    print_message = "sequence file name: {}\n".format(seq_file_name)
    print_message += "sequence length {} \n".format(len(s))

    print(print_message)

    return s, {"seq_file": seq_file_name, "length": len(s), "print_message": print_message}

