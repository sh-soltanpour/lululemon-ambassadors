from instapy import InstaPy
import pandas as pd
from config import crawler_username, crawler_password


print(crawler_username, crawler_password)


with open('europe_ambassadors.csv') as csv_file:
	df = pd.read_csv(csv_file)
	usernames = df.instagram


session = InstaPy(username=crawler_username, password=crawler_password)
session.login()

crawled_users = {'hassettwex', 'thecarlabredin', 'lorraineconwell', 'sarahshannonyoga', 'alessandragiunta'}

for username in usernames:
	if username in crawled_users:
		continue

	followers = session.grab_followers(username=username, amount="full", live_match=True, store_locally=True)
	# print(followers)
# with 