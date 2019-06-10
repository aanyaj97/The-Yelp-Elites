import json
from mrjob.job import MRJob
import string
import ast
from mrjob.protocol import JSONValueProtocol

class MRGetReviewWords(MRJob):

    OUTPUT_PROTOCOL = JSONValueProtocol

    def mapper(self, _, line):
        data_entry = ast.literal_eval(line)
        words = data_entry["text"].split()
        review_id = data_entry["review_id"]
        review_text = [word.translate(str.maketrans('', '',\
                           string.punctuation)).lower() for word in words]
        yield (review_id, review_text), 1

    def reducer_init(self):
        self.review_text_dict = {}

    def reducer(self, key, values):
        review_id = key[0]
        review_text = key[1]
        self.review_text_dict[review_id] = review_text

    def reducer_final(self):
        yield None, self.review_text_dict

if __name__ == '__main__':
    MRGetReviewWords.run()