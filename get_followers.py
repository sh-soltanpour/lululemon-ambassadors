"""
When you run this file, you should pass the address of the ambassadors region to it, and it will populate that file
with followers of the ambassador. Example:
python get_followers.py ambassador_lists/canada_ambassadors.json
"""

import json
import time

import requests
import sys

ambassadors_file = ' '.join(sys.argv[1:])

with open(ambassadors_file) as f:
    data = json.load(f)
count = 0

for record in data:
    try:
        print("-----------------")
        count += 1
        print(f"Processing {count}/{len(data)}")
        if count == 400:
            break
        headers = {
            'authority': 'www.instagram.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 9; GM1903 Build/PKQ1.190110.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/75.0.3770.143 Mobile Safari/537.36 Instagram 103.1.0.15.119 Android (28/9; 420dpi; 1080x2260; OnePlus; GM1903; OnePlus7; qcom; sv_SE; 164094539)',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': 'ig_did=DD71B3BC-E1F4-4E34-B812-B5D771CBD718; ig_nrcb=1; mid=Ya8DOAAEAAE5YLr6PYMN6AU8Zbi4; csrftoken=DB9M9fWiuGOsFRVUpZCQsncHZjR6t3gB; ds_user_id=50372941876; sessionid=50372941876%3AHovOPh1bTYtCEZ%3A3; rur="NAO\\05450372941876\\0541670395801:01f7958c1838f45386f12eb0c1d62d29cbe27392fdf5f2141ae2e6badc05d26fc8088faf"',
        }
        params = (
            ('__a', '1'),
        )
        username = record['instagram']
        print(f"Username: {username}")
        response = requests.get(f'https://www.instagram.com/{username}/', headers=headers, params=params)
        print(response)
        print(response.status_code)
        if response.status_code == 200:
            record_id = response.json().get('graphql', {}).get('user', {}).get('id')
            print(f"REC iD:{record_id}")
            if record_id is None:
                continue
            record['id'] = record_id
        else:
            continue

        print("Retrieved Id")
        headers = {
            'authority': 'i.instagram.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 9; GM1903 Build/PKQ1.190110.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/75.0.3770.143 Mobile Safari/537.36 Instagram 103.1.0.15.119 Android (28/9; 420dpi; 1080x2260; OnePlus; GM1903; OnePlus7; qcom; sv_SE; 164094539)',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': 'ig_did=290CDBE8-02C6-4D5E-BA71-CB0D9A693AED; ig_nrcb=1; mid=Ya57mwAEAAGZf9CxMszzUCnzMzUL; csrftoken=HVqF7SJJidn07OBPVTiJldHeANkWTsxM; ds_user_id=50372941876; sessionid=50372941876%3AgSTy9zzYfVD0uk%3A29; rur="EAG\\05450372941876\\0541670361006:01f7eaa53e894b34555dcf61f0a9090af02c0973480ab97a5e63758c754a88c3a037576d"',
        }

        params = (
            ('count', '10000'),
            ('search_surface', 'follow_list_page'),
        )
        response = requests.get(f'https://i.instagram.com/api/v1/friendships/{record["id"]}/followers/',
                                headers=headers,
                                params=params)
        print(response)
        if response.status_code == 200:
            all_followers = record.get('followers', []) + list(response.json()['users'])
            record['followers'] = list({v['pk']: v for v in all_followers}.values())

        time.sleep(1)
        print("Retrieved Followers")
    except:
        pass

with open(ambassadors_file, 'w') as outfile:
    json.dump(data, outfile)
