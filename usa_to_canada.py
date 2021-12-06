import json

with open('./usa_ambassadors.json') as f:
    data = json.load(f)

canadians = []
for record in data:
    if record['country'] == "Canada":
        canadians.append(record)

with open('./canada_ambassadors.json', 'w') as f:
    json.dump(canadians, f)