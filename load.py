import pickle
import os

def is_task_performed(output_dir):
    return os.path.exists(output_dir)

def load_and_print_summary(output_dir):
    

    pairs_summary_path = os.path.join(output_dir, "pairs", "summary.pickle")
    segments_summary_path = os.path.join(output_dir, "segments", "summary.pickle")
    pairs_summary = pickle.load(open(pairs_summary_path, "rb"))
    segments_summary = pickle.load(open(segments_summary_path, "rb"))

    seq_message = pairs_summary["seq_info"]["print_message"]
    pairs_message = pairs_summary["pairs_info"]["print_message"]
    segments_message = segments_summary["segments_info"]["print_message"]

    print(seq_message)
    print(pairs_message)
    print(segments_message)
    

