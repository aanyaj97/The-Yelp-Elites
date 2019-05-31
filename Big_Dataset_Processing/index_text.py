'''
Maps review index to words in top20k vocab.
'''

import json
import os
import re
import ast
import heapq
import string

from mrjob.job import MRJob

TOP_WORDS = ["","from", "one", "their", "time", "get", "if", "here", "like",\
             "just", "its", "service", "so", "place", "there", "me", "out",\
             "are", "our", "good", "were", "you", "at", "all", "not", "have",\
             "they", "food", "i", "very", "was", "of", "had", "great", "a",\
             "for", "be", "as", "in", "it", "is", "we", "to", "with", "the",\
             "my", "but", "this", "that", "and", "on"]
STOP_WORDS = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you",\
              "your", "yours", "yourself", "yourselves", "he", "him", "his",\
              "himself", "she", "her", "hers", "herself", "it", "its", "itself",\
              "they", "them", "their", "theirs", "themselves", "what", "which",\
              "who", "whom", "this", "that", "these", "those", "am", "is", "are",\
              "was", "were", "be", "been", "being", "have", "has", "had", "having",\
              "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if",\
              "or", "because", "as", "until", "while", "of", "at", "by", "for",\
              "with", "about", "against", "between", "into", "through", "during",\
              "before", "after", "above", "below", "to", "from", "up", "down",\
              "in", "out", "on", "off", "over", "under", "again", "further",\
              "then", "once", "here", "there", "when", "where", "why", "how",\
              "all", "any", "both", "each", "few", "more", "most", "other", "some",\
              "such", "no", "nor", "not", "only", "own", "same", "so", "than",\
              "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

class MRReviewWordCount(MRJob):

    def configure_args(self):
        super(MRReviewWordCount, self).configure_args()
        self.add_file_arg('--json1')
        self.add_file_arg('--json2')

    def mapper(self, _, line):
        '''
        Mapper function to assign each word a count of one.
        '''
        self.vocab_json = self.options.json1
        with open(self.vocab_json) as f:
            dict = json.load(f)
            vocab = dict.keys()
        data_entry = ast.literal_eval(line)
        words = data_entry["text"].split()
        review_id = data_entry["review_id"]
        lower_unique = set([word.translate(str.maketrans('', '',\
                           string.punctuation)).lower() for word in words])
        review_words = []
        for word in lower_unique:
            if word in list(dict.keys()):
                review_words.append(word)

        yield (review_id, review_words)

    def reducer(self, review_id, review_words):
        '''
        Reducer function to count word review frequency.
        '''
        self.review_id_json = self.options.json2
        with open(self.review_id_json) as f2:
            id_dict = json.load(f2)
            index = id_dict[review_id]

        yield (index, list(review_words))



if __name__ == '__main__':
    MRReviewWordCount.run()
