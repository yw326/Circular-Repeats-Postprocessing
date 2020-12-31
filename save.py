import matplotlib.pyplot as plt
import pickle
import os

def save_cr_pairs_info(output_dir, pairs, pairs_info, seq_info):
    output_dir = os.path.join(output_dir, "pairs")
    os.mkdir(output_dir)
    csv_path = os.path.join(output_dir, "circular repeated pairs.csv")
    with open(csv_path, "wb") as csv_file:
        csv_file.write(" , direct or inverted, segment 1 starting index, segment 2 starting index, first s1 length, first s2 length, second s1 length, second s2 length, mismatch, s1 mismatch, s2 mismatch, microhomology\n".encode())
        for i, pair in enumerate(pairs):
            direct = "direct" if pair.direct else "inverted"
            line = ",".join([str(i+1), direct, str(pair.idx1), str(pair.idx2), str(pair.first_s1_len), str(pair.first_s2_len),
                             str(pair.second_s1_len), str(pair.second_s2_len), str(pair.mismatch), str(pair.s1_mismatch),
                             str(pair.s2_mismatch), str(pair.microhomology)]) + "\n"
            csv_file.write(line.encode())

    microhomology_data = [pair.microhomology for pair in pairs]
    microhomology_plot_path = os.path.join(output_dir, "microhomology length distribution.png")
    bins = [i for i in range(16)]
    plt.hist(microhomology_data, bins=bins)
    plt.title("microhomology length distribution")
    plt.savefig(microhomology_plot_path)
    plt.close()

    summary = {"seq_info": seq_info, "pairs_info": pairs_info}
    summary_path = os.path.join(output_dir, "summary.pickle")
    pickle.dump(summary, open(summary_path, "wb"))

def save_cr_segments_info(output_dir, segments, segments_info, seq_info):
    output_dir = os.path.join(output_dir, "segments")
    os.mkdir(output_dir)
    csv_path = os.path.join(output_dir, "circular repeated segments.csv")

    with open(csv_path, "wb") as csv_file:
        csv_file.write(" , direct or inverted, starting index, s1 length, s2 length, GC content\n".encode())
        for i, seg in enumerate(segments):
            direct = "direct" if seg.direct else "inverted"
            line = ",".join([str(i+1), direct, str(seg.idx), str(seg.s1_len), str(seg.s2_len), str(seg.gc_content)]) + "\n"
            csv_file.write(line.encode())

        f1 = plt.figure(1)
        gc_data = [seg.gc_content for seg in segments]
        gc_plot_path = os.path.join(output_dir, "GC content distribution.png")
        plt.hist(gc_data, bins=[i * 0.02 for i in range(50)])
        plt.title("GC content distribution")
        f1.savefig(gc_plot_path)
        plt.close()

        f2 = plt.figure(2)
        length_data = [seg.segment_length() for seg in segments]
        length_plot_path = os.path.join(output_dir, "length distribution.png")
        plt.hist(length_data, bins=[i * 20 for i in range(120)])
        plt.title("length distribution")
        f2.savefig(length_plot_path)
        plt.close()

        summary = {"seq_info": seq_info, "segments_info": segments_info}
        summary_path = os.path.join(output_dir, "summary.pickle")
        pickle.dump(summary, open(summary_path, "wb"))

def save_result(output_dir, pairs, segments, pairs_info, segments_info, seq_info):
    os.mkdir(output_dir)
    save_cr_pairs_info(output_dir, pairs, pairs_info, seq_info)
    save_cr_segments_info(output_dir, segments, segments_info, seq_info)
