__author__ = 'jma'
# encoding=utf-8

'''
This code:lattice2seg_experiment, module: gen_instance_to_train_score_model

Input: train.corpus.seg

Output: train.score.instance, each instance represent a state in the segmentation <previous_word, current_word, incoming_char>
mapped to a feature space specified by feature_gen () specified in feature_gen.py

Procedure:
1. extract  train.word
2. gen train.lattice using lattice_build.py
3. gen_instance_to_train_score_model, via  viterbi_search.py + feature_gen.py

To-do: improve Viterbi_search so that it can be used both in training and testing

'''