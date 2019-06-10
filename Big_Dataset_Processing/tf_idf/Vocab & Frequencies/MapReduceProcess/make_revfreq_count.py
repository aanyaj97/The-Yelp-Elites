'''
Conversion code to transfer mrjob output into a json of words with review frequency
to be referenced in tf/idf vectors.
'''

import json

with open('revfreq_dict.json', 'w') as outfile:
    with open('revfreq.json', 'r') as infile:
        d = {}
        for line in infile:
            word_key = tuple(line.split())
            if len(word_key) == 2:
                k, v = word_key
                d[k[1:-1]] = int(v)
        json.dump(d, outfile)
