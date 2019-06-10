import numpy as np
import scipy.sparse as sp 
import json

# maps the current index in small matrix to index in larger tf-idf matrix 

def make_user_matrix(user_id, tfidf_file):

    tf_idf = sp.load_npz(tfidf_file)
    tf_idf = tf_idf.toarray() 
    v = tf_idf.shape[1] #num elements in vocab 

    with open('userid_4star_review_dict.json') as f:
        dict_4star = json.load(f)
    with open('smaller_review_index_dict.json') as g:
        dict_indices = json.load(g)

    review_ids = dict_4star[user_id]

    index_dict = {}
    i = 0
    for review in review_ids: 
        index = dict_indices[review]
        index_dict[i] = index
        i += 1
    
    arrlst = []
    for review in review_ids:
        index = dict_indices[review]
        vector = tf_idf[index]
        arrlst.append(vector)
    result_array = np.array(arrlst)
    return result_array, index_dict 

def final_recommendations(user_id, tfidf_file, num_recs): 
    tf_idf = sp.load_npz(tfidf_file)
    tf_idf = tf_idf.toarray() 
    pos_mat, index_dict = make_user_matrix(user_id, tfidf_file)
    print('made user matrix')
    mat = np.matmul(pos_mat, tf_idf.T) 
    (n, m) = np.shape(mat)
    for i in range(n): 
        mat[i] = mat[i] / np.linalg.norm(pos_mat[i])
    for j in range(m): 
        mat[:, j] = mat[:, j] / np.linalg.norm(tf_idf[j])
    for big_index in index_dict.values(): 
        mat[:, big_index] = mat[:, big_index] * 0 
    print('computed cosine similarities')
    rec_list = []
    for i in range(n): 
        ind = np.argsort(mat[i])[:num_recs]
        rec_list += [(index_dict[i], j) for j in ind]
    return rec_list 



















    

