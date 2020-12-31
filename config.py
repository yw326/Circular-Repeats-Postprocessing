import argparse


def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--seq_path', type=str, help="the path to the DNA sequence file")
    parser.add_argument('--data_path', type=str, help="the path to the circular repeated pairs data")
    parser.add_argument('--is_data_folder', type=bool, help="true if data_path is a folder of data files")
    parser.add_argument('--output_path', type=str, help="output path")
    parser.add_argument('--is_direct', type=bool, help="true if it is direct circular repeats")

    parser.add_argument('--remove_pair_dup', type=bool, default=True)
    parser.add_argument('--remove_pair_overlap', type=bool, default=True)
    parser.add_argument('--faver_microhomology', type=bool, default=True)
    parser.add_argument('--remove_segments_overlap', type=bool, default=True)

    return parser
