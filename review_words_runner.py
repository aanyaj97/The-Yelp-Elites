from review_words import MRGetReviewWords
import mrjob
import json
import sys
import re
import mrjob.parse
from google.cloud import logging
from google.cloud import storage
import time

def run():
    start_time = time.time()
    reducer_output = []
    mr_job = MRGetReviewWords(args=['ON_reviews_editedMRJobsafe.json'])
    with mr_job.make_runner() as runner:
        runner.run()
        for line in mrjob.util.to_lines(runner.cat_output()):
            reducer_output.append(line)
        sorted_output = sorted(reducer_output)
        d = {}
        for i in sorted_output:
            s = i.decode()
            review = re.findall(r'[\w\-]{22}', s)[0]
            text = s[29:len(s) - 4]
            text_list = text.split('", "')
            d[review] = text_list
    with open('ON_review_text_dict.json', 'w') as f:
        json.dump(d, f)
    end_time = time.time() - start_time
    print(end_time)

if __name__ == '__main__':
    globals()[sys.argv[1]]()
