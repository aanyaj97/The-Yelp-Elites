'''
Conversion code to transfer mrjob output into a json of words with unique
numerical 'key' to be referenced in tf/idf vectors.
'''

import json

def mrtransfer(infile, outfile):
    with open(outfile, 'w') as fout:
        with open(infile, 'r') as fin:
            d = {}
            for line in fin:
                word_key = tuple(line.split())
                if len(word_key) == 2:
                    k, v = word_key
                    d[k[1:-1]] = v
            json.dump(d, fout)

mrtransfer('revfreq_smallmrjob.json', 'rev_freq.json')
