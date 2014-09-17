__author__ = 'jma'
#test windows
def lattice_build_bigram(word_list, lines_of_sentences):
    if not type(word_list) is set:
        word_list=set(word_list)

    lattice_list=[]

    for sent in lines_of_sentences:
        lattice=[]
        print "\n\n------ sent=",  " ".join(sent), "------"
        sent_len=len(sent)

        for current_word_end_index in range (1, sent_len):
            print '\n\n==>position ',current_word_end_index

            print '#current_end=', current_word_end_index

            backward_bigram_table={}

            for current_word_start_index in range (current_word_end_index):

                current_word = u"".join(sent[current_word_start_index: current_word_end_index])

                print '\n$$current_start=', current_word_start_index, 'current_word=', current_word

                if current_word_start_index == 0:

                    if  current_word in word_list:
                        previous_word_start_index = None
                        previous_word = '#START#'
                        backward_bigram_table[0]={(previous_word_start_index, current_word_start_index, previous_word, current_word)}

                    print previous_word_start_index, current_word_end_index, previous_word, current_word


                elif current_word in word_list:
                    set_of_bigram_tuples=set()

                    for previous_word_start_index in range(current_word_start_index):

                        previous_word = u"".join(sent[previous_word_start_index: current_word_start_index])
                        if previous_word in word_list:
                            set_of_bigram_tuples.add((previous_word_start_index, current_word_start_index, previous_word, current_word))

                            print previous_word_start_index, current_word_start_index, previous_word, current_word

                    backward_bigram_table[current_word_start_index]= set_of_bigram_tuples










