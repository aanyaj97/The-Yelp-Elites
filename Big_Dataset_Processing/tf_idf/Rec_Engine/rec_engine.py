import numpy as np
import scipy.sparse as sp 
import json

'''
This file creates recommendation engine such that given a unique user ID, 
it would provide a list of recommended places based on high 
TFIDF similarity scores. This is done over a test dataset for places 
among Champaign, IL, but can be used for larger datasets with relevant 
files as inputs. 

test more sample user ids from userid_4star_review_dict.json 
where file is in the form user_id: [list of 4star+ review_ids]
''' 

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
    '''
    Function that computes the recommendation list. 

    ''' 
    tf_idf = sp.load_npz(tfidf_file)
    tf_idf = tf_idf.toarray() 
    pos_mat, index_dict = make_user_matrix(user_id, tfidf_file)
    #print('made user matrix')
    mat = np.matmul(pos_mat, tf_idf.T) 
    (n, m) = np.shape(mat)
    for i in range(n): 
        mat[i] = mat[i] / (np.linalg.norm(pos_mat[i]) + 1)
    for j in range(m): 
        mat[:, j] = mat[:, j] / (np.linalg.norm(tf_idf[j]) + 1)
    for big_index in index_dict.values(): 
        mat[:, big_index] = mat[:, big_index] * 0
    #print('computed cosine similarities')
    rec_list = []
    for i in range(n): 
        ind = np.argsort(mat[i])[:num_recs]
        rec_list += [(index_dict[i], j) for j in ind]
    return rec_list 


def recommend(list_of_tups, num_recs):
    '''
    Handles post processing and prints output of recommendations. 

    Input: 
        list_of_tups: (pairs, of restaurants). Note that this could be done with a 
        simple list, but the function could also be modified to give recommendations 
        based on specific places you may have visited rather than general ones so it 
        is useful to pass list of tuples. 

        num_recs: number of recommendations. Note the function  may not yield the 
        as many recommendations as that of num_recs, because it filters whether 
        the restaurant has positive reviews. 

    ''' 
    with open('Small_Dataset_Processing/smaller_review_index_dict.json', 'r') as f:
        review_index_dict = json.load(f)
    with open('reviewid_businessid_dict.json', 'r') as g:
        business_id_dict = json.load(g)
    with open('businessid_business_name_dict.json', 'r') as h:
        business_name_dict = json.load(h)
    with open('good_businesses.json', 'r') as i:
        good_businesses = json.load(i)

    list_of_lists = []
    for i in range(0, int(len(list_of_tups)/num_recs)):
        interval = num_recs*i
        list_of_lists.append(list_of_tups[interval:interval+num_recs])

    recommended_review_ids = []
    for l in list_of_lists:
        rec_indices = []
        rec_ids = []
        for tup in l:
            rec_indices.append(tup[1]) 
        for (review_id, index) in review_index_dict.items():
            if index in rec_indices:
                rec_ids.append(review_id)
        recommended_review_ids.append(rec_ids)

    rec_businesses = []
    for review_id_list in recommended_review_ids:
        business_name_list = []
        for review_id in review_id_list:
            business_id = business_id_dict[review_id]
            if business_id in good_businesses:
                business_name = business_name_dict[business_id]
                business_name_list.append(business_name)
        rec_businesses.append(business_name_list)

    recommended_businesses = []
    for rec_business_list in rec_businesses:
        for rest in rec_business_list:
            if rest not in recommended_businesses:
                recommended_businesses.append(rest)
    s_recommend = ''
    if len(recommended_businesses) > 0:
        if len(recommended_businesses) > 2:
            for rest in recommended_businesses:
                if recommended_businesses.index(rest) != (len(recommended_businesses) - 1):
                    s_recommend = s_recommend + rest + ', '
                else:
                    s_recommend = s_recommend + 'and ' + rest
        elif len(recommended_businesses) == 1:
            s_recommend = recommended_businesses[0]
        elif len(recommended_businesses) == 2:
            s_recommend = recommended_businesses[0] + ' and ' + recommended_businesses[1]
    else:
        s = "We couldn't find any recommendations based on the places you like."
        print(s)
        return None 
    if s_recommend != '':
        s = 'Because of the places you liked, we think you should try {}.'.format(s_recommend)
    print(s)        



def go(user_id, tfidf_file, num_recs): 
    rec_list = create_rec_list(user_id, tfidf_file, num_recs)
    recommend(rec_list, num_recs)

if __name__ == '__main__':
    go("nCbHlJEJtqpGIWLRtlTQ0g", 'tfidf.npz', 10) #sample user-id. 









