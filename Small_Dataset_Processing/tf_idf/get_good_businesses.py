from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
import ast
'''
    Use MapReduce to create a list of businesses that have 4.0 stars or higher and are open.
    Example output (using Champaign dataset) is in good_businesses.json
    Used to generate recommendation engine output.
    
    To run:
    python3 get_good_businesses.py <business dataset filename (JSON)>
    '''

class MRGoodBusinesses(MRJob):

    OUTPUT_PROTOCOL = JSONValueProtocol

    def mapper(self, _, line):
        data_entry = ast.literal_eval(line)
        business_id = data_entry["business_id"]
        stars = data_entry["stars"]
        is_open = data_entry["is_open"]
        yield (business_id, stars, is_open), 1

    def reducer_init(self):
        self.good_businesses = []

    def reducer(self, key, value):
        business_id = key[0]
        stars = key[1]
        is_open = key[2]
        if (stars >= 4.0) and (is_open == 1):
            self.good_businesses.append(business_id)

    def reducer_final(self):
        yield None, self.good_businesses

if __name__ == '__main__':
    MRGoodBusinesses.run()