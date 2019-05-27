from CircleRepeat.circle_repeats_setup import setup_circle_repeats_from_index_file, plot_distr, averge_GC_content, check_microhomo, get_pairs_len_smaller_than
from helpers.file_helper import get_seq_from_file



sequence = get_seq_from_file("data/chrY_prefiltered.mask")
print("sequence length", len(sequence))
index_file_name = "data/chrY_index.txt"
circle_repeat_pairs = setup_circle_repeats_from_index_file(sequence, index_file_name)

print("Number of repeat pair found", len(circle_repeat_pairs))
print("Average GC content: ", averge_GC_content(circle_repeat_pairs))
check_microhomo(circle_repeat_pairs, sequence)
plot_distr(circle_repeat_pairs)

