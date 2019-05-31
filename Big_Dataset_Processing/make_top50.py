'''
Conversion code to transfer mrjob output into a json of words with unique
numerical 'key' to be referenced in tf/idf vectors.
'''

import json
import heapq

with open('top50_dict.json', 'w') as outfile:
    with open('top50.json', 'r') as infile:
        queue = []
        for line in infile:
            word_key = tuple(line.split())
            k, v = word_key
            if len(queue) < 50:
                heapq.heappush(queue, (int(v), k[1:-1]))
            else:
                heapq.heappushpop(queue,(int(v), k[1:-1]))
        d = [word for (count, word) in queue]
        json.dump(d, outfile)
