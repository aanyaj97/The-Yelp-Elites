import json
from mrjob.job import MRJob

class MRIndex(MRJob):

    def mapper(self, _, line):
        line = json.loads(line)
        yield line['review_id'], 1

    def reducer(self, key, values):
        yield None, key

if __name__ == '__main__':
    MRIndex.run()