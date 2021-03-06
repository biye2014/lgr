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
import codecs
import sys
import multiprocessing

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

    display_flag = False

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



def write_instance_and_stat(instance_list, output):   #  Each instance is a tuple (label, feature_list)

    print '\nWriting the training instance for scoring model to', output,
    print '...'

    t_count, f_count, other_count = 0, 0, 0
    t_label, f_label = u"T", u"F"

    f=codecs.open(output, 'w','utf-8')
    for label, feature in instance_list:
        #print len(feature), label+u"\t"+u"\t".join(feature)
        f.write(label+u"\t"+u"\t".join(feature)+u"\n")
        if label == t_label:
            t_count += 1
        elif label == f_label:
            f_count += 1
        else:
            other_count +=1
    f.close()
    print 'done'

    total = t_count + f_count + other_count

    assert total == len(instance_list)

    print '\nStat of instances:'
    print '# of positive instance=',t_count, '  percentage=', "{0:.2f}".format(t_count/float(total))
    print '# of negative instance=', f_count, '  percentage=', "{0:.2f}".format(f_count/float(total))
    print '# of instance with unrecognized label, ', other_count

    if other_count !=0:
        print 'Warning: instances with unrecognized label! Check the data/code!'



def read_training_corpus(path_to_corpus):
    print '\nReading segmented-corpus from', path_to_corpus
    print '...'
    corpus, word_list =[], set()
    f = codecs.open(path_to_corpus, 'rU', 'utf-8')
    for line in f:
        sent = line.split()
        corpus.append(sent)
        word_list.update(set(sent))
    f.close()
    print 'done'
    return corpus, word_list



def core(parameter_tuple):

    sent, word_list, max_word_len, dummy_start, dummy_end = parameter_tuple


    raw_sent =u"".join(sent)

    f_lattice, b_lattice = gen_lattice(word_list, raw_sent, max_word_len, dummy_start)


    valid_state = gen_valid_state(sent, dummy_start, dummy_end)

    instances = gen_instance_by_traversal_lattice(valid_state, b_lattice, raw_sent, dummy_end)

    return instances



def main(path_to_corpus, path_to_instance_file, num_proc):



    corpus, word_list = read_training_corpus(path_to_corpus)

    max_word_len = 15 # actually no restriction of word length
    dummy_start, dummy_end = u'$START#', u'$END#'
    print "\n\n==== Generating instances for training scoring function ===="

    #print len(corpus)

    extend_corpus = [(sent, word_list, max_word_len, dummy_start, dummy_end) for sent in corpus]

    pool = multiprocessing.Pool(num_proc)

    list_of_groups = pool.map(core, extend_corpus)
    pool.close()
    pool.join()

    #print type(list_of_groups)

    instance_list = [instance for group in list_of_groups for instance in group]

    write_instance_and_stat(instance_list, path_to_instance_file)


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
#main('../working_data/train.ctb5.seg', '../working_data/tmp.out', 4)

if __name__=='__main__':
    print '\n>>>> Running gen_ins_to_train_score_model'
    print 'This program generates instances to train scoring model of lattice-based segmentation system...'
    print '\n @Arg: 1.training_corpus(segmented), 2. path_to_resulting_instances, 3.num_of_processes '
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]))