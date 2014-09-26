__author__ = 'jma'
# encoding=utf-8
#
# !! Experimental code for search algorithm (without lookahead)
#

from feature_gen import feature_gen


def bigram_score(tuple_of_word):
    word1, word2 = tuple_of_word
    return 1.0


def score_it (score_model, bigram, incoming_char):
    return -1.0
'''
    previous_word, current_word = bigram
    feature= feature_gen (previous_word, current_word, incoming_char)
    print "feature:", u" ".join(feature)
    score = len(score_model+feature)

    return score
'''



def get_incoming_char(sent, sent_index):

    if sent_index < len(sent):
        return sent[sent_index]
    else:
        return u"$END#"


def viterbi_search(score_model, backward_lattice, sent, max_word_len):


    display_flag = True

    if display_flag: print "start viterbi search..."

    best_partial_combination = []



    # ########
    # basis #
    # ########
    # init_lastword, init_score = dummy_start, 1.0

    init_score = 0.0
    best_partial_combination.append(init_score)

    lattice_len = len(backward_lattice)

    for i in range(1, lattice_len + 1):

        incoming_char = get_incoming_char(sent, i)

        if display_flag:  print '\n\ni=', i

        best_seq = {}
        cached_bigram = backward_lattice[i - 1]

        for j in cached_bigram:

            if display_flag: print '\tj=',j

            # j==0  cached_bigram is a dict, key=index value: (dummy_start_word, sent[j:i])
            if j == 0:
                best_score = best_partial_combination[0] + score_it(score_model, cached_bigram[0], incoming_char)
                best_seq[j] = (best_score, 0)

                if display_flag: print '\tSPECIAL partial_score, bigram_score=', best_partial_combination[0] \
                    , score_it(score_model, cached_bigram[0], incoming_char), 'final_score=', best_score, 'bigram=', "-".join(cached_bigram[0])

            else:
                #j>0  cached_bigram is a dict of dict such that cached_bigram[j][k] maps to bigram (sent[k:j], sent[j:i])

                best_score = min(best_partial_combination[j][k][0] for k in best_partial_combination[j]) - 1
                best_tracer = None

                print '??? Initial best_score, best_tracer=', best_score, best_tracer

                for k in cached_bigram[j]:

                    bigram = cached_bigram[j][k]

                    score = best_partial_combination[j][k][0] + score_it(score_model, bigram, incoming_char)

                    if display_flag: print '\t\tk=', k, 'bigram/partial score=', "-".join(bigram), score_it(score_model, bigram, incoming_char), \
                        best_partial_combination[j][k][0], ' Final score=', score

                    if score > best_score:
                        best_score, best_tracer = score, k

                best_seq[j] = (best_score, best_tracer)

                if display_flag: print '\t\t>>best k found(with score):', best_tracer, best_score

        best_partial_combination.append(best_seq)

    #######
    # final test
    #######

    best_index_seq=[]

    sent_len=len(backward_lattice)

    best_score = 0
    if best_partial_combination[sent_len]:
        print "YES!"

        last_word_record = [(j, best_partial_combination[sent_len][j]) for j in best_partial_combination[sent_len]]
        last_word_record.sort(key=lambda x: x[1], reverse=True)

        # print last_word_record[0]
        if display_flag: print 'last_comb=', best_partial_combination[sent_len]
        j, (best_score, k) = last_word_record[0]
        if display_flag: print 'best score/j, k=', best_score, j, k

        best_index_seq = [j, sent_len]

        while k > 0:
            best_index_seq.insert(0, k)
            k = last_word_start = best_partial_combination[j][k][1]
        best_index_seq.insert(0, 0)

        print best_index_seq

    return best_index_seq


def test():
    from lattice_build import gen_lattice

    print '\n=== Running viterbi Search Test...'

    sent = u"材 料 利 用 率 高".split()
    word_list = [u'材料', u'利用', u'利用率', u'率', u'高']
    max_word_len = 3
    dummy_start = '#'

    forward_lattice, backward_lattice = gen_lattice(word_list, sent, max_word_len, dummy_start)

    scoring_model = u'I am a model'

    best_index_seq = viterbi_search(scoring_model, backward_lattice, sent, max_word_len)

    x = best_index_seq[:-1]
    y = best_index_seq[1:]
    z = zip(x, y)
    for index1, index2 in z:
        print forward_lattice[index1][index2]
        # print "".join(sent[index1:index2])


test()









