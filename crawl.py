from instapy import InstaPy
import pandas as pd
from config import crawler_username, crawler_password
import threading
import queue


def crawl_followers(username):
    if username in crawled_users:
        return
    followers = session.grab_followers(username=username, amount="full", live_match=False, store_locally=True)


def worker():
    while True:
        item = usernames_queue.get()
        crawl_followers(item)
        usernames_queue.task_done()


with open('europe_ambassadors.csv') as csv_file:
    df = pd.read_csv(csv_file)
    usernames = df.instagram

usernames_queue = queue.Queue()
for u in usernames:
    usernames_queue.put(u)

session = InstaPy(username=crawler_username, password=crawler_password, headless_browser=True)
session.login()

crawled_users = {'hassettwex', 'thecarlabredin', 'lorraineconwell', 'sarahshannonyoga', 'alessandragiunta'}
worker()
for i in range(2):
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()

usernames_queue.join()
