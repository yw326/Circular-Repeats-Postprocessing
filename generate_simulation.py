from Simulation.simulation import insert_circle_repeats, add_mutation, get_rand_seq
import sys, getopt
import pickle

myopts, args = getopt.getopt(sys.argv[1:],"",["seqlen=", "num_crepeats=", "min=", "max=", "maxitr=", "num_mutations=",
                                              "output_seq_file=", "output_crepeats_file=", "reversed_compl"])

max_len = 1000
max_itr = 1000

rc = False
for o, a in myopts:
    if o == '--seqlen':
        seq_len = int(a)
    elif o == '--num_crepeats':
        num_crepeats = int(a)
    elif o == "--min":
        min_len = int(a)
    elif o == "--max":
        max_len == int(a)
    elif o == "--maxitr":
        max_itr = int(a)
    elif o == "--num_mutations":
        num_mutation = int(a)
    elif o == "--output_seq_file":
        output_seq_file_name = a
    elif o == "--output_crepeats_file":
        output_crepeats_file_name = a
    elif o == "--reversed_compl":
        rc = True
    else:
        print("unhandled option")

seq = get_rand_seq(seq_len)
seq, circle_repeats, success_count = insert_circle_repeats(num_crepeats=num_crepeats, seq=seq, min_s_len=min_len, max_s_len=max_len,
                                            reversed_complement=rc, max_itr=max_itr)
print("Total of", success_count, "inserted")
seq, circle_repeats = add_mutation(num_mutation, seq, circle_repeats)
seq_file = open(output_seq_file_name, "w")
seq_file.write(seq)
seq_file.close()
pickle.dump(circle_repeats, open(output_crepeats_file_name, "wb"))

