__author__ = 'jma'
# encoding=utf-8

# #######################
#
# generate features from word-bigram and character sequences for evaluation
#
#########################
#
# generate features from word-bigram and their context
#

def feature_gen(bigram, incoming_char):


    dummy_start = u"$START#"  #ideally, this dummy_start should be passed as parameter, we just keep it as it is for now.

    previous_word, word = bigram[0], bigram[1]

    ##################
    # base_feature: 13 base features are from word-based CWS, Zhang & Clark (2011)
    ####################



    word_end = word[-1]
    word_begin = word[0]
    word_len_str = u"".join(str(len(word)))

    if previous_word == dummy_start:
        p_word_end = previous_word
        p_word_len_str = u"1"
    else:
        p_word_end = previous_word[-1]
        p_word_len_str=u"".join(str(len(previous_word)))
        #p_word_begin = previous_word[0]




    tie=u"_"
    base_feature_str_list = [word, tie.join([previous_word, word]), tie.join([word_begin, word_len_str]), \
                        tie.join([word_end, word_len_str]), tie.join([word_end, incoming_char]), \
                        tie.join([word_begin, word_end]), tie.join([word,incoming_char]),tie.join([p_word_end, word]),\
                        tie.join([word_begin,incoming_char]),tie.join([p_word_end, word_end]),\
                        tie.join([previous_word,word_len_str]), tie.join([p_word_len_str, word]), tie.join([p_word_len_str, word])]



    id=[u"1",u"2"]+[u"".join(str(i)) for i in range(4,7)]+[u"".join(str(i)) for i in range(8,15)]
    id_feature_list= zip(id, base_feature_str_list)
    base_feature_list=[u"f"+u"".join(id_feature[0])+u"_"+id_feature[1] for id_feature in id_feature_list]

    f3 = None
    if len(word) == 1:
        f3 = word+u"_one"

    if f3:
        base_feature_list.append(u"f3_"+f3)

    return tuple(base_feature_list)


    #============> We'll skip the word structure features at the moment

    ############
    # Group A feature: head_char to substitute begin/end char of word
    ############

    ############
    # group B extended feature: word tag to substitute begin/end char of word
    #############


def test_base_feature():

    for p_word, word, incoming_char in [(u"中国", u"民众们", u"站"), (u"我们", u"和", u"敌")]:
        f_list = feature_gen((p_word, word), incoming_char)
        print "\np_word, word, char are: ", p_word, word, incoming_char, "  , then features are:"
        for feature in f_list:
            print feature


#test_base_feature()