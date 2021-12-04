import json
import requests

with open('./australia_ambassadors.json') as f:
    data = json.load(f)

usernames = []
for record in data:
    username = record['instagram']
    usernames.append(username)
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
    response = requests.get(f'https://www.instagram.com/{username}/', headers=headers, params=params)
    print(response)
    if response.status_code == 200:
        record['id'] = response.json()['graphql']['user']['id']

with open('./result.json', 'w') as outfile:
    json.dump(data, outfile)