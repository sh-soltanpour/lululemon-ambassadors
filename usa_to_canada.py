import json

with open('./lululemon_site_ambassadors/usa_canada_ambassadors.json') as f:
    data = json.load(f)

canadians = []
for record in data:
    if record['country'] == "United States":
        canadians.append(record)

with open('./usa_ambassadors.json', 'w') as f:
    json.dump(canadians, f)