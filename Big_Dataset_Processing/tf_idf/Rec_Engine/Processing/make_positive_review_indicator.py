import numpy as np
import json
from mrjob.job import MRJob
import sys
'''
    Uses MapReduce to create an array of zeros and ones for a review dataset. A review is given a 1 if
    its star rating is greater than or equal to --min_pos_val, and a zero otherwise. Output is a list,
    which was then turned into a sparse matrix using iPython (sparse_pos_matrix.npz).
    Example output comes from Champaign dataset.
'''
with open('Small_Dataset_Processing/smaller_review_index_dict.json', 'r') as f:
    review_index_dict = json.load(f)

class MRNumpy(MRJob):

    def configure_args(self):
        super(MRNumpy, self).configure_args()
        self.add_passthru_arg(
            '--min_pos_val', type=float, default='3.5', help='...')

    def load_args(self, args):
        super(MRNumpy, self).load_args(args)
        self.min_pos_val = self.options.min_pos_val

    def mapper(self, _, line):
        ln = json.loads(line)
        stars_raw = ln['stars']
        if stars_raw >= self.min_pos_val:
            ranking = 1
        else:
            ranking = 0
        review_id = ln['review_id']
        review_index = review_index_dict[review_id]
        yield (review_index, ranking), 1

    def reducer_init(self):
        self.array = np.empty([len(review_index_dict)], int)

    def reducer(self, key, val):
        self.array[int(key[0])] = key[1]

    def reducer_final(self):
        print(self.array)
        array = self.array.tolist()
        yield None, array

if __name__=="__main__":
    MRNumpy.run()
