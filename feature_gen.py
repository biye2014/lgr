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

def feature_gen(previous_word, word, incoming_char):
    # first 13 features are from word-based CWS, Zhang & Clark (2011)
    f3 = u'NULL'
    if len(word) == 1:
        f3 = u'_l_'.join(word, u'one')

    word_end = word[-1]
    word_begin = word[0]

    p_word_end = previous_word[-1]
    p_word_begin = previous_word[0]

    word_len_str = u"".join(str(len(word)))
    p_word_len_str=u"".join(str(len(previous_word)))


    p_word_len_str = u"".join(str(len(previous_word)))

    base_feature_str = [word, u"_".join(previous_word, word), f3, u"_".join(word[0], word_len_str), \
                        u"".join(word[-1], word_len_str)]


