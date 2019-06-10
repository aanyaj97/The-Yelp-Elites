'''
MapReduce code to run with Google Cloud to form a 'vocabulary' of all
words used in reviews.
'''

import json
import os
import re
import string
import mrjob
import ast

from mrjob.job import MRJob

# remove the top 50 words (likely stop words) from vocabulary as they do not
# indicate sentiment.

#with open('top50_dict.json', 'r') as top_words_file:
#    TOP_WORDS = json.load(top_words_file)

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

index_count = -1

class MRReviewWordCount(MRJob):

    def mapper(self, _, line):
        '''
        Mapper function to assign each word a count of one.
        '''

        data_entry = ast.literal_eval(line)
        words = data_entry["text"].split()
        lower_unique = set([word.translate(str.maketrans('', '',\
                           string.punctuation)).lower() for word in words])
        for word in lower_unique:
            if word not in set(TOP_WORDS + STOP_WORDS):
               yield (word, 1)

    def combiner(self, word, count):
        '''
        Combiner function to count words.
        '''

        yield (word, sum(count))

    def reducer_init(self):
        self.count = -1  # start count at 0

    def reducer(self, word, count):
        if sum(count) >= 50:
            index_count += 1
            yield (word, index_count)



if __name__ == '__main__':
    MRReviewWordCount.run()
