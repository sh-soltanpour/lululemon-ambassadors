import json
import requests
import time


with open('./result.json') as f:
    data = json.load(f)

for record in data:
    headers = {
        'authority': 'i.instagram.com',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 9; GM1903 Build/PKQ1.190110.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/75.0.3770.143 Mobile Safari/537.36 Instagram 103.1.0.15.119 Android (28/9; 420dpi; 1080x2260; OnePlus; GM1903; OnePlus7; qcom; sv_SE; 164094539)',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'mid=YarB5AAEAAE-9ub8ttBY5dujr8q2; ig_did=7ABF8E1B-4E09-4CE5-9D9B-68749083F620; ig_nrcb=1; csrftoken=zYEQsIb6WSvmhho8jcw5tF5Yt8QGds5l; ds_user_id=29618483559; sessionid=29618483559%3AJhIcC8F3iQe06r%3A12; shbid="2002\\05429618483559\\0541670116721:01f7723b666b59d827af8c73730caeb6c980881aa7ad5cfa06c022bde257c1589148c329"; shbts="1638580721\\05429618483559\\0541670116721:01f766a2545e3ecb76311bd6356826ba6f1edf20255548bcc1f28e8af817fd653cb52ecc"; rur="NAO\\05429618483559\\0541670118118:01f75f18067c5981f183a6a2d7817e78aa2b0fee286240ee19745c1e2ceff141134b0b0a"',
    }

    params = (
        ('count', '10000'),
        ('search_surface', 'follow_list_page'),
    )
    if 'id' not in record:
        continue
    user_id = record['id']

    response = requests.get(f'https://i.instagram.com/api/v1/friendships/{user_id}/followers/', headers=headers,
                            params=params)
    print(response)
    if (response.status_code == 200):
        record['followers'] = response.json()['users']
    time.sleep(1)

with open('./result-2.json', 'w') as outfile:
    json.dump(data, outfile)