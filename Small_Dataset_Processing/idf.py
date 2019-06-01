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
import math

from mrjob.job import MRJob

NUM_REV = 30904

class MRIDF(MRJob):

    def configure_args(self):
        super(MRIDF, self).configure_args()
        self.add_file_arg('--json1')
        self.add_file_arg('--json2')

    def mapper(self, _, line):
        '''
        Mapper function to tally word frequencies.
        '''
        self.freq = self.options.json1
        self.vocab = self.options.json2
        data_entry = ast.literal_eval(line)
        review_id = data_entry["review_id"]
        with open(self.freq) as f1:
            freq_ind = json.load(f1)
        with open(self.vocab) as f2:
            vocab_ind = json.load(f2)
        idf_vec = [0] * len(vocab_ind)
        for word, ind in vocab_ind.items():
            if word in freq_ind.keys():
                revfreq = int(freq_ind[word])
                idf = NUM_REV/(1 + revfreq)
                idf = math.log(idf)
                idf_vec[ind] = idf
        yield(review_id, idf_vec)

    def combiner(self, review_id, idf_vec):
        '''
        Combiner.
        '''

        yield (review_id, list(idf_vec))

    def reducer(self, review_id, idf_vec):
        '''
        Reducer function.
        '''
        yield (review_id, list(idf_vec))



if __name__ == '__main__':
    MRIDF.run()
