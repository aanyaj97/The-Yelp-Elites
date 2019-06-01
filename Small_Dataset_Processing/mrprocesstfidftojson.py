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
                split = line.split()
                review_id = split[0]
                review_id = review_id[1:-1]
                tf_vec = split[1:]
                tf_vec[0] = float(tf_vec[0][3:-1])
                for i in range(1,19903):
                    tf_vec[i] = float(tf_vec[i][:-1])
                tf_vec[-1] = float(tf_vec[-1][:-3])
                d[review_id] = tf_vec
            json.dump(d, fout)

mrtransfer('test_dataidf1.json', 'test_dataidffinal.json')
