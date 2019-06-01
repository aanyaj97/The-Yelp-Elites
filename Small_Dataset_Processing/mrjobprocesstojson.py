'''
Conversion code to transfer mrjob output into a json of words with unique
numerical 'key' to be referenced in tf/idf vectors.
'''

# DOESNT WORK!!
import json

def mrtransfer(infile, outfile):
    with open(outfile, 'w') as fout:
        with open(infile, 'r') as fin:
            counter = 0
            d = {}
            for line in fin:
                word_key = tuple(line.split())
                if len(word_key) == 2:
                    k, v = word_key
                    d[k[1:-1]] = counter
                    counter += 1
            json.dump(d, fout)

mrtransfer('vocab_small.json', 'vocab_small_dict.json')
