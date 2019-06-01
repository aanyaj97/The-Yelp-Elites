from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
import ast

class MRUserID4StarReviews(MRJob):

    OUTPUT_PROTOCOL = JSONValueProtocol

    def mapper(self, _, line):
        data_entry = ast.literal_eval(line)
        user_id = data_entry["user_id"]
        review_id = data_entry["review_id"]
        stars = data_entry["stars"]
        if stars >= 4.0:
            yield (user_id, review_id), 1

    def reducer_init(self):
        self.userid_review_dict = {}

    def reducer(self, key, value):
        user_id = key[0]
        review_id = key[1]
        if user_id in self.userid_review_dict.keys():
            self.userid_review_dict[user_id].append(review_id)
        else:
            self.userid_review_dict[user_id] = [review_id]

    def reducer_final(self):
        yield None, self.userid_review_dict

if __name__ == '__main__':
    MRUserID4StarReviews.run()