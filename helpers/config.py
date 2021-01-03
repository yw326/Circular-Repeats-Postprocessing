import argparse


def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--seq_path', type=str, help="the path to the DNA sequence file")
    parser.add_argument('--data_path', type=str, help="the path to the circular repeated pairs data")
    parser.add_argument('--output_path', type=str, help="output path")

    parser.add_argument('--is_data_file', default=False, action="store_true",
                        help="use this if data_path is a file rather than a folder")
    parser.add_argument('--is_inverted', default=False, action="store_true",
                        help="use this for inverted circular repeats")

    parser.add_argument('--no_remove_pair_dup', default=False, action="store_true")
    parser.add_argument('--no_remove_pair_overlap', default=False, action="store_true")
    parser.add_argument('--no_faver_microhomology', default=False, action="store_true")
    parser.add_argument('--no_remove_segments_overlap', default=False, action="store_true")

    return parser
