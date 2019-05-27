import random
import string
import pickle

def get_rand_seq(length):
    my_letters='ATCG'
    return ''.join((random.choice(my_letters) for i in range(length)))

def is_valid_insertion(pos, currlist):
    if (len(currlist) == 0):
        return True
    for circle_repeat in currlist:
        length = circle_repeat[2]
        if ( (pos >= circle_repeat[0] and pos <= circle_repeat[0]+ length)):
            return False
        if ( (pos >= circle_repeat[1] and pos <= circle_repeat[1]+ length)):
            return False
    return True

def insert(source_str, insert_str, pos):
    return source_str[:pos]+insert_str+source_str[pos:]

def get_reverse_complement(str):
    s_c = ""
    for c in str:
        if (c == "A"):
            s_c += "T"
        elif (c == "T"):
            s_c += "A"
        elif (c == "C"):
            s_c += "G"
        elif (c == "G"):
            s_c += "C"
    return s_c[::-1]

# each element in the list contain (first start, second start, len)
# insertion of s1s2 or s2s1 will not perform if it's overlapping with existing circle repeats
# max_itr is the max number of attempts to insert
# if reversed_complement set to True, then ...s1s2...s1's2'... (s' is reversed complement of s) will be inserted
def insert_circle_repeat(curr_seq, curr_list, min_s_len, max_s_len, reversed_complement, max_itr=1000):
    # sample the length of s1 and s2
    s1_len = random.randrange(min_s_len,max_s_len)
    s2_len = random.randrange(min_s_len,max_s_len)

    # based on the length, generate random string s1 and s2
    s1 = get_rand_seq(s1_len)
    s2 = get_rand_seq(s2_len)
    s1s2 = s1+s2
    length = len(s1s2)

    if (reversed_complement):
        # if insert reversed complement circle repeat, insert ...s1s2...s1's2'...
        s2s1 = get_reverse_complement(s1) + get_reverse_complement(s2)
    else:
        # if insert direct circle repeat, insert ...s1s2...s1's2'...
        s2s1 = s2 + s1

    # insert s1s2 and s2s1, where inserted position is sampled from [0,len(seq))
    # if the inserted position overlaps with one of the previous inserted circle repeats, resample insertion position
    # and try again; stop trying after max_itr times
    insert_attempt_count = 0
    while (insert_attempt_count < max_itr):
        insert_attempt_count += 1
        insert_pos_s1s2 = random.randrange(len(curr_seq))
        if (not is_valid_insertion(insert_pos_s1s2, curr_list)):
            continue
        insert_pos_s2s1 = random.randrange(len(curr_seq))
        if (not is_valid_insertion(insert_pos_s2s1, curr_list) or (insert_pos_s1s2 + len(s1s2) > insert_pos_s2s1)):
            continue

        new_seq = insert(curr_seq, s1s2, insert_pos_s1s2)
        new_seq = insert(new_seq, s2s1, insert_pos_s2s1)

        # if the second insertion position is before the first, update the first inserted position
        if (insert_pos_s1s2 < insert_pos_s2s1):
            insert1 = insert_pos_s1s2
            insert2 = insert_pos_s2s1
        else:
            insert1 = insert_pos_s1s2 + len(s1s2)
            insert2 = insert_pos_s2s1


        start1 = min(insert1, insert2)
        start2 = max(insert1, insert2)
        new_list = list()

        # for each previously inserted circle repeat, update its indices
        for circle_repeat in curr_list:
            new_start1 = circle_repeat[0]
            new_start2 = circle_repeat[1]

            if (new_start1 > start1):
                new_start1 += length
            if (new_start1 > start2):
                new_start1 += length

            if (new_start2 > start1):
                new_start2 += length
            if (new_start2 > start2):
                new_start2 += length

            new_list.append([new_start1, new_start2, circle_repeat[2], circle_repeat[3]])

        # add new circle repeat pair to the list
        new_list.append([start1, start2, len(s1s2), len(s2s1)])
        return new_seq,new_list, True

    print("insertion failed")
    return curr_seq, curr_list, False

# insert multiple circle repeat into seq
def insert_circle_repeats(num_crepeats, seq, min_s_len, max_s_len, max_itr, reversed_complement=False):
    circle_repeats = list()
    success_count = 0
    for i in range(num_crepeats):
        seq, circle_repeats, success = insert_circle_repeat(seq, circle_repeats, min_s_len, max_s_len,
                                                            reversed_complement, max_itr)
        if (success):
            success_count += 1

    return seq, circle_repeats, success_count

# add num_mutations mutations to the sequence, and update indices of inserted circle repeats
# each mutation is one of (1) substitution (2) insertion (3) deletion
def add_mutation(num_mutations, seq, circle_repeats):
    new_circle_repeats = list()
    new_seq = seq
    if (num_mutations == 0):
        return seq, circle_repeats

    for i in range(num_mutations):
        # first randomly select a number from {0,1,2} as mutation type
        # 0: substitution
        # 1: insertion
        # 2: deletion
        type = random.randrange(3)

        # randomly select a mutation position in the sequence
        pos = random.randrange(len(new_seq))

        # randomly select a mutation character (used for substitution and insertion)
        # 0 : A
        # 1 : T
        # 2 : C
        # 3 : G
        mutation_num = random.randrange(4)
        mutation_char = ''
        if (mutation_num == 0):
            mutation_char = 'A'
        elif (mutation_num == 1):
            mutation_char = 'T'
        elif (mutation_num == 2):
            mutation_char = 'C'
        elif (mutation_num == 3):
            mutation_char = 'G'

        # update the sequence after insertion
        if (type == 0):
            new_seq = new_seq[:pos] + mutation_char + new_seq[pos+1:]
            continue
        elif (type == 1):
            new_seq = insert(seq, mutation_char, pos)
        elif (type == 2):
            new_seq = new_seq[:pos] + new_seq[pos+1:]

        # update the indices of circle repeats
        for crepeat in circle_repeats:
            start1 = crepeat[0]
            start2 = crepeat[1]
            length1 = crepeat[2]
            length2 = crepeat[3]
            if (pos <= start1):
                if (type == 1):
                    new_circle_repeats.append([start1+1,start2+1,length1,length2])
                if (type == 2):
                    new_circle_repeats.append([start1-1,start2-1,length1,length2])
            elif (pos > start1 and pos < start1 + length1):
                if (type == 1):
                    new_circle_repeats.append([start1,start2+1,length1+1,length2])
                if (type == 2):
                    new_circle_repeats.append([start1,start2-1,length1-1,length2])
            elif (pos >= start1 + length1 and pos <= start2):
                if (type == 1):
                    new_circle_repeats.append([start1,start2+1,length1,length2])
                if (type == 2):
                    new_circle_repeats.append([start1,start2-1,length1,length2])
            elif (pos > start2 and pos < start2 + length2):
                if (type == 1):
                    new_circle_repeats.append([start1,start2+1,length1,length2+1])
                if (type == 2):
                    new_circle_repeats.append([start1,start2-1,length1,length2-1])
            elif (pos >= start2 + length2):
                new_circle_repeats.append(crepeat)
        return new_seq, new_circle_repeats

# Given the simulated sequence, its corresponding circle repeats, and the result (the index file) obtained from the
# circle repeat finding algorithm, we check how many circle repeats where found and missed by the algorithm
# since the algorithm can only approximately find circle repeats, we allow the found circle repeats to be off by a
# certain number of bases, which is determined by (off_allowed_ratio * (avg length of that circle repeat pair) )

# seq: simulated seq
# index_file_name: the index file output by circle repeat finding algorithm containing info of circle repeats locations
# actual_circle_repeats: circle repeats info when creating the simulated seq (ground truth)
# off_allowed_ratio: see above comment
def check_simulated_results(seq, index_file_name, actual_circle_repeats, off_allowed_ratio):
    from CircleRepeat.circle_repeats_setup import setup_circle_repeats_from_index_file
    circle_repeat_pairs = setup_circle_repeats_from_index_file(seq, index_file_name)

    found_count = 0
    for c_found in circle_repeat_pairs:
        for actual_c in actual_circle_repeats:
            off_allowed = max(off_allowed_ratio * (actual_c[2]+actual_c[3])/2, 1)
            if (abs(c_found.first_index - actual_c[0]) < off_allowed):
                if (abs(c_found.second_index - actual_c[1]) < off_allowed):
                    if (abs(c_found.length - (actual_c[2]+actual_c[3])/2) < off_allowed):
                        found_count += 1

    print("Number of missed circle repeats:",len(actual_circle_repeats) - found_count)
    print("Percentage found: ", found_count/len(actual_circle_repeats))




