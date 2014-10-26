# encoding=utf-8
__author__ = 'jma'

'''
Input:

1. the lexicon (the union of training lexcion + lexcicon extracted from *predicted* test corpus)
2. the raw corpus (a bunch of unsegmentd sentences)
3. scoring model that can evaluate


a implicit consistency required for the training code (exp_l2s_ins_to_train_score_model.py) is that both use the same
notabtion for labels, which are "T" and "F" to represent positive and negative labels.


'''

import math
import codecs

from lattice_build import gen_lattice  # b_lattic_display
from viterbi_search import viterbi_search
from feature_gen import feature_gen



# from exp_l2s_gen_ins_to_train_score_model import gen_valid_state, gen_instance_by_traversal_lattice

from maxent import MaxentModel  # need python interface of Zhang Le's maxent package


class ScoreModel(MaxentModel):
    def __init__(self, path_me_model):
        #print "initialization..."
        super(ScoreModel, self).__init__()
        self.load(path_me_model)


    def score_it(self, bigram, incoming_char):
        feature = feature_gen(bigram, incoming_char)
        raw_score = self.eval([u_str.encode('utf-8') for u_str in feature],
                              "T")  # maxent_model only takes utf-8 string as input
        #print '\t\tRaw score=',raw_score

        return math.log(raw_score, 10)


def test_single_sent():
    #parameters
    max_word_len = 15
    dummy_start, dummy_end = u'$START#', u'$END#'

    print '\nRunning test for exp_l2s_predict....'
    path_me_model = "../working_data/train.set1.i80.model"
    path_to_lexicon = "../working_data/train_testPredict.dict"

    sent = u"材 料 利 用 率 高".split()
    sent = u"下 雨 天 留 客 天 天 留 我 不 留".split()
    print "sample sentence is:", " - ".join(sent)

    #
    # loading maximum entropy model as the score function
    #
    print '\nInitializing maximum entropy model as the scoring model'
    model = ScoreModel(path_me_model)
    print 'done'


    #
    # loading lexicion
    #
    print "\nLoading lexicion file..."
    with codecs.open(path_to_lexicon, 'rU', 'utf-8') as f:
        lexicon = [word for line in f for word in line.split()]
        print "lexicion size=", len(lexicon), "example word in lexicion:", "  ".join(lexicon[:5])
        lexicon = set(lexicon)

    print '\n====1 Bui latttice for the sample sentence====='

    forward_unigram_lattice, backward_bigram_lattice = gen_lattice(lexicon, sent, max_word_len, dummy_start)

    print '\n====2 Runing Viterbi search to decode===='
    best_index_seq = viterbi_search(model.score_it, backward_bigram_lattice, sent, dummy_end)
    #b_lattic_display(backward_bigram_lattice)
    #f_lattice_display(forward_unigram_lattice)

    x = best_index_seq[:-1]
    y = best_index_seq[1:]
    z = zip(x, y)

    segmented = []
    for index1, index2 in z:
        word = u"".join(sent[index1:index2])
        print word
        segmented.append(word)

    print '\nSegmented sent=', u" ".join(segmented)


def main(path_corpus, path_me_model, path_to_lexicon, path_to_output):
    max_word_len = 12
    dummy_start, dummy_end = u'$START#', u'$END#'


    #
    # loading maximum entropy model as the score function
    #
    print '\nInitializing maximum entropy model as the scoring model'
    model = ScoreModel(path_me_model)
    print 'done'


    #
    # loading lexicion
    #
    print "\nLoading lexicion file..."
    with codecs.open(path_to_lexicon, 'rU', 'utf-8') as f:
        lexicon = [word for line in f for word in line.split()]
        print "lexicion size=", len(lexicon), "example word in lexicion:", "  ".join(lexicon[:5])
        lexicon = set(lexicon)

    segmented_corpus = []

    print "\nLoading corpus to be segmented..."
    with codecs.open(path_corpus, 'rU', 'utf-8') as f:
        raw_corpus = [u"".join(line.split()) for line in f]
        print 'line count of raw_corpus=', len(raw_corpus)
        print 'the first line is ', raw_corpus[0]

    print "\n\n====Segmenting the corpus======"
    for sent in raw_corpus:

        #print '\n====1 Bui latttice for the sample sentence====='

        forward_unigram_lattice, backward_bigram_lattice = gen_lattice(lexicon, sent, max_word_len, dummy_start)

        #print '\n====2 Runing Viterbi search to decode===='
        best_index_seq = viterbi_search(model.score_it, backward_bigram_lattice, sent, dummy_end)
        #b_lattic_display(backward_bigram_lattice)
        #f_lattice_display(forward_unigram_lattice)

        x = best_index_seq[:-1]
        y = best_index_seq[1:]
        z = zip(x, y)

        segmented = []
        for index1, index2 in z:
            word = u"".join(sent[index1:index2])
            #print word
            segmented.append(word)

        print '\nSegmented sent=', u" ".join(segmented)
        segmented_corpus.append(u" ".join(segmented))

    print "\nSegmentation done, writing it to file", path_to_output, '...'
    with codecs.open(path_to_output, 'w', 'utf-8') as f:
        for sent in segmented_corpus:
            f.write(sent + u'\n')

    print 'done'
    print "Program exit."


def test1():
    path_corpus = "../working_data/test.ctb5.seg"
    path_me_model = "../working_data/train.set1.i100.model"
    path_to_lexicon = "../working_data/train_testPredict.dict"
    path_to_output = "../working_data/test.ctb5.seg.l2s"

    main(path_corpus, path_me_model, path_to_lexicon, path_to_output)


def test1_2():
    print "Running test1_2, i.e. experiment Setting 1.2"

    path_corpus = "../working_data/test.ctb5.seg"
    path_me_model = "../working_data/train.set1.i100.model"
    path_to_lexicon = "../working_data/testPredict.dict"
    path_to_output = "../working_data/test.ctb5.seg.l2s.1.2"

    main(path_corpus, path_me_model, path_to_lexicon, path_to_output)



def test2_1():
    print "Running test2_2, i.e. experiment Setting 2.1"

    path_corpus = "../working_data/test.ctb5.seg"
    path_me_model = "../working_data/train.set1.i100.model"
    path_to_lexicon = "../working_data/test_crf_wordhood.dict"
    path_to_output = "../working_data/test.ctb5.seg.l2s.2.1"

    main(path_corpus, path_me_model, path_to_lexicon, path_to_output)


def test2_2():

    print "Running test2_2, i.e. experiment Setting 2.2"

    path_corpus = "../working_data/test.ctb5.seg"
    path_me_model = "../working_data/train.set1.i100.model"
    path_to_lexicon = "../working_data/train_test_crf_wordhood.dict"
    path_to_output = "../working_data/test.ctb5.seg.l2s.22"

    main(path_corpus, path_me_model, path_to_lexicon, path_to_output)


def test_fine():
    print "Running fine, i.e. experiment with .fine (30i) merge-action prediciton model"

    path_corpus = "../working_data/test.ctb5.seg"
    path_me_model = "../working_data/train.set1.i100.model"
    path_to_lexicon = "../working_data/train_crf_wordhood.fine.dict"
    path_to_output = "../working_data/test.ctb5.seg.fine"

    main(path_corpus, path_me_model, path_to_lexicon, path_to_output)


def test_fine50():
    print "Running fine, i.e. experiment with .fine.50i merge-action prediction model"

    path_corpus = "../working_data/test.ctb5.seg"
    path_me_model = "../working_data/train.set1.i100.model"
    path_to_lexicon = "../working_data/train_crf_wordhood.fine.50i.dict"
    path_to_output = "../working_data/test.ctb5.seg.fine50"

    main(path_corpus, path_me_model, path_to_lexicon, path_to_output)


def test_fine100():
    print "Running fine, i.e. experiment with /fine.100i merge-action prediciton model"

    path_corpus = "../working_data/test.ctb5.seg"
    path_me_model = "../working_data/train.set1.i100.model"
    path_to_lexicon = "../working_data/train_crf_wordhood.fine.100i.dict"
    path_to_output = "../working_data/test.ctb5.seg.fine100"

    main(path_corpus, path_me_model, path_to_lexicon, path_to_output)


def test_fine15():
    print "Running fine, i.e. experiment with /fine.15i merge-action prediciton model"

    path_corpus = "../working_data/test.ctb5.seg"
    path_me_model = "../working_data/train.set1.i100.model"
    path_to_lexicon = "../working_data/train_crf_wordhood.fine.15i.dict"
    path_to_output = "../working_data/test.ctb5.seg.fine15"

    main(path_corpus, path_me_model, path_to_lexicon, path_to_output)


def test_fine8():
    print "Running fine, i.e. experiment with /fine.8i merge-action prediciton model"

    path_corpus = "../working_data/test.ctb5.seg"
    path_me_model = "../working_data/train.set1.i100.model"
    path_to_lexicon = "../working_data/train_crf_wordhood.fine.8i.dict"
    path_to_output = "../working_data/test.ctb5.seg.fine8"

    main(path_corpus, path_me_model, path_to_lexicon, path_to_output)


def test_fine2():
    print "Running fine 2i..."

    path_corpus = "../working_data/test.ctb5.seg"
    path_me_model = "../working_data/train.set1.i100.model"
    path_to_lexicon = "../working_data/train_crf_wordhood.fine.2i.dict"
    path_to_output = "../working_data/test.ctb5.seg.fine2"

    main(path_corpus, path_me_model, path_to_lexicon, path_to_output)


def test_merge():
    print "Running fine, i.e. experiment with /exp.merge/model.merge.o16"

    path_corpus = "../working_data/test.ctb5.seg"
    path_me_model = "../working_data/train.set1.i100.model"
    path_to_lexicon = "../exp.merge/o16.train.crf.dict"
    path_to_output = "../exp.merge/test.ctb5.seg.o16"

    main(path_corpus, path_me_model, path_to_lexicon, path_to_output)


def test_merge15():
    print "Running fine, i.e. experiment with /exp.merge/model.merge.o16.i15"

    path_corpus = "../working_data/test.ctb5.seg"
    path_me_model = "../working_data/train.set1.i100.model"
    path_to_lexicon = "../exp.merge/o16.15i.train.crf.dict"
    path_to_output = "../exp.merge/test.ctb5.seg.o16.15i"
    main(path_corpus, path_me_model, path_to_lexicon, path_to_output)


def test_merge100():
    print "Running fine, i.e. experiment with /exp.merge/model.merge.o16.100i"

    path_corpus = "../working_data/test.ctb5.seg"
    path_me_model = "../working_data/train.set1.i100.model"
    path_to_lexicon = "../exp.merge/o16.100i.train.crf.dict"
    path_to_output = "../exp.merge/test.ctb5.seg.o16.100i"

    main(path_corpus, path_me_model, path_to_lexicon, path_to_output)


def test_group():
    print "Running fine, i.e. experiment with /exp.merge.group/model.merge.group.o16"

    path_corpus = "../working_data/test.ctb5.seg"
    path_me_model = "../working_data/train.set1.i100.model"
    path_to_lexicon = "../exp.merge.group/all.o16.train.crf.dict"
    path_to_output = "../exp.merge.group/test.ctb5.seg.group"

    main(path_corpus, path_me_model, path_to_lexicon, path_to_output)


def test_group_i15():
    print "Running fine, i.e. experiment with /exp.merge.group/model.merge.group.o16.i15"

    path_corpus = "../working_data/test.ctb5.seg"
    path_me_model = "../working_data/train.set1.i100.model"
    path_to_lexicon = "../exp.merge.group/all.biye.group.i15.dict"
    path_to_output = "../exp.merge.group/test.ctb5.seg.group.i15"

    main(path_corpus, path_me_model, path_to_lexicon, path_to_output)


def test_group_no_train():
    print "Running fine, i.e. experiment with /exp.merge.group/model.merge.group.o16"

    path_corpus = "../working_data/test.ctb5.seg"
    path_me_model = "../working_data/train.set1.i100.model"
    path_to_lexicon = "../exp.merge.group/group.crf.dict"
    path_to_output = "../exp.merge.group/test.ctb5.seg.group.no_train"

    main(path_corpus, path_me_model, path_to_lexicon, path_to_output)


def test_base():
    path_corpus = "../working_data/test.ctb5.seg"
    path_me_model = "../working_data/train.set1.i100.model"
    path_to_lexicon = "../exp.base/test.ctb5.segwp.model.dict"
    path_to_output = "../exp.base/test.ctb5.seg.base"

    main(path_corpus, path_me_model, path_to_lexicon, path_to_output)


def test_base50():
    path_corpus = "../working_data/test.ctb5.seg"
    path_me_model = "../working_data/train.set1.i100.model"
    path_to_lexicon = "../exp.base/test.ctb5.segwp.model.i50.dict"
    path_to_output = "../exp.base/test.ctb5.seg.base.i50"

    main(path_corpus, path_me_model, path_to_lexicon, path_to_output)


def test_base100():
    path_corpus = "../working_data/test.ctb5.seg"
    path_me_model = "../working_data/train.set1.i100.model"
    path_to_lexicon = "../exp.base/test.ctb5.segmodel.wp.i100.dict"
    path_to_output = "../exp.base/test.ctb5.seg.base.i00"

    main(path_corpus, path_me_model, path_to_lexicon, path_to_output)


#test()
#test1_2()
#test2_1()

def test_base100_no_train():
    path_corpus = "../working_data/test.ctb5.seg"
    path_me_model = "../working_data/train.set1.i100.model"
    path_to_lexicon = "../exp.base/i100.crf.dict"
    path_to_output = "../exp.base/test.ctb5.seg.base.i00"

    main(path_corpus, path_me_model, path_to_lexicon, path_to_output)


def test_a2_100():
    path_corpus = "../working_data/test.ctb5.seg"
    path_me_model = "../working_data/train.set1.i100.model"
    path_to_lexicon = "../working_data/a2.i100.crf.dict"
    path_to_output = "../working_data/a2.i100.seg"

    main(path_corpus, path_me_model, path_to_lexicon, path_to_output)


def test_a2_150():
    path_corpus = "../working_data/test.ctb5.seg"
    path_me_model = "../working_data/train.set1.i100.model"
    path_to_lexicon = "../working_data/a2.i150.crf.dict"
    path_to_output = "../working_data/a2.i150.seg"

    main(path_corpus, path_me_model, path_to_lexicon, path_to_output)


def test_a2_200():
    path_corpus = "../working_data/test.ctb5.seg"
    path_me_model = "../working_data/train.set1.i100.model"
    path_to_lexicon = "../working_data/a2.i200.crf.dict"
    path_to_output = "../working_data/a2.i200.seg"

    main(path_corpus, path_me_model, path_to_lexicon, path_to_output)


def test_a2_100_nobase():
    path_corpus = "../working_data/test.ctb5.seg"
    path_me_model = "../working_data/train.set1.i100.model"
    path_to_lexicon = "../working_data/a2.nobase.100i.crf.dict"
    path_to_output = "../working_data/a2.nobase.i100.seg"

    main(path_corpus, path_me_model, path_to_lexicon, path_to_output)


def test_bichar_extend_150():
    path_corpus = "../working_data/test.ctb5.seg"
    path_me_model = "../working_data/train.set1.i100.model"
    path_to_lexicon = "../working_data/bichar.crf.e.i150.dict"
    path_to_output = "../working_data/bichar.e.i150.seg"

    main(path_corpus, path_me_model, path_to_lexicon, path_to_output)


def test_bichar_150():
    path_corpus = "../working_data/test.ctb5.seg"
    path_me_model = "../working_data/train.set1.i100.model"
    path_to_lexicon = "../working_data/bichar.crf.i150.dict"
    path_to_output = "../working_data/bichar.i150.seg"

    main(path_corpus, path_me_model, path_to_lexicon, path_to_output)


def test_crf():
    path_corpus = "../working_data/test.ctb5.seg"
    path_me_model = "../working_data/train.set1.i100.model"
    path_to_lexicon = "../working_data/test.crf.dict"
    path_to_output = "../working_data/test.crf.seg"

    main(path_corpus, path_me_model, path_to_lexicon, path_to_output)


# #TODO  code to handle "fail to segment" error (make each char a possible wor
if __name__ == '__main__':
    #test_merge()
    #test_merge100()
    #test_merge15()
    # test_group_no_train()
    #test_base()
    #test_base50()
    #test_base100_no_train()

    # test_a2_100()
    #test_a2_150()
    #test_a2_200()
    #test_crf()
    #test_a2_100_nobase()
    test_bichar_extend_150()
    test_bichar_150()

