from utils import get_seq_from_file
from preprocess import cr_pairs_from_file, cr_segments_from_pairs
from save import save_result
from load import is_task_performed, load_and_print_summary
from config import get_arguments

# e.g. python main.py --seq_path data/chr21_prefiltered.mask --data_path data/chr21_direct_index_40_20.txt --output_path output --is_direct true --is_data_folder false
# e.g. python main.py --seq_path data/chr21_prefiltered.mask --data_path data/chr21_direct_idx --output_path output --is_direct true --is_data_folder true


if __name__ == '__main__':
    parser = get_arguments()
    args = parser.parse_args()

    data_file_path = args.data_path
    output_path = args.output_path
    seq_path = args.seq_path
    is_direct = args.is_direct
    is_data_folder = args.is_data_folder

    if is_task_performed(output_path):
        print("The task has already been performed\n")
        load_and_print_summary(output_path)
    else:
        seq, seq_info = get_seq_from_file(seq_path)
        pairs, pairs_info= cr_pairs_from_file(data_file_path, seq, is_direct, is_data_folder)
        segments, segs_info = cr_segments_from_pairs(pairs, seq)

        save_result(output_path, pairs, segments, pairs_info, segs_info, seq_info)

