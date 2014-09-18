__author__ = 'jma'
# encoding=utf-8
#
# !! Experimental code for search algorithm (without lookahead)
#

from lattice_build import lattice_build_bigram

lines_of_sent = [u"材 料 利 用 率 高".split()]  # with and without special symbol for start/end of sentence
word_list = [u'材料', u'利用', u'利用率', u'率', u'高']

lattice_list = lattice_build_bigram(word_list, lines_of_sent)


def bigram_score(tuple_of_word):
    word1, word2 = tuple_of_word
    return len(word2)


def viterbi_search(backward_lattice, max_word_len):
    best_seq = []

    # ########
    # basis #
    # ########
    init_word_seq, init_start_index_last_word, init_score = ['#START#'], None, 1.0
    best_seq.append({init_start_index_last_word: (init_score, None)})





