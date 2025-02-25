import json
from mrjob.job import MRJob
import string
import ast
from mrjob.protocol import JSONValueProtocol
'''
    Use MapReduce to extract the business ID from each review in a dataset.
    Example output (using Champaign dataset) is in reviewid_businessid_dict.json
    To run:
    python3 get_business_id_from_review_id_MRJob.py <review dataset filename (JSON)>
'''

class MRGetBusinessID(MRJob):

    OUTPUT_PROTOCOL = JSONValueProtocol

    def mapper(self, _, line):
        data_entry = ast.literal_eval(line)
        business_id = data_entry["business_id"]
        review_id = data_entry["review_id"]
        yield (review_id, business_id), 1

    def reducer_init(self):
        self.business_id_dict = {}

    def reducer(self, key, values):
        review_id = key[0]
        business_id = key[1]
        self.business_id_dict[review_id] = business_id

    def reducer_final(self):
        yield None, self.business_id_dict

if __name__ == '__main__':
    MRGetBusinessID.run()
