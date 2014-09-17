__author__ = 'jma'
# encoding=utf-8
#test windows
def lattice_build_bigram(word_list, lines_of_sentences):
    max_word_len = 3


    if not type(word_list) is set:
        word_list=set(word_list)

    lattice_list=[]

    for sent in lines_of_sentences:

        backward_bigram_lattice = []
        forward_unigram_lattice = [{} for i in range(len(sent))]

        print len(forward_unigram_lattice), type(forward_unigram_lattice), type(forward_unigram_lattice[0])

        print "\n\n------ sent=",  " ".join(sent), "------"
        sent_len=len(sent)

        for current_word_end_index in range(1, sent_len + 1):
            print '\n\n==>position ',current_word_end_index

            print '#current_end=', current_word_end_index

            backward_bigram_table={}

            for current_word_start_index in range(max(0, current_word_end_index - max_word_len), current_word_end_index):

                current_word = u"".join(sent[current_word_start_index:current_word_end_index])

                print '\n$$current_start=', current_word_start_index, 'current_word_hypothesis=', current_word

                if current_word_start_index == 0:

                    if  current_word in word_list:
                        print 'CCurrent_word IS A WORD!'

                        previous_word_start_index = None
                        previous_word = '#START#'
                        backward_bigram_table[0]={(previous_word_start_index, current_word_start_index, previous_word, current_word)}

                        print 'end_index, previous_word, current_word==>', current_word_start_index, previous_word, current_word

                        print '!! forward-table update'
                        forward_unigram_lattice[current_word_start_index][current_word_end_index] = current_word


                elif current_word in word_list:

                    set_of_bigram_tuples=set()

                    print '>current word IS A WORD!'

                    print '!! forward-table update'
                    forward_unigram_lattice[current_word_start_index][current_word_end_index] = current_word

                    for previous_word_start_index in range(max(0, current_word_start_index - max_word_len),
                                                           current_word_start_index):
                        #print 'previous_start=', previous_word_start_index

                        previous_word = u"".join(sent[previous_word_start_index: current_word_start_index])

                        if previous_word in word_list:
                            set_of_bigram_tuples.add((previous_word_start_index, current_word_start_index, previous_word, current_word))

                            print 'p_start, current_start, previous_word, current_word==>', previous_word_start_index \
                                , current_word_start_index, previous_word, current_word, "(check=", \
                                u"".join(sent[previous_word_start_index:current_word_start_index]), u"".join(
                                sent[current_word_start_index:current_word_end_index]), ')'

                    backward_bigram_table[current_word_start_index]= set_of_bigram_tuples

            backward_bigram_lattice.append(backward_bigram_table)

        #
        # check forward_word_lattice
        #
        print '\n========  checking forward word lattice ======='
        for index, forward_word_table in enumerate(forward_unigram_lattice):
            print '\n\n** index=', index
            for index2 in forward_word_table:
                print 'end_index=', index2, 'word=', u"".join(sent[index:index2]), 'check=', forward_word_table[index2]


        #
        # check bigram_lattice
        #
        print '\n=======  checking backward bigram lattice ======'
        for index, backward_bigram_table in enumerate(backward_bigram_lattice):
            print '\n\n## index=', index + 1  # <---------- index+1 is very important
            # first record of bigram_lattice starts at index 1!

            for index2 in backward_bigram_table:
                print '##-## current_start, current_end, current_word = ', index2, index + 1, u"".join(
                    sent[index2:index + 1])
                for p_start, c_start, previous_word, current_word in backward_bigram_table[index2]:
                    print 'p_start, current_start, current_end,  previous_word, current_word==>', p_start, c_start, index + 1, previous_word, current_word, "(check=", u"".join(
                        sent[p_start:c_start]), u"".join(sent[c_start:index + 1]), ')'

        print 'length of forward_lattice', len(forward_unigram_lattice), 'len of backward_lattice', len(
            backward_bigram_lattice)


lines_of_sent = [u"材 料 利 用 率 高".split()]  # with and without special symbol for start/end of sentence

word_list = [u'材料', u'利用', u'利用率', u'率', u'高']

lattice_build_bigram(word_list, lines_of_sent)






