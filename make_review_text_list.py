import json
import sys

with open('review_text_dict.json', 'r') as f:
    text_dict = json.load(f)

with open('smaller_review_index_dict.json', 'r') as h:
    index_dict = json.load(h)

def run():
    review_text_list = [0]*30904
    for (review_id, review_text) in text_dict.items():
        index = index_dict[review_id]
        if review_text_list[index] == 0:
            review_text_list[index] = review_text
    with open('review_text_list.csv', 'w') as i:
        i.write(str(review_text_list))

if __name__ == '__main__':
    globals()[sys.argv[1]]()
