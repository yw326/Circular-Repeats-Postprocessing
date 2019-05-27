from helpers.file_helper import get_seq_from_file
from Simulation.simulation import check_simulated_results
import sys, getopt
import pickle

myopts, args = getopt.getopt(sys.argv[1:],"",["seq_file=", "ground_truth_file=", "found_file_name=", "off_allowed="])
# if (len(myopts) < 4 or len(args) < 4):
#     print("Not enough arguments or options: 4 required")

for o, a in myopts:
    if o == "--seq_file":
        output_seq_file_name = a
    elif o == "--ground_truth_file":
        crepeats_ground_truth_file_name = a
    elif o == "--found_file_name":
        crepeats_found_file_name = a
    elif o == "--off_allowed":
        off_allowed_ratio = float(a)
    else:
        print("unhandled option")

seq = get_seq_from_file(output_seq_file_name)
circle_repeats = pickle.load(open(crepeats_ground_truth_file_name, "rb"))
check_simulated_results(seq=seq, index_file_name=crepeats_found_file_name, actual_circle_repeats=circle_repeats,
                            off_allowed_ratio=off_allowed_ratio)