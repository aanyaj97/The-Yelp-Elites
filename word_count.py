import json
import os
import re
import ast
import heapq

from mrjob.job import MRJob

class MRReviewWordCount(MRJob):

    def mapper(self, _, line):
        '''
        Mapper function to assign each word a count of one.
        '''

        data_entry = ast.literal_eval(line)
        words = re.findall(r'\w+', data_entry['text'])
        lower_unique = set([word.lower() for word in words])
        for word in lower_unique:
            yield (word, 1)

    def combiner(self, word, count):
        '''
        Combiner function to count words.
        '''

        yield (word, sum(count))


    def reducer(self, word, count):
        yield ({word: sum(count)}, None)



if __name__ == '__main__':
    MRReviewWordCount.run()
