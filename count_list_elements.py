import json
with open('./result-2.json') as f:
    data = json.load(f)

for record in data:
    if 'followers' in record:
        print(len(record['followers']))