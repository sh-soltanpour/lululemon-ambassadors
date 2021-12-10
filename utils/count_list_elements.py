import json

total = 0
areas_lists = ["asia_1", "asia_2", "australia", "canada", "europe", "global", "korea", "uk"]
for area in areas_lists:
    with open(f'./ambassadors_lists/{area}_ambassadors.json') as f:
        data = json.load(f)
        total += len(data)
print(total)
# for record in data:
#     if 'followers' in record:
#         print(record['instagram'], len(record['followers']))
#         print("----------")
