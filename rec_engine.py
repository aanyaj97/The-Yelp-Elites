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


def recommend(list_of_tups, num_recs):
    with open('Small_Dataset_Processing/smaller_review_index_dict.json', 'r') as f:
        review_index_dict = json.load(f)
    with open('reviewid_businessid_dict.json', 'r') as g:
        business_id_dict = json.load(g)
    with open('businessid_business_name_dict.json', 'r') as h:
        business_name_dict = json.load(h)

    list_of_lists = []
    for i in range(0, int(len(list_of_tups)/num_recs)):
        interval = num_recs*i
        list_of_lists.append(list_of_tups[interval:interval+num_recs])

    liked_review_ids = []
    recommended_review_ids = []
    for l in list_of_lists:
        liked_index = l[0][0]
        rec_indices = []
        rec_ids = []
        for tup in l:
            rec_indices.append(tup[1]) 
        for (review_id, index) in review_index_dict.items():
            if index == liked_index:
                liked_review_ids.append(review_id)
            elif index in rec_indices:
                rec_ids.append(review_id)
        recommended_review_ids.append(rec_ids)

    liked_businesses = []
    rec_businesses = []
    for review_id in liked_review_ids:
        business_id = business_id_dict[review_id]
        business_name = business_name_dict[business_id]
        liked_businesses.append(business_name)
    for review_id_list in recommended_review_ids:
        business_name_list = []
        for review_id in review_id_list:
            business_id = business_id_dict[review_id]
            business_name = business_name_dict[business_id]
            business_name_list.append(business_name)
        rec_businesses.append(business_name_list)

    for business in liked_businesses:
        rec_list = rec_businesses[liked_businesses.index(business)]
        s_recommend = ''
        if num_recs > 1:
            for ind in range(0, len(rec_list) - 1):
                s_recommend = s_recommend + rec_list[ind] + ', '
            s_recommend = s_recommend + 'and ' + rec_list[len(rec_list) - 1]
        else:
            s_recommend = rec_list[0]
        s = 'Because you liked {}, we think you should try {}.'.format(business, s_recommend)
        print(s)



def go(user_id, tfidf_file, num_recs): 
    rec_list = create_rec_list(user_id, tfidf_file, num_recs)
    recommend(rec_list)

if __name__ == '__main__':
    go('7bbZoD0Tc2v1t8hYNY8GMA', 'tfidf.npz', 3)








