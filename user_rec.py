import numpy as np
from dummy_matrix import make_dummy_array
import json

def make_user_matrix(user_id):

	tf_idf = make_dummy_array()
	l = tf_idf.shape[1]

	with open('userid_4star_review_dict.json') as filename:
		dict_4star = json.load(filename)
	with open('smaller_review_index_dict.json') as filename:
		dict_indices = json.load(filename)

	review_ids = dict_4star[user_id]
	
	result_array = np.empty((0, l))
	
	for review in review_ids:
		index = dict_indices[review]
		vector = tf_idf[index]
		np.append(result_array, [vector], axis=0)

	return result_array










 	

