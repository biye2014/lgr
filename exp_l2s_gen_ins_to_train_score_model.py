__author__ = 'jma'
# encoding=utf-8

'''
This code:lattice2seg_experiment, module: gen_instance_to_train_score_model

Input: train.corpus.seg

Output: train.score.instance, each instance represent a state in the segmentation <previous_word, current_word, incoming_char>
mapped to a feature space specified by feature_gen () specified in feature_gen.py

Procedure:
1. extract  train.word
2. gen train.lattice using lattice_build.py
3. gen_instance_to_train_score_model by traversal of the train.lattice and calling feature_gen (note: this traversal is similar to Viterbi in a way)


'''
from lattice_build import gen_lattice, b_lattic_display
from feature_gen import feature_gen


def get_incoming_char(sent, sent_index, dummy_end):
    # dummy_end = u"$END#"
    if sent_index < len(sent):
        return sent[sent_index]
    else:
        return dummy_end


def gen_valid_state(word_seq, dummy_start, dummy_end):
    # dummy_start = u'$START#'
    #dummy_end = u'$END#'

    previous_word_seq = [dummy_start] + word_seq[:-1]
    bigram_seq = zip(previous_word_seq, word_seq)

    char_position_seq = []
    count = 0
    for word in word_seq:
        char_position_seq.append(len(word) + count)
        count += len(word)

    char_seq = u"".join(word_seq)
    incoming_char_seq = [char_seq[i] for i in char_position_seq[:-1]]
    incoming_char_seq.append(dummy_end)

    assert len(incoming_char_seq) == len(bigram_seq)

    valid_state = [(bigram_seq[i], incoming_char_seq[i]) for i in range(len(bigram_seq))]

    #for i in valid_state:
    #print u"==".join((i[0][0], i[0][1], i[1])

    return set(valid_state)


def gen_instance_by_traversal_lattice(valid_state, backward_lattice, sent, dummy_end):
    instance = []

    display_flag = True
    if display_flag: print "instance gen..."

    for i in range(1, len(backward_lattice) + 1):

        incoming_char = get_incoming_char(sent, i, dummy_end)

        if display_flag:  print '\n\ni=', i

        cached_bigram = backward_lattice[i - 1]

        for j in cached_bigram:

            if display_flag: print '\tj=', j

            if j == 0:
                label = u"F"

                if (cached_bigram[0], incoming_char) in valid_state:
                    label = u"T"

                feature = feature_gen(cached_bigram[0], incoming_char)
                instance.append((label, feature))

                if display_flag: print '\t## label/bigram/incoming_char=', label, u"-".join(cached_bigram[0]) \
                    , incoming_char, 'feature=', u"/".join(feature)

            else:

                for k in cached_bigram[j]:
                    bigram = cached_bigram[j][k]

                    label = u"F"
                    if (bigram, incoming_char) in valid_state:
                        label = u"T"

                    feature = feature_gen(bigram, incoming_char)
                    instance.append((label, feature))

                    if display_flag: print '\t\tk=', k, 'label/bigram/incoming_char=', label, u"-".join(
                        bigram), incoming_char, 'feature=', u"/".join(feature)

    return instance


def test():
    word_set = [u'材料', u'利用', u'利用率', u'率', u'高']

    word_seq = [u'材料', u'利用率', u'高']

    raw_sent = u"".join(word_seq)

    max_word_len = 3
    dummy_start, dummy_end = u'$START#', u'$END#'

    f_lattice, b_lattice = gen_lattice(word_set, raw_sent, max_word_len, dummy_start)

    b_lattic_display(b_lattice)

    valid_state = gen_valid_state(word_seq, dummy_start, dummy_end)

    instance = gen_instance_by_traversal_lattice(valid_state, b_lattice, raw_sent, dummy_end)

    print '\n\n=====  Display all instances ====='
    for i in instance:
        print i[0], u"/".join(i[1])


test()