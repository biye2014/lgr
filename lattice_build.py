__author__ = 'jma'
# encoding=utf-8

def gen_lattice(word_list, sent, max_word_len, dummy_start):

    if not type(word_list) is set:
        word_list=set(word_list)

    backward_bigram_lattice = []
    forward_unigram_lattice = [{} for i in range(len(sent))]

    # print len(forward_unigram_lattice), type(forward_unigram_lattice), type(forward_unigram_lattice[0])
    #print "\nbuilding lattice for------ sent=",  " ".join(sent), "------"

    sent_len = len(sent)

    for i in range(1, sent_len + 1):

        if False:
            print '\n\n==>position ', i
            print '#current_end=', i

        backward_bigram_table = {}

        for j in range(max(0, i - max_word_len), i):

            current_word = u"".join(sent[j:i])

            if False: print '\n$$current_start=', j, 'current_word_hypothesis=', current_word

            if j == 0 and current_word in word_list:

                previous_word = dummy_start

                if False: print 'CCurrent_word IS A WORD!'

                backward_bigram_table[j] = (previous_word, current_word)
                #only 1 possible bigram (with dummy symbol and previous word), so put the tuple directly in b_table[j]

                forward_unigram_lattice[j][i] = current_word

                if False:
                    print 'end_index, previous_word, current_word==>', j, previous_word, current_word
                    print '!! forward-table update'



            elif j > 0 and current_word in word_list:  # j!=0 and current word in word_list



                if False:
                    print '>current word IS A WORD!'
                    print '!! forward-table update'

                forward_unigram_lattice[j][i] = current_word

                # potentially many (real) bigrams, so make a nested dict index2bigram and put it in b_table[j]
                # i.e. if k,j are valid, b_table[j][k] maps to ---> bigram (sent[k:j], sent[j:i])
                dict_index2bigram = {}
                for k in range(max(0, j - max_word_len), j):

                    # print 'previous_start=', k
                    previous_word = u"".join(sent[k: j])

                    if previous_word in word_list:
                        dict_index2bigram[k] = (previous_word, current_word)

                        # print 'p_start, current_start, previous_word, current_word==>', k \
                        #    , j, previous_word, current_word, "(check=", \
                        #    u"".join(sent[k:j]), u"".join(sent[j:i]), ')'

                backward_bigram_table[j] = dict_index2bigram

        backward_bigram_lattice.append(backward_bigram_table)

    return forward_unigram_lattice, backward_bigram_lattice


def b_lattic_display(b_lattice):
    print "\nDisplay backward lattice"
    for i, table in enumerate(b_lattice):
        print  i + 1
        for j in table:
            if j == 0:
                print "Special bigram", (j, i + 1), "-".join(table[j])

            else:
                for k in table[j]:
                    print "\tbigram", (k, j, i + 1), "-".join(table[j][k])


def f_lattice_display(f_lattice):
    print '\nDisplay forward_lattice...'
    for i, table in enumerate(f_lattice):
        print i
        for j in table:
            print '\t', j, "".join(table[j])


print '\n????'

sent = u"材 料 利 用 率 高".split()
print " - ".join(sent)

word_list = [u'材料', u'利用', u'利用率', u'率', u'高']

max_word_len = 3
dummy_start = '$START#'

forward_unigram_lattice, backward_bigram_lattice = gen_lattice(word_list, sent, max_word_len, dummy_start)

b_lattic_display(backward_bigram_lattice)
f_lattice_display(forward_unigram_lattice)




