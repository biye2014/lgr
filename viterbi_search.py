__author__ = 'jma'
# encoding=utf-8
#
# !! Experimental code for search algorithm (without lookahead)
#

from lattice_build import lattice_build_bigram

lines_of_sent = [u"材 料 利 用 率 高".split()]  # with and without special symbol for start/end of sentence
word_list = [u'材料', u'利用', u'利用率', u'率', u'高']

lattice_list = lattice_build_bigram(word_list, lines_of_sent)


def viterbi_search(backward_lattice, max_word_len):
    best_seq = []

    # ########
    # basis #
    # ########
    init_word_seq, init_start_index_last_word, init_score = ['#START#'], None, 1.0
    best_seq.append((init_word_seq, init_word_seq, init_score))


    # ################
    # Inductive Step#
    #################

    for i in range(1, len(backward_lattice) + 1):

        best = None

        for j in range(max(i - max_word_len, 0), i):

            if best_seq[i - j]:  # exist valid best seq at position i-k
                backward_table = backward_lattice[
                    i - 1]  #backward_lattice keeps records starting from position 1 of the sent

                if backward_table[
                            i - j]:  #exist at least one bigram (previous_word, current_word), and current_word=sent[i-k:i]
                    pass

                    #set_of_bigrams = backward_table[i - k]

                    #last_word_of_best_seq =



