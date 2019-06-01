import json
import string

with open ('business_edited.json') as b:
    data = json.load(b)
    businesses = list(data.keys())

with open('../review.json', 'r') as fin:
    with open('reviews_edited.json', 'w') as fout:
        data = {}
        for line in fin:
            data_rev = json.loads(line)
            if data_rev["business_id"] in businesses:
                data[data_rev["review_id"]] = {"business_id": data_rev["business_id"],
                                           "user_id": data_rev["user_id"],
                                            "stars": data_rev["stars"],
                                           "text": data_rev["text"]}
                review_info = {"review_id":data_rev["review_id"],
                          "business_id": data_rev["business_id"],
                           "user_id": data_rev["user_id"],
                            "stars": data_rev["stars"],
                            "text": data_rev["text"]}
                json.dump(review_info, fout)
with open('reviews_edited_dict.json', 'w') as outfile:
    json.dump(data, outfile)
