import json
import string

with open ('business_edited.json') as b:
    data = json.load(b)
    businesses = list(data.keys())

with open('../review.json') as f:
    data = {}
    for line in f:
        data_rev = json.loads(line)
        if data_rev["business_id"] in businesses:
            data[data_rev["review_id"]] = {"business_id": data_rev["business_id"],
                                           "user_id": data_rev["user_id"],
                                           "stars": data_rev["stars"],
                                           "text": data_rev["stars"]}
with open('reviews_edited.json', 'w') as outfile:
    json.dump(data, outfile)
