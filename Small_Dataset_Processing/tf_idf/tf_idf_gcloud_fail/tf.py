'''
MapReduce code to run with Google Cloud to form a 'vocabulary' of all
words used in reviews.
'''

import json
import os
import re
import string
import mrjob
import ast

from mrjob.job import MRJob

class MRTF(MRJob):

    def configure_args(self):
        super(MRTF, self).configure_args()
        self.add_file_arg('--json')

    def mapper(self, _, line):
        '''
        Mapper function to tally word frequencies.
        '''
        self.vocab = self.options.json
        with open(self.vocab) as f:
            vocab_ind = json.load(f)
        data_entry = ast.literal_eval(line)
        review_id = data_entry["review_id"]
        tf_vec = [0] * len(vocab_ind)
        words = data_entry["text"].split()
        text = [word.translate(str.maketrans('', '',\
                           string.punctuation)).lower() for word in words]
        lower_unique = set(text)
        for word in lower_unique:
            if word in vocab_ind.keys():
                index = vocab_ind[word]
                tf_vec[index] += 1/len(text)
        yield(review_id, tf_vec)

    def combiner(self, review_id, tf_vec):
        '''
        Combiner.
        '''

        yield (review_id, list(tf_vec))

    def reducer(self, review_id, tf_vec):
        '''
        Reducer function.
        '''
        yield (review_id, list(tf_vec))



if __name__ == '__main__':
    MRTF.run()
