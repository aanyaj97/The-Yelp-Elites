import json
from mrjob.job import MRJob
import string
import ast
from mrjob.protocol import JSONValueProtocol
'''
    Use MapReduce to extract the business name from each business in a dataset.
    Used with get_business_id_from_review_id_MRJob.py to generate recommendation engine output.
    Example output (using Champaign dataset) is in businessid_business_name_dict.json
    
    To run:
    python3 get_business_name_from_id_MRJob.py <business dataset filename (JSON)>
    '''
class MRGetBusinessName(MRJob):

    OUTPUT_PROTOCOL = JSONValueProtocol

    def mapper(self, _, line):
        data_entry = ast.literal_eval(line)
        business_id = data_entry["business_id"]
        business_name = data_entry["name"]
        yield (business_id, business_name), 1

    def reducer_init(self):
        self.business_name_dict = {}

    def reducer(self, key, values):
        business_id = key[0]
        business_name = key[1]
        self.business_name_dict[business_id] = business_name

    def reducer_final(self):
        yield None, self.business_name_dict

if __name__ == '__main__':
    MRGetBusinessName.run()
