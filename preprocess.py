from collections import Counter
import os

class CircularRepeatPair(object):
    # initialize from a line in the index file
    def __init__(self, direct, line, id):
        # if direct, set to true
        # if inverted, set to false
        self.direct = direct

        # unique to each pair
        self.id = id

        # not set                       -1
        # doesn't have microhomology    0 or 1
        # satisfies microhomology       the length of microhomology (>= 2)
        self.microhomology = -1

        items = line[1:len(line) - 2].split(",")
        self.idx1 = int(items[0])
        self.idx2 = int(items[1])
        self.first_s1_len = int(items[2])
        self.first_s2_len = int(items[3])
        self.second_s1_len = int(items[4])
        self.second_s2_len = int(items[5])
        self.mismatch = float(items[6])
        self.s1_mismatch = float(items[7])
        self.s2_mismatch = float(items[8])


    def set_microhomology(self, s, overwrite=False):
        if self.microhomology == -1 or overwrite:
            # prefix of the 1st segment, and the substring following the 2nd segment
            count1 = 0
            for i in range(15):
                if s[self.idx1 + i] != s[self.idx1 + self.first_segment_length() + i]:
                    break
                count1 += 1

            # prefix of the 2nd segment, and the substring following the 1st segment
            count2 = 0
            for i in range(15):
                if s[self.idx2 + i] != s[self.idx2 + self.second_segment_length() + i]:
                    break
                count2 += 1

            self.microhomology = max(count1, count2)

    def satisfy_microhomology(self):
        return self.microhomology >= 2

    def first_segment_length(self):
        return self.first_s1_len + self.first_s2_len

    def second_segment_length(self):
        return self.second_s1_len + self.second_s2_len

    def get_segments(self):
        segment1 = CircularRepeatSegment(self.idx1, self.first_s1_len, self.first_s2_len, self.direct, False)
        segment2 = CircularRepeatSegment(self.idx2, self.second_s1_len, self.second_s2_len, self.direct, self.direct)
        return segment1, segment2

class CircularRepeatSegment(object):
    def __init__(self, idx, s1_len, s2_len, direct, s2_first):
        # is the segment s1s2 or s2s1
        # can only have s2s1 if it's the second segment in the directed pair
        self.s2_first = s2_first

        self.idx = idx
        self.s1_len = s1_len
        self.s2_len = s2_len
        self.direct = direct

        self.gc_content = -1.0

    def segment_length(self):
        return self.s1_len + self.s2_len

    def set_gc_content(self, s, overwrite=False):
        if self.gc_content == -1 or overwrite:
            counter = Counter(s[self.idx : self.idx + self.segment_length()])
            self.gc_content = (counter["C"] + counter["G"]) / self.segment_length()

def remove_duplicate_pairs(cr_pairs, favor_microhomology):
    # key: two starting indices of the pair segments
    # value: length of microhomology
    dic = {}
    for pair in cr_pairs:
        idx = (pair.idx1, pair.idx2)
        if not idx in dic or (favor_microhomology and dic[idx] < pair.microhomology):
            dic[idx] = pair.microhomology

    h_set = set()
    result = []
    for pair in cr_pairs:
        idx = (pair.idx1, pair.idx2)
        if not idx in h_set and idx in dic:
            result.append(pair)
            h_set.add(idx)

    return result

def remove_overlapping_pairs(cr_pairs, favor_microhomology, n):

    marked = [0]*n
    result = []

    def check_overlap_and_update_marked(pair):
        first_overlap = set(marked[pair.idx1: pair.idx1+pair.first_segment_length()])
        second_overlap = set(marked[pair.idx2: pair.idx2+pair.second_segment_length()])


        if len(first_overlap.intersection(second_overlap)) == 1: # only contain 0
            marked[pair.idx1] = pair.id
            marked[pair.idx1 + pair.first_segment_length()] = pair.id
            marked[pair.idx2] = pair.id
            marked[pair.idx2 + pair.second_segment_length()] = pair.id
            return False
        return True

    # when favor microhomo, we first add pairs that satisfies microhomo, then add others
    if favor_microhomology:
        for pair in cr_pairs:
            if pair.satisfy_microhomology():
                both_overlap = check_overlap_and_update_marked(pair)
                if not both_overlap:
                    result.append(pair)
        for pair in cr_pairs:
            if not pair.satisfy_microhomology():
                both_overlap = check_overlap_and_update_marked(pair)
                if not both_overlap:
                    result.append(pair)
        return result

    # when not favor microhomo
    for pair in cr_pairs:
        both_overlap = check_overlap_and_update_marked(pair)
        if not both_overlap:
            result.append(pair)
    return result



def remove_segments_overlap(segments, n):
    ressult = []
    marked = [0]*n
    for seg in segments:
        if sum(marked[seg.idx: seg.idx + seg.segment_length()]) == 0:
            for i in range(seg.idx, seg.idx + seg.segment_length()):
                marked[i] = 1
            ressult.append(seg)
    return ressult


def raw_pairs_from_file(file_path, is_direct, seq):
    file = open(file_path, "r")
    result = []
    for i, line in enumerate(file):
        # skip invalid lines
        if len(line) < 10:
            continue

        cr_pair = CircularRepeatPair(is_direct, line, i+1)
        cr_pair.set_microhomology(seq)
        result.append(cr_pair)
    return result

def raw_pairs_from_dir(dir, is_direct, seq):
    data_file_paths = [os.path.join(dir, f) for f in os.listdir(dir) if 
                       os.path.isfile(os.path.join(dir, f)) and f != '.DS_Store']
    result = []
    for file_path in data_file_paths:
        result = result + raw_pairs_from_file(file_path, is_direct, seq)
    return result

def cr_pairs_from_file(file_path, seq, is_direct, is_data_folder, remove_duplicates=True, remove_overlap=True,
        favor_microhomology=True):

    print_message = "Circular repeats index file: {}\n".format(file_path)

    if not is_data_folder:
        result = raw_pairs_from_file(file_path, is_direct, seq)
    else:
        result = raw_pairs_from_dir(file_path, is_direct, seq)

    print_message += "Number of circular repeated pairs found before any filtering: {}\n".format(len(result))

    if remove_duplicates:
        result = remove_duplicate_pairs(result, favor_microhomology)
        print_message += "Number of circular repeated pairs after duplication removal: {}\n".format(len(result))
    else:
        print_message += "No duplication removal\n"

    if remove_overlap:
        result = remove_overlapping_pairs(result, favor_microhomology, len(seq))
        print_message += "Number of circular repeated pairs after overlapping removal: {}\n".format(len(result))
    else:
        print_message += "No overlapping removal\n"
    
    microhomology_percentage = len([pair for pair in result if pair.satisfy_microhomology()]) / len(result)
    print_message += "Percentage of circular repeated pairs satisfying microhomology: {}\n".format(microhomology_percentage)

    meta_data = {"file_name": file_path,
                 "remove_duplicates": remove_duplicates,
                 "remove_overlap": remove_overlap,
                 "favor_microhomology": favor_microhomology,
                 "print_message": print_message}

    print(print_message)

    return result, meta_data

def cr_segments_from_pairs(pairs, seq, remove_overlap=True):

    result = []
    for pair in pairs:
        seg1, seg2 = pair.get_segments()
        seg1.set_gc_content(seq)
        seg2.set_gc_content(seq)
        result.append(seg1)
        result.append(seg2)

    print_message = "Number of circular repeat segments found before any filtering: {}\n".format(len(result))

    if remove_overlap:
        result = remove_segments_overlap(result, len(seq))
        print_message += "Number of circular repeat segments after overlapping removal: {}\n".format(len(result))
    else:
        print_message += "No overlapping removal\n"

    meta_data = {"remove_overlap": remove_overlap,
                 "print_message": print_message}

    print(print_message)

    return result, meta_data







