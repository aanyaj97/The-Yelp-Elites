    

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