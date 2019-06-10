import json
from mrjob.job import MRJob
'''
    Uses MapReduce to grab review ID from review datasets. Used in conjunction with runner.py and
    runner_states.py to index review IDs from different review datasets.
'''

class MRIndex(MRJob):

    def mapper(self, _, line):
        line = json.loads(line)
        yield line['review_id'], 1

    def reducer(self, key, values):
        yield None, key

if __name__ == '__main__':
    MRIndex.run()
