import json
import os
import re
import ast
import heapq

from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
from mr3px.csvprotocol import CsvProtocol

class MRReviewWordCount(MRJob):

    INPUT_PROTOCOL: JSONValueProtocol
    OUTPUT_PROTOCOL: CsvProtocol

    def mapper(self, _, line):
        '''
        Mapper function to assign each word a count of one.
        '''

        data_entry = ast.literal_eval(line)
        words = re.findall(r'\w+', data_entry['text'])
        for word in words:
            yield (word.lower(), 1)

    def combiner(self, word, count):
        '''
        Combiner function to count words.
        '''

        yield (word, sum(count))


    def reducer(self, word, count):

        yield (word, sum(count))
m



if __name__ == '__main__':
    MRReviewWordCount.run()
