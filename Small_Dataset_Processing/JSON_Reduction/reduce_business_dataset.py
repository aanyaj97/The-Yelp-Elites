import json
import string


def reduce_business_json(state_abbr):
    with open('../business.json') as f:
        data = {}
        for line in f:
           data_bus = json.loads(line)
           if data_bus["city"] == state_abbr:
               data[data_bus["business_id"]] = {"name": data_bus["name"],
                                            "stars": data_bus["stars"],
                                            "is_open": data_bus["is_open"],
                                            }

    with open('business_edited.json', 'w') as f:
        json.dump(data, f)

reduce_business_json("Champaign")
