import json
import time

import requests
import sys

ambassadors_file = ' '.join(sys.argv[1:])

with open(ambassadors_file) as f:
    data = json.load(f)
count = 0
for record in data:
    print("-----------------")
    count += 1
    print(f"Processing {count}/{len(data)}")

    headers = {
        'authority': 'www.instagram.com',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'mid=YarB5AAEAAE-9ub8ttBY5dujr8q2; ig_did=7ABF8E1B-4E09-4CE5-9D9B-68749083F620; ig_nrcb=1; csrftoken=zYEQsIb6WSvmhho8jcw5tF5Yt8QGds5l; ds_user_id=29618483559; sessionid=29618483559%3AJhIcC8F3iQe06r%3A12; shbid="2002\\05429618483559\\0541670116721:01f7723b666b59d827af8c73730caeb6c980881aa7ad5cfa06c022bde257c1589148c329"; shbts="1638580721\\05429618483559\\0541670116721:01f766a2545e3ecb76311bd6356826ba6f1edf20255548bcc1f28e8af817fd653cb52ecc"; rur="NAO\\05429618483559\\0541670118595:01f7576c45ff480438fcec1a9746237ab6b236628bdccfcbd0a56af55791afd749c09c6e"',
    }
    params = (
        ('__a', '1'),
    )
    username = record['instagram']
    print(f"Username: {username}")
    response = requests.get(f'https://www.instagram.com/{username}/', headers=headers, params=params)
    print(response)
    if response.status_code == 200:
        record_id = response.json().get('graphql',{}).get('user',{}).get('id')
        if record_id is None:
            continue
        record['id'] = record_id
    else:
        continue

    print("Retrieved Id")
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
    response = requests.get(f'https://i.instagram.com/api/v1/friendships/{record["id"]}/followers/', headers=headers,
                            params=params)
    print(response)
    if response.status_code == 200:
        all_followers = record.get('followers', []) + list(response.json()['users'])
        record['followers'] = list({v['pk']: v for v in all_followers}.values())

    time.sleep(1)
    print("Retrieved Followers")

with open(ambassadors_file, 'w') as outfile:
    json.dump(data, outfile)