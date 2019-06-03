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

def create_rec_list(user_id, tfidf_file, num_recs): 
    tf_idf = sp.load_npz(tfidf_file)
    tf_idf = tf_idf.toarray() 
    pos_mat, index_dict = make_user_matrix(user_id, tfidf_file)
    print('made user matrix')
    mat = np.matmul(pos_mat, tf_idf.T) 
    (n, m) = np.shape(mat)
    for i in range(n): 
        mat[i] = mat[i] / (np.linalg.norm(pos_mat[i]) + 1)
    for j in range(m): 
        mat[:, j] = mat[:, j] / (np.linalg.norm(tf_idf[j]) + 1)
    for big_index in index_dict.values(): 
        mat[:, big_index] = mat[:, big_index] * 0
    print('computed cosine similarities')
    rec_list = []
    for i in range(n): 
        ind = np.argsort(mat[i])[:num_recs]
        print(ind)
        rec_list += [(index_dict[i], j) for j in ind]
    print(rec_list)
    return rec_list 


def recommend(list_of_tups):
    with open('Small_Dataset_Processing/smaller_review_index_dict.json', 'r') as f:
        review_index_dict = json.load(f)
    with open('reviewid_businessid_dict.json', 'r') as g:
        business_id_dict = json.load(g)
    with open('businessid_business_name_dict.json', 'r') as h:
        business_name_dict = json.load(h)
    liked_review_ids = []
    recommended_review_ids = []
    for (review_id, index) in review_index_dict.items():
        for tup in list_of_tups:
            if index == int(tup[0]):
                liked_review_ids.append(review_id)
            elif index == int(tup[1]):
                recommended_review_ids.append(review_id)
    liked_businesses = []
    recommended_businesses = []
    for review_id in liked_review_ids:
        business_id = business_id_dict[review_id]
        business_name = business_name_dict[business_id]
        liked_businesses.append(business_name)
    for review_id in recommended_review_ids:
        business_id = business_id_dict[review_id]
        business_name = business_name_dict[business_id]
        recommended_businesses.append(business_name)
    for i in liked_businesses:
        ind = liked_businesses.index(i)
        s = 'Because you liked {}, we think you should try {}.'.format(\
            i, recommended_businesses[ind])
        print(s)

def go(user_id, tfidf_file, num_recs): 
    rec_list = create_rec_list(user_id, tfidf_file, num_recs)
    recommend(rec_list)

if __name__ == '__main__':
    go('7bbZoD0Tc2v1t8hYNY8GMA', 'tfidf.npz', 3)








