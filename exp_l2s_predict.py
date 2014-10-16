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
    


#test()
#test1_2()
#test2_1()
##TODO  code to handle "fail to segment" error (make each char a possible word)
