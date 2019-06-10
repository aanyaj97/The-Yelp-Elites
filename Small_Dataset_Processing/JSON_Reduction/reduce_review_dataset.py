import json
import string


states = ['AB', 'AZ', 'IL', 'NC', 'NV', 'OH', 'ON', 'PA', 'QC', 'SC']

def reduce_reviews(state_abbr):
    with open (state_abbr + '_business_editedMRJobsafe.json') as b:
        businesses = set()
        for line in b:
            data = json.loads(line)
            businesses.add(data['business_id'])

        with open('../review.json', 'r') as fin:
            with open(state_abbr + '_reviews_editedMRJobsafe.json', 'w') as fout:
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
                        fout.write('\n')

for state in states:
    reduce_reviews(state)
