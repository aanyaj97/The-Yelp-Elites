import json
import os
import re
import ast
import heapq
import string

from mrjob.job import MRJob

class MRReviewWordCount(MRJob):


    def mapper(self, _, line):
        '''
        Mapper function to assign each word a count of one.
        '''

        data_entry = ast.literal_eval(line)
        words = data_entry["text"].split()
        lower_unique = [word.translate(str.maketrans('', '',\
                           string.punctuation)).lower() for word in words]
        for word in lower_unique:
            if word:
               yield (word, 1)

    def combiner(self, word, count):
        '''
        Combiner function to count visits per visitor.
        '''

        yield (word, sum(count))

    def reducer_init(self):
        self.top_fifty = []

    def reducer(self, word, count):
        '''
        Reducer function to filter out words whose count is less than the top 50.
        '''

        total = sum(count)
        if len(self.top_fifty) < 50:
            heapq.heappush(self.top_fifty, (total, word))
        else:
            heapq.heappushpop(self.top_fifty, (total, word))

    def reducer_final(self):
        for counts, word in self.top_fifty:
            yield (word, counts)


if __name__ == '__main__':
    MRReviewWordCount.run()
