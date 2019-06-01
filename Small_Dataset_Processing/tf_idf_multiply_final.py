import json
import numpy as np

def tf_idf(tf_file, idf_file, outfile):
    d = {}
    with open(outfile, 'w') as tfidfout:
        with open(tf_file) as tfin:
            tf_dict = json.load(tfin)
        with open(idf_file) as idfin:
            idf_dict = json.load(idfin)
            for key, value in tf_dict.items():
                tf_array = np.array(value)
                idf_array = np.array(idf_dict[key])
                tf_idf = tf_array * idf_array
                d[key] = list(tf_idf)
        json.dump(d, tfidfout)


tf_idf('test_dataidffinal.json', 'test_dataidffinal.json', 'test_datatfidf.json')
