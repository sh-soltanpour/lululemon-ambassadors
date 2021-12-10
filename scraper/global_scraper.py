"""
This file is the scraper for global region. Retrieves ambassadors, their city and instagram account.
"""

import os
import requests
import json

headers = {
    'authority': 'shop.lululemon.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    'sec-ch-ua-platform': '"Linux"',
    'content-type': 'application/json',
    'accept': '*/*',
    'origin': 'https://shop.lululemon.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://shop.lululemon.com/ambassadors/store-ambassadors',
    'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
    'cookie': f"Country=CA; s_ecid=MCMID%7C02772114470948128188394411253032628697; _scid=8b0df4bb-077b-44cf-a98f-5fec1eba06f5; mboxEdgeCluster=35; _sctr=1|1638514800000; _gcl_au=1.1.37893170.1638568962; __pdst=a9ec943b082e4bdca56f48c96c46a8fe; cd_user_id=17d82522d0f74c-00708aee96817a-162d1e0a-1fa400-17d82522d10c3e; _fbp=fb.1.1638573867285.1003562494; cartCount=0; __cq_uuid=efOQrcjd0a0EbcETLsXTEN5yZH; tfc-l=%7B%22k%22%3A%7B%22v%22%3A%227i0tockabugoqif8cemmjg1nhs%22%2C%22e%22%3A1701473082%7D%7D; __cq_seg=0~0.00!1~0.00!2~0.00!3~0.00!4~0.00!5~0.00!6~0.00!7~0.00!8~0.00!9~0.00; QuantumMetricUserID=f876e1e289a9a434639c8b4f33d6aebe; userPrefLanguage=fr_CA; a1ashgd=e37s2hu9f5c00000e37s2hu9f5c00000; lll-ecom-correlation-id=F092DFC9-72A6-C9F9-F9DB-A52A4300816D; akacd_RWASP-default-phased-release=3816060055~rv=84~id=a116568660a679841f8bc16bb9a0f2b8; ltmo=1; AMCVS_A92B3BC75245B1030A490D4D%40AdobeOrg=1; s_cc=true; WLS_ROUTE=.102; _gid=GA1.2.1118862350.1638734223; undefined; isLoggedin=false; check=true; AMCV_A92B3BC75245B1030A490D4D%40AdobeOrg=-2121179033%7CMCIDTS%7C18967%7CMCMID%7C02772114470948128188394411253032628697%7CMCAAMLH-1639381288%7C9%7CMCAAMB-1639381288%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1638783688s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.3.0; lll_usr=%7B%22alerts%22%3A%7B%7D%2C%22locale%22%3A%22fr_CA%22%2C%22sl%22%3A%22US%22%7D; xdVisitorId=10C8u6-WGeG-hq-r515ZP-3s1YZujJjV0SYVTg1SWr3RUTM0DBC; atgRecVisitorId=10C8u6-WGeG-hq-r515ZP-3s1YZujJjV0SYVTg1SWr3RUTM0DBC; _abck=1EECD4FA724CB8FF10ADED5B290DB491~0~YAAQl78mFyEOZRF9AQAAS86xjgdmw9xc0EeyQ7r96Cw8WD2aHpZlB7+0D1NJa6DFNfDlXeU9xjSUdiM3NoW18i1vop9/WNrVDS2MxJd3bq3O4KIkbkajwX/B97/htjacsW/9ekpQlt0rGsHQTJG8JcGLCYIaAtOzQC917KO5yioSQb5Ai5Lg+eBwglm7qvMVCFGZIEVElRjPdhdiydtMjjNYGE/HieTgnqGkl5hq7OWYqdvlwFvJW8Isb93iIglucgrmCnIB0DFVoHrK6H6MXXjpCTXxuEZjAi1WWe9IjK+5oXI1jOVpZc76fTaBYGmswEmeAxCsYow3K1H1QbN5BtESiFwB5odtDxECxXgIcvCLRx6nFoe8twrSaPGZ6jDaL5qui8aE26pCCubGGMxpJWq4krYsdMfojTw=~-1~-1~-1; bm_sz=4371CE4507FDFC132263DC85EBAFA6C1~YAAQl78mFyIOZRF9AQAAS86xjg5SgVz3fjStRhcWyZNxnon0uGjznn29m6o+cOUHKDfjormTsFsswtgyf7UfXp4jzoM4h66lZNam9/NulSnhXXf4dR6bOLhPcyIv8pziWOOaVdfeS4kLX/Kz7sQWa+yzyzj1HvaejzzX3a3x807bav0sKboQloR9wgFF5xGdHrIh/Cgwz2ZK65SXJ0Y/ST7fvkjLn5SUndcZCn3mW7PsTsncN+tYTdA3i9Pm+pyN5TOP8RCpFH7gD9IwVUWu6Ap8qLYjeQSAOoYjRQ9/WdauI4N9Qo4=~3420469~3359795; lll_adobe_geo_country=canada; lll_adobe_geo_state=alberta; lll_adobe_geo_city=calgary; lll_adobe_geo_postal_zip=t2r%200a1; lll_adobe_geo_latitude=51.04; lll_adobe_geo_longitude=-114.06; atgRecSessionId=8TWPE2QojZVvNQPQOvaEEuqzhZYVQKxaJJ4Kc_rFn1sYs3tiUyT-!-1450166882!-900695727; JSESSIONID=WI-PFIXXoFsW7nsNUP_G7vIyGvShddPX7c61QXd8CCyj3797yu1e!-1390629958; ca_ord_stores=\"pMlNRyVXVK9lm2b7YpF2/A==<|>XzGjq9zxQ8E=\"; us_ord_stores=\"pMlNRyVXVK/K59g9JHyVig==<|>XzGjq9zxQ8E=\"; us_ord=\"pMlNRyVXVK/K59g9JHyVig==\"; mbox=PC#b007474c946846f6a700c1e5cfa500f8.34_0#1702027947|session#dac45e312f4a42cfbef528e681a1510f#1638784807; digitalData.page.a1Token=2a$10$bWpM83fqZ6nG02j7Gh/4XOPqzE.GOPeLtP.XNv9LvENJQAdGT/RBG; kampyleUserSession=1638783605001; kampyleUserSessionsCount=17; QuantumMetricSessionID=c675a55e947a33a5236e21b986ff054d; _gat_gtag_UA_4236786_4=1; ca_ord=\"pMlNRyVXVK9NR3xSDthpRg==\"; sl=US; UsrLocale=en_US; _ga=GA1.2.18144351.1638568962; _uetsid=c206ded0560511eca966bdb728ea2712; _uetvid=2e16643031e411eca1e7db081018f6e8; kampyleSessionPageCounter=9; s_sq=llmnprod%3D%2526c.%2526a.%2526activitymap.%2526page%253Dambassadors%25253Astore-ambassadors%2526link%253DBarry%252520Clark%252520Run%252520Crew%252520Lead%2526region%253D__next%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Dambassadors%25253Astore-ambassadors%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fshop.lululemon.com%25252Fambassadors%25252Fstore-ambassadors%25252Fvirginia-beach%25252Fbarry-clark%2526ot%253DA%26llmncaprod%3D%2526c.%2526a.%2526activitymap.%2526page%253Dhomepage%2526link%253DUnited%252520States%252520USD%2526region%253Dregion-selector-accordion-item__panel-North-America%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Dhomepage%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fshop.lululemon.com%25252F%25253Flocale%25253Den_US%252526sl%25253DUS%2526ot%253DA; ak_bmsc=AF4B232410409B39EB9529625DC177BC~000000000000000000000000000000~YAAQl78mFz3vaBF9AQAAVqoejw5taAArjOBtGSNOLaO1ENcDi2ldl3wWwSTgTJKeJ1tkXroKn1n7vfGYB9x6oTbVIAdHXw1JbdRNukbyLBx+ZuK56uad/IndQTgxA3iOWw7k3TF+GxPBfezw74fQ1eFmv8KL67MH/jGak/fgR8dhdGGPbQ9nS+jv7E+C3XDwayfWKzv8ToyVTXYqCnh6sK8VrMH588a4PC07hm4+g2Nq2uXTJHWugtfjei4lPFp/3uh7cj9/GgpeN8NFKvYiZr2xp0OQy4Q/hASunnAA7UnuCPGxuiDi3mb9Oe6wVKV/KWYcF+zZ3bq+FEHXlTMXFawR7WfG/eddINLE0HouamI1ZR1aG02e7Tknr8z061E7pihT9jqhdmWgB6HSU6w=; bm_sv=0EA6D65E72AF57D272FB4F95F76167E6~+JBDqnOfYVmDH31aJ8Of/r3Qsa+ngCHSCzOC3DFj8IJxx0oGuAvNK2xErmZSS3EGqYbEOYsCEZ2CX6lYSbeopA+Kp6eRkYfjn/8ZXmw+Exy7+ggqCTFCHhu/H4FWu3puh2Pk1JoigRik9vQVZ5uHjR7kl24qrwct97aYyN/UX0k=; _ga_CCD7VVYPZ7=GS1.1.1638782942.10.1.1638783689.22",
}


with open('globals.txt', 'r') as f:
    lines = [line.rstrip() for line in f]

data_amb = []
for l in lines:
    data = '{"query":"query ($slug: String!) {\\n  ambassadorBySlug(slug: $slug) {\\n    biography\\n    city\\n    countryName\\n    facebook\\n    fact1\\n    fact2\\n    fact3\\n    fact4\\n    fact5\\n    firstName\\n    instagram\\n    lastName\\n    profileImageUrl\\n    store {\\n      name\\n      city\\n      state\\n      slug\\n    }\\n    strava\\n    subDiscipline\\n    twitter\\n    type\\n    website\\n    youtube\\n    urlSlug\\n  }\\n}\\n","variables":{"slug":"%s"}}'%l
    response = requests.post('https://shop.lululemon.com/cne/graphql', headers=headers, data=data)
    res_json = response.json()['data']['ambassadorBySlug']
    x = {
        "name": res_json['firstName'] + res_json['lastName'], 
        'city': res_json['city'],
        'instagram': res_json['instagram'],
        'country': res_json['countryName'],
    }
    print(x)
    data_amb.append(x)

with open('global_ambassadors.json', 'w') as f:
    json.dump(data_amb, f)
