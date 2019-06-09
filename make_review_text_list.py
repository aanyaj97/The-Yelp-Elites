import json
import sys
import csv
import time
'''
    Takes a JSON file of a dictionary mapping review ID to list of words in the review and converts the data
    to a CSV file formatted as a list of reviews.
    Output was used to create the tf-idf vectors for each review.
    Example output is in <state abbreviation>_review_text_list.csv (i.e., SC_review_text_list.csv)
'''

with open('NC_review_text_dict.json', 'r') as f:
    text_dict = json.load(f)

with open('NC_review_index_dict.json', 'r') as h:
    index_dict = json.load(h)

def run():
    start_time = time.time()
    review_text_list = [0]*408060
    for (review_id, review_text) in text_dict.items():
        index = index_dict[review_id]
        if review_text_list[index] == 0:
            review_text_list[index] = review_text
    with open("NC_review_text_list.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(review_text_list)
    end_time = time.time() - start_time
    print(end_time)

if __name__ == '__main__':
    globals()[sys.argv[1]]()
