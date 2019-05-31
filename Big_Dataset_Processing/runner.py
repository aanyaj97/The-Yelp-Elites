from index import MRIndex
import mrjob
import json
import sys
import re
import mrjob.parse
from google.cloud import logging
from google.cloud import storage

def run():
    reducer_output = []
    mr_job = MRIndex(args=['-r', 'dataproc', 'gs://yelp-reviews-json/review.json'])
    with mr_job.make_runner() as runner:
        runner.run()
        for line in mrjob.util.to_lines(runner.cat_output()):
            reducer_output.append(line)
        sorted_output = sorted(reducer_output)
        d = {}
        ct = 0
        for i in sorted_output:
            s = i.decode()
            review = re.findall(r'[\w\-]{22}', s)[0]
            d[review] = ct
            ct += 1
    with open('review_index_dict.json', 'w') as f:
        json.dump(d, f)



if __name__ == '__main__':
    globals()[sys.argv[1]]()