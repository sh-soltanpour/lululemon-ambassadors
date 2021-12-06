import json
with open('./uk_ambassadors.json') as f:
    data = json.load(f)

for record in data:
    if 'followers' in record:
        print(record['instagram'], len(record['followers']))
        print("----------")