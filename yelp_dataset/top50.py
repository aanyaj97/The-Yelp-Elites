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
        Combiner function to count visits per visitor.
        '''

        yield (word, sum(count))

    def reducer_init(self):
        self.top_fifty = []

    def reducer(self, word, count):
        '''
        Reducer function to filter out visitors who visited less than
        10 times.
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

    