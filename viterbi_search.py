__author__ = 'jma'
# encoding=utf-8
#
# !! Experimental code for search algorithm (without lookahead)
#

from lattice_build import lattice_build_bigram

lines_of_sent = [u"材 料 利 用 率 高".split()]  # with and without special symbol for start/end of sentence
word_list = [u'材料', u'利用', u'利用率', u'率', u'高']

forward_unigram_lattice, backward_bigram_lattice = lattice_build_bigram(word_list, lines_of_sent)


def bigram_score(tuple_of_word):
    word1, word2 = tuple_of_word
    return len(word2)


def viterbi_search(backward_lattice, max_word_len):
    print "start viterbi search..."

    best_seq = []

    # ########
    # basis #
    # ########
    init_word_seq, init_start_index_last_word, init_score = ['#START#'], "NULL", 1.0
    best_seq.append({init_start_index_last_word: (init_score, "NULL")})

    for i in range(1, len(backward_lattice) + 1):

        best_table={}

        for j in range(max(i - max_word_len, 0), i):

            if best_seq[j]:  # exist valid best seq at position j

                best_score = 0
                best_back_tracer = None
                for k in best_seq[j]:
                    sub_score, sub_last_word_start_index = best_seq[j][k]

                    new_score = sub_score + bigram_score(backward_lattice[i-1][j][k]) > best_score
                    if new_score > best_score:
                        best_score = new_score
                        best_back_tracer = k

                best_table [j] = (best_score, best_back_tracer)

        best_seq.append(best_table)

    #######
    # final test
    #######

    best_index_seq=[]

    sent_len=len(backward_lattice)

    best_score = 0
    if best_seq[sent_len]:
        print "YES!"

        last_position_record=[best_seq[sent_len][x] for x in best_seq[sent_len]]
        last_position_record.sort(reverse=True)

        best_score, last_word_start = last_position_record[0]

        best_index_seq=[sent_len]


        while type (last_word_start) is int:

            best_index_seq.insert(0, last_word_start)
            last_word_start = best_seq[last_word_start][1]

        print best_index_seq


from lattice_build import lattice_build_bigram

lines_of_sent = [u"材 料 利 用 率 高".split()]  # with and without special symbol for start/end of sentence
word_list = [u'材料', u'利用', u'利用率', u'率', u'高']

lattice_list=lattice_build_bigram(word_list, lines_of_sent)
backward_lattice=[i[1] for i in lattice_list]
print backward_lattice
viterbi_search(backward_lattice, 3)










