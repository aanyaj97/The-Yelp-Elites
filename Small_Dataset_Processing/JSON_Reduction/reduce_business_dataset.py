import json
import string

states = ['AB', 'AZ', 'IL', 'NC', 'NV', 'OH', 'ON', 'PA', 'QC', 'SC'] 


def reduce_business_json(state_abbr):
    with open('../business.json') as f:
        with open(state_abbr + '_business_editedMRJobsafe.json', 'w') as fout:
            for line in f:
                data = {}
                data_bus = json.loads(line)
                if data_bus["state"] == state_abbr:
                    data = {"business_id": data_bus["business_id"],
                            "name": data_bus["name"], "stars": data_bus["stars"],
                            "is_open": data_bus["is_open"]}
                    json.dump(data, fout)
                    fout.write('\n')

for state in states:
    reduce_business_json(state)
